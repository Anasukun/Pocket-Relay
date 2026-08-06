import asyncio
from pathlib import Path

from pocketrelay.security.path_guard import ensure_child_path, resolve_project_path


class WorktreeManager:
    def __init__(self, base_worktree_dir: Path = Path("./data/worktrees")) -> None:
        self.base_worktree_dir = base_worktree_dir.resolve()
        self.base_worktree_dir.mkdir(parents=True, exist_ok=True)

    async def create_worktree(self, repo_path: Path, task_id: str, base_branch: str = "main") -> Path:
        resolved_repo = resolve_project_path(repo_path)
        branch_name = f"pocketrelay/task-{task_id}"
        worktree_path = self.base_worktree_dir / f"wt-{task_id}"
        ensure_child_path(worktree_path, self.base_worktree_dir)

        command = [
            "git",
            "-C",
            str(resolved_repo),
            "worktree",
            "add",
            "-b",
            branch_name,
            str(worktree_path),
            base_branch,
        ]

        proc = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _stdout, stderr = await proc.communicate()

        if proc.returncode != 0:
            err_msg = stderr.decode("utf-8", errors="replace")
            raise RuntimeError(f"Failed to create Git worktree for task {task_id}: {err_msg}")

        return worktree_path

    async def remove_worktree(self, repo_path: Path, worktree_path: Path) -> None:
        resolved_repo = resolve_project_path(repo_path)
        ensure_child_path(worktree_path, self.base_worktree_dir)

        command = [
            "git",
            "-C",
            str(resolved_repo),
            "worktree",
            "remove",
            "--force",
            str(worktree_path),
        ]

        proc = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await proc.communicate()

worktree_manager = WorktreeManager()
