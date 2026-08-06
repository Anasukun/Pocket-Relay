from datetime import datetime
from pathlib import Path

from pydantic import BaseModel

from .enums import TaskStatus


class Task(BaseModel):
    id: str
    user_id: int
    chat_id: int
    project_slug: str
    prompt: str
    status: TaskStatus = TaskStatus.CREATED
    conversation_id: str | None = None
    worktree_path: Path | None = None
    created_at: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None
