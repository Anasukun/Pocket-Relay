from pathlib import Path

import pytest

from pocketrelay.application.approval_service import ApprovalService
from pocketrelay.security.path_guard import ensure_child_path, resolve_project_path
from pocketrelay.security.redaction import redact_secrets


def test_path_guard_traversal():
    with pytest.raises(ValueError):
        resolve_project_path(Path("../secret_folder"))

    with pytest.raises(ValueError):
        resolve_project_path(Path("project\x00path"))

def test_ensure_child_path():
    parent = Path("./data/worktrees").resolve()
    child = parent / "task-1"
    assert ensure_child_path(child, parent) == child.resolve()

    outside_child = Path("./data/../other_folder").resolve()
    with pytest.raises(PermissionError):
        ensure_child_path(outside_child, parent)

def test_secret_redaction():
    text = (
        "Telegram Token: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz123456789\n"
        "GitHub Token: ghp_1234567890abcdefghijklmnopqrstuvwxyz\n"
        "AWS Key: AKIAIOSFODNN7EXAMPLE\n"
        "DB: postgresql://admin:secretpass@localhost:5432/db\n"
    )
    redacted = redact_secrets(text)
    
    assert "[REDACTED_TELEGRAM_TOKEN]" in redacted
    assert "[REDACTED_GITHUB_TOKEN]" in redacted
    assert "[REDACTED_AWS_KEY]" in redacted
    assert "[REDACTED_PASSWORD]" in redacted
    assert "secretpass" not in redacted
    assert "ghp_" not in redacted

def test_approval_service_lifecycle():
    service = ApprovalService()
    task_id = "PR-101"
    user_id = 123456
    diff_content = "diff --git a/file.txt b/file.txt\n+hello"

    req = service.create_request(task_id, user_id, "git_commit", diff_content)
    assert req.status == "PENDING"

    # Test tampering rejection
    tampered_hash = service.compute_hash("different diff content")
    assert not service.consume_approval(req.id, user_id, tampered_hash)

    # Test wrong user rejection
    correct_hash = service.compute_hash(diff_content)
    assert not service.consume_approval(req.id, 999999, correct_hash)

    # Test successful approval
    assert service.consume_approval(req.id, user_id, correct_hash)
    assert req.status == "APPROVED"

    # Test single-use (cannot consume twice)
    assert not service.consume_approval(req.id, user_id, correct_hash)
