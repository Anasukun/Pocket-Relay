import argparse
import asyncio
import sys

import structlog

from pocketrelay.application.task_service import worker
from pocketrelay.cli.doctor import format_doctor_report
from pocketrelay.cli.init_wizard import run_init_wizard
from pocketrelay.settings import settings
from pocketrelay.telegram.app import build_application

logger = structlog.get_logger()

async def async_main() -> None:
    logger.info("Starting PocketRelay", mode="local")
    
    if not settings.telegram_bot_token:
        print("Error: TELEGRAM_BOT_TOKEN is not set in environment or .env file.")
        print("Please run 'pocketrelay init' to launch the setup wizard.")
        sys.exit(1)

    app = build_application(settings.telegram_bot_token)
    
    worker_task = asyncio.create_task(worker())
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    logger.info("PocketRelay is polling for Telegram updates.")
    
    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        logger.info("Shutting down...")
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()
        worker_task.cancel()

def main() -> None:
    parser = argparse.ArgumentParser(prog="pocketrelay", description="PocketRelay CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("init", help="Run guided non-technical setup wizard")
    subparsers.add_parser("doctor", help="Run system diagnostics check")
    subparsers.add_parser("run", help="Start the PocketRelay worker process")

    args = parser.parse_args()

    if args.command == "init":
        run_init_wizard()
    elif args.command == "doctor":
        print(format_doctor_report())
    else:
        try:
            asyncio.run(async_main())
        except KeyboardInterrupt:
            print("\nExiting.")

if __name__ == "__main__":
    main()

