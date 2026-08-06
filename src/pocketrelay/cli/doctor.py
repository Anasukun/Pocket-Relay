import shutil
import sys

from pocketrelay.settings import config, settings


def run_doctor_checks() -> dict[str, str]:
    results = {}
    
    # 1. Python version
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    results["Python Version"] = f"OK ({py_ver})" if sys.version_info >= (3, 12) else f"WARNING (Recommended >= 3.12, got {py_ver})"
    
    # 2. Telegram Bot Token
    if settings.telegram_bot_token:
        results["Telegram Token"] = "OK (Configured)"
    else:
        results["Telegram Token"] = "MISSING (Set TELEGRAM_BOT_TOKEN in .env)"
        
    # 3. Owner IDs
    if config.telegram.owner_ids:
        results["Paired Owner IDs"] = f"OK ({len(config.telegram.owner_ids)} owners paired)"
    else:
        results["Paired Owner IDs"] = "WARNING (No owners paired yet. Run setup wizard or pair via Telegram)"

    # 4. Git binary
    git_path = shutil.which("git")
    if git_path:
        results["Git CLI"] = f"OK ({git_path})"
    else:
        results["Git CLI"] = "MISSING (Install Git to support workspace isolation)"

    # 5. Agent CLI detection
    agy_path = shutil.which("agy")
    claude_path = shutil.which("claude")
    detected_agents = []
    if agy_path:
        detected_agents.append(f"Antigravity CLI ({agy_path})")
    if claude_path:
        detected_agents.append(f"Claude Code ({claude_path})")
        
    if detected_agents:
        results["Agent CLI Detection"] = f"OK ({', '.join(detected_agents)})"
    else:
        results["Agent CLI Detection"] = "WARNING (No agent CLI like 'agy' or 'claude' found in PATH. Using fake adapter for testing.)"

    # 6. Database directory
    db_dir = settings.pocketrelay_database_path.parent
    try:
        db_dir.mkdir(parents=True, exist_ok=True)
        results["Database Directory"] = f"OK (Writable at {db_dir.resolve()})"
    except Exception as e:  # noqa: BLE001
        results["Database Directory"] = f"ERROR (Cannot write to {db_dir}: {e})"


    return results

def format_doctor_report() -> str:
    checks = run_doctor_checks()
    lines = ["=== PocketRelay System Doctor ==="]
    for check, status in checks.items():
        lines.append(f"• {check}: {status}")
    return "\n".join(lines)
