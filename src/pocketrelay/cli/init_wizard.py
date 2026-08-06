import shutil
from pathlib import Path
import os
import stat

import yaml

from pocketrelay.cli.doctor import format_doctor_report
from pocketrelay.security.pairing import pairing_manager


def run_init_wizard() -> None:
    print("==================================================")
    print("       Welcome to PocketRelay Setup Wizard        ")
    print("==================================================")
    print("This wizard will help you set up PocketRelay without needing")
    print("to manually edit configuration files or code.\n")

    # Step 1: Telegram Bot Token
    token = input("1. Enter your Telegram Bot Token (from @BotFather): ").strip()
    while not token:
        token = input("Token cannot be empty. Enter Telegram Bot Token: ").strip()

    # Step 2: Agent Detection
    print("\n2. Detecting installed coding agents...")
    agy_path = shutil.which("agy")
    claude_path = shutil.which("claude")
    
    selected_adapter = "fake"
    if agy_path:
        print(f"   [✓] Found Google Antigravity CLI at: {agy_path}")
        selected_adapter = "antigravity-cli"
    elif claude_path:
        print(f"   [✓] Found Claude Code CLI at: {claude_path}")
        selected_adapter = "claude-code"
    else:
        print("   [!] No coding agent CLI detected in PATH. Defaulting to 'fake' testing adapter.")

    # Step 3: Project setup
    default_proj_path = Path.cwd().resolve()
    print("\n3. Select repository/project directory.")
    proj_path_input = input(f"   Enter folder path [default: {default_proj_path}]: ").strip()
    proj_path = Path(proj_path_input) if proj_path_input else default_proj_path

    proj_name = input("   Enter project display name [default: My First Project]: ").strip() or "My First Project"
    proj_slug = "my-project"

    # Step 4: Write .env
    env_content = f"TELEGRAM_BOT_TOKEN={token}\nPOCKETRELAY_LOG_LEVEL=INFO\n"
    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_content)
    os.chmod(".env", stat.S_IRUSR | stat.S_IWUSR)  # 0o600 - owner read/write only
    print("\n[✓] Saved '.env' file successfully.")

    # Step 5: Write config.yml
    config_dict = {
        "app": {
            "name": "PocketRelay",
            "mode": "local",
            "data_dir": "./data",
            "worktree_dir": "./data/worktrees",
            "max_concurrent_tasks": 1,
            "default_task_timeout_seconds": 900,
            "telemetry_enabled": False,
        },
        "telegram": {
            "transport": "polling",
            "owner_ids": [],
            "allowed_chat_types": ["private"],
            "reject_unknown_users": True,
            "max_prompt_length": 12000,
        },
        "security": {
            "require_pairing": True,
            "pairing_code_ttl_seconds": 300,
            "redact_secrets": True,
        },
        "projects": [
            {
                "slug": proj_slug,
                "display_name": proj_name,
                "repository_path": str(proj_path.resolve()),
                "adapter": selected_adapter,
                "default_branch": "main",
                "allowed_test_commands": [["pytest"]],
            }
        ],
    }

    with open("config.yml", "w", encoding="utf-8") as f:
        yaml.dump(config_dict, f, default_flow_style=False)
    os.chmod("config.yml", stat.S_IRUSR | stat.S_IWUSR)  # 0o600 - owner read/write only
    print("[✓] Saved 'config.yml' file successfully.")

    # Step 6: Generate Pairing Code
    code = pairing_manager.generate_code()
    print("\n==================================================")
    print("               Pairing Instructions               ")
    print("==================================================")
    print("To pair your phone with PocketRelay:")
    print("1. Open Telegram on your phone.")
    print("2. Search for your Bot.")
    print(f"3. Send this message to your Bot: /pair {code}")
    print("   (This code expires in 5 minutes)")
    print("==================================================\n")

    print(format_doctor_report())
    print("\nSetup complete! Run 'pocketrelay run' to start PocketRelay.")
