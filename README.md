# 📱 PocketRelay

> **A Free-to-Use Mobile Remote for Google Antigravity & AI Coding Agents via Telegram**

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Security Status](https://img.shields.io/badge/security-hardened-success.svg)](SECURITY.md)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](Dockerfile)

---

## 🌟 Overview

**PocketRelay** turns your smartphone into a remote control for AI coding agents running on your local development machine. Send prompts, review git diffs, run tests, and approve commits on the go—directly through Telegram.

Built **local-first** with **deny-by-default security**, PocketRelay keeps your source code, credentials, and tokens safely on your machine without requiring cloud subscriptions or third-party servers.

```text
📱 Smartphone (Telegram) ──► 🤖 Telegram Bot Gateway ──► 💻 Local PocketRelay Controller
                                                                  │
                                                        ┌─────────┴─────────┐
                                                        ▼                   ▼
                                                  Google Antigravity    Claude Code / Aider
                                                        │                   │
                                                        └─────────┬─────────┘
                                                                  ▼
                                                      🌿 Isolated Git Worktree
```

---

## ✨ Key Features

- 🔒 **Local-First & Deny-by-Default**: Secrets, credentials, and repository files never leave your computer.
- 🔑 **Cryptographic Pairing & Lockout**: Secure setup via one-time 6-digit terminal codes with rate limiting and automated brute-force protection.
- ⚡ **Multi-Agent Adapter Platform**: Out-of-the-box support for **Google Antigravity CLI (`agy`)**, **Claude Code (`claude`)**, **Aider**, **Codex**, **Gemini**, and custom CLIs.
- 🌿 **Git Worktree Isolation**: Executes coding tasks in isolated git worktrees so your main branch stays untouched until approved.
- 🛡️ **Secret Redaction**: Automatically redacts API keys, tokens, and database passwords from diffs and stdout before sending to Telegram.
- 🎯 **Interactive Telegram Approvals**: Review line-by-line diffs and approve or reject commits via interactive Telegram inline buttons.
- 🩺 **Built-in Diagnostics & Setup Wizard**: Interactive setup wizard (`pocketrelay init`) and health check diagnostic tool (`pocketrelay doctor`).

---

## 🚀 Quick Start

### Prerequisites

- **Python**: 3.12 or newer
- **Git**: Installed and available in your `PATH`
- **Coding Agent CLI**: Google Antigravity (`agy`), Claude Code (`claude`), or similar
- **Telegram Bot**: Created via [@BotFather](https://t.me/BotFather)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Anasukun/Pocket-Relay.git
   cd Pocket-Relay
   ```

2. **Set up virtual environment & install dependencies:**
   Using `uv` (recommended):
   ```bash
   uv sync
   ```
   Or using standard `pip`:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e .
   ```

3. **Run Guided Setup Wizard:**
   ```bash
   uv run pocketrelay init
   # Or `pocketrelay init` if virtual environment is activated
   ```
   The wizard will auto-detect installed agent CLIs, prompt for your Telegram Bot Token, set up your project directory, generate secure local configs, and issue a pairing code.

4. **Verify System Health:**
   ```bash
   uv run pocketrelay doctor
   ```

5. **Start PocketRelay:**
   ```bash
   uv run pocketrelay run
   ```

---

## 📱 Pairing & Telegram Usage

1. Open Telegram on your phone and open a chat with your newly created Bot.
2. Send the pair command printed during `init`:
   ```text
   /pair <6-digit-code>
   ```
3. Once paired, your Telegram User ID is saved as an authorized owner.

### Available Telegram Commands

| Command | Description |
|---|---|
| `/start` | Check bot status & active project |
| `/pair <code>` | Pair phone using single-use terminal code |
| `/projects` | List configured repositories |
| `/use <slug>` | Select active project workspace |
| `/status` | View running task status |
| `/doctor` | Run health checks directly from Telegram |
| `/help` | Show command overview |

Simply type any prompt in private chat with the bot to start a new coding task on your active project!

---

## ⚙️ Configuration Reference

Configuration is managed via `.env` (environment variables & tokens) and `config.yml` (app & security settings).

### `.env`
```dotenv
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
POCKETRELAY_LOG_LEVEL=INFO
```

### `config.yml`
```yaml
app:
  name: PocketRelay
  mode: local
  data_dir: ./data
  worktree_dir: ./data/worktrees
  max_concurrent_tasks: 1
  default_task_timeout_seconds: 900

telegram:
  transport: polling
  allowed_chat_types:
    - private
  max_prompt_length: 12000

security:
  require_pairing: true
  pairing_code_ttl_seconds: 300
  redact_secrets: true
  allow_raw_shell: false

projects:
  - slug: my-project
    display_name: My Project
    repository_path: C:/Projects/MyProject
    adapter: auto  # auto-detects agy, claude, etc.
    default_branch: main
    allowed_test_commands:
      - ["pytest"]
```

---

## 🐳 Docker Deployment

PocketRelay includes a production-ready, security-hardened Docker container running under a non-root system user.

```bash
docker-compose up -d
```

---

## 🛡️ Security Architecture

PocketRelay is built on deny-by-default security controls:

- **Path Traversal Guards**: Path validation prevents access outside designated workspace folders.
- **Cryptographic Nonce & Hash Checks**: Approval requests use `secrets.token_hex()` and full SHA-256 payload verification to prevent tampering.
- **Non-Root Execution**: Docker container isolates processes under a dedicated `pocketrelay` non-root user.
- **Strict File Permissions**: Automated setup locks down sensitive `.env` and `config.yml` files (`0o600`).

For security vulnerabilities reporting, please see [SECURITY.md](SECURITY.md).

---

## 📄 License & Terms

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
Please review our [TERMS_OF_USE.md](TERMS_OF_USE.md) and [PRIVACY.md](PRIVACY.md) for details regarding data privacy and usage guidelines.