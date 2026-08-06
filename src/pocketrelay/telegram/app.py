from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from pocketrelay.settings import config
from pocketrelay.telegram.handlers import (
    approval_callback_handler,
    doctor_handler,
    help_handler,
    pair_handler,
    projects_handler,
    prompt_handler,
    start_handler,
)


def build_application(token: str) -> Application:
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("pair", pair_handler))
    app.add_handler(CommandHandler("doctor", doctor_handler))
    app.add_handler(CommandHandler("help", help_handler))
    app.add_handler(CommandHandler("projects", projects_handler))
    app.add_handler(CallbackQueryHandler(approval_callback_handler))

    # Build chat-type filter from config
    chat_type_map = {
        "private": filters.ChatType.PRIVATE,
        "group": filters.ChatType.GROUPS,
        "supergroup": filters.ChatType.SUPERGROUP,
        "channel": filters.ChatType.CHANNEL,
    }
    chat_filter = None
    for ct in config.telegram.allowed_chat_types:
        f = chat_type_map.get(ct)
        if f:
            chat_filter = f if chat_filter is None else (chat_filter | f)

    base_filter = filters.TEXT & ~filters.COMMAND
    if chat_filter is not None:
        base_filter = base_filter & chat_filter

    app.add_handler(MessageHandler(base_filter, prompt_handler))

    return app


