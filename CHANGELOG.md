# Changelog

All notable changes to PocketRelay will be documented in this file.

## [v0.1.0-alpha] - 2026-08-06

### Added
- **Local-first Architecture:** Asynchronous Python 3.12 core using `uv` dependency management.
- **Telegram Shell:** Commands `/start`, `/help`, `/projects`, `/use`, `/status`, `/pair`, `/doctor`.
- **Adapter-Neutral Framework:** `AgentAdapter` Protocol supporting `AntigravityCliAdapter` (Google Antigravity CLI `agy`) and `FakeAgentAdapter`.
- **Non-Technical UX:** Interactive Setup Wizard (`pocketrelay init`) and 6-digit numeric Telegram auto-pairing (`/pair <code>`).
- **Path Guard Security:** Protection against directory traversal (`..`), null bytes, filesystem roots, and folder escape.
- **Secret Redaction:** Automatic redaction of Telegram tokens, GitHub PATs, AWS keys, database passwords, and SSH keys.
- **Git Worktree Isolation:** Per-task isolated worktrees (`pocketrelay/task-<task_id>`).
- **Human-in-the-Loop Approvals:** Inline Telegram commit approval buttons with SHA-256 diff hash binding, 5-minute expiry, and single-use consumption.
- **Diagnostics:** System doctor tool (`pocketrelay doctor`).
- **Packaging:** Dockerfile and `docker-compose.yml` for self-hosting.
