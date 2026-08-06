import asyncio
from dataclasses import dataclass
from pathlib import Path

from pocketrelay.security.redaction import redact_secrets


@dataclass
class DiffSummary:
    status_short: str
    diff_stat: str
    full_diff: str

async def get_worktree_diff(worktree_path: Path) -> DiffSummary:
    # 1. git status --short
    proc_status = await asyncio.create_subprocess_exec(
        "git", "-C", str(worktree_path), "status", "--short",
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout_status, _ = await proc_status.communicate()
    status_text = stdout_status.decode("utf-8", errors="replace").strip()

    # 2. git diff --stat
    proc_stat = await asyncio.create_subprocess_exec(
        "git", "-C", str(worktree_path), "diff", "HEAD", "--stat",
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout_stat, _ = await proc_stat.communicate()
    stat_text = stdout_stat.decode("utf-8", errors="replace").strip()

    # 3. git diff HEAD
    proc_diff = await asyncio.create_subprocess_exec(
        "git", "-C", str(worktree_path), "diff", "HEAD",
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout_diff, _ = await proc_diff.communicate()
    diff_text = stdout_diff.decode("utf-8", errors="replace").strip()

    return DiffSummary(
        status_short=redact_secrets(status_text),
        diff_stat=redact_secrets(stat_text),
        full_diff=redact_secrets(diff_text),
    )
