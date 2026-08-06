import asyncio
import uuid
from datetime import UTC, datetime
from pathlib import Path

from pocketrelay.adapters.base import AgentRequest
from pocketrelay.adapters.registry import get_adapter
from pocketrelay.application.project_service import project_service
from pocketrelay.domain.models import Task, TaskStatus
from pocketrelay.settings import config


class TaskService:
    def __init__(self) -> None:
        self.tasks: dict[str, Task] = {}
        self.queue: asyncio.Queue[Task] = asyncio.Queue()

    async def create_from_prompt(self, user_id: int, chat_id: int, prompt: str, project_slug: str = "example") -> Task:
        task_id = f"PR-{str(uuid.uuid4())[:8]}"
        task = Task(
            id=task_id,
            user_id=user_id,
            chat_id=chat_id,
            project_slug=project_slug,
            prompt=prompt,
            created_at=datetime.now(UTC),
            status=TaskStatus.QUEUED
        )
        self.tasks[task_id] = task
        await self.queue.put(task)
        return task

    def get_task(self, task_id: str) -> Task | None:
        return self.tasks.get(task_id)

    async def execute(self, task: Task) -> None:
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now(UTC)
        
        try:
            proj = project_service.get_project(task.project_slug)
            adapter = get_adapter(proj.adapter)
            workspace = proj.repository_path
        except Exception:  # noqa: BLE001
            # Fallback to fake adapter if project not found or invalid path
            adapter = get_adapter("fake")
            workspace = Path(".")

        # Enforce security policies
        if not config.security.allow_raw_shell:
            req_sandbox = True
        else:
            req_sandbox = False

        import structlog
        logger = structlog.get_logger()
        
        if not config.security.allow_raw_shell:
            dangerous_patterns = ['$(', '`', '| ', '; ', '&& ', '|| ', '> ', '>> ']
            for pattern in dangerous_patterns:
                if pattern in task.prompt:
                    logger.warning("Potentially dangerous shell pattern in prompt", 
                                   task_id=task.id, pattern=pattern)
                    break

        req = AgentRequest(
            prompt=task.prompt,
            workspace=workspace,
            conversation_id=task.conversation_id,
            sandbox=req_sandbox,
        )

        result = await adapter.run(req)

        if result.conversation_id:
            task.conversation_id = result.conversation_id

        if result.status.upper() in ("SUCCESS", "COMPLETED"):
            task.status = TaskStatus.COMPLETED
        else:
            task.status = TaskStatus.FAILED

        task.finished_at = datetime.now(UTC)

    async def mark_failed(self, task_id: str, error: str) -> None:
        if task := self.get_task(task_id):
            task.status = TaskStatus.FAILED
            task.finished_at = datetime.now(UTC)

task_service = TaskService()

async def worker() -> None:
    while True:
        task = await task_service.queue.get()
        try:
            await task_service.execute(task)
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001
            await task_service.mark_failed(task.id, str(exc))
        finally:
            task_service.queue.task_done()
