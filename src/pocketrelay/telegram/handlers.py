from telegram import Update
from telegram.ext import ContextTypes

from pocketrelay.settings import config
from pocketrelay.application.approval_service import approval_service
from pocketrelay.application.auth_service import auth_service
from pocketrelay.application.task_service import task_service
from pocketrelay.cli.doctor import format_doctor_report
from pocketrelay.security.pairing import pairing_manager


async def approval_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user = update.effective_user
    if not query or not user or not query.data:
        return

    await query.answer()

    if not auth_service.is_allowed(user.id):
        await query.edit_message_text("Access denied.")
        return

    data = query.data
    if data.startswith("approve:"):
        req_id = data.split(":")[1]
        req = approval_service.get_request(req_id)
        if not req:
            await query.edit_message_text("Approval request not found.")
            return

        if approval_service.consume_approval(req_id, user.id, req.payload_hash):
            await query.edit_message_text(f"✅ Approved commit for Task {req.task_id}!")
        else:
            await query.edit_message_text(f"❌ Failed to approve Task {req.task_id} (expired or invalid).")

    elif data.startswith("reject:"):
        req_id = data.split(":")[1]
        req = approval_service.get_request(req_id)
        if req and approval_service.reject_approval(req_id, user.id):
            await query.edit_message_text(f"🚫 Rejected changes for Task {req.task_id}.")
        else:
            await query.edit_message_text("Request already processed or expired.")

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    user = update.effective_user
    if user is None:
        return

    if not auth_service.is_allowed(user.id):
        if update.effective_message:
            await update.effective_message.reply_text("Access denied. Send /pair <code> to pair your phone.")
        return

    if update.effective_message:
        await update.effective_message.reply_text(
            "PocketRelay is active.\n"
            "Use /projects to select a project."
        )

async def pair_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    msg = update.effective_message
    if user is None or msg is None:
        return

    if not context.args:
        await msg.reply_text("Usage: /pair <code>\nExample: /pair 834921")
        return

    code = context.args[0]
    if pairing_manager.verify_code(code):
        auth_service.add_owner(user.id)
        await msg.reply_text(f"Pairing successful! Telegram User ID {user.id} has been paired as an owner.")
    else:
        await msg.reply_text("Invalid or expired pairing code. Please check your terminal or run setup again.")

async def doctor_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    msg = update.effective_message
    if user and auth_service.is_allowed(user.id) and msg:
        report = format_doctor_report()
        await msg.reply_text(report)

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user is None or not auth_service.is_allowed(user.id):
        return
    if update.effective_message:
        await update.effective_message.reply_text(
            "Commands:\n"
            "/start - Start bot\n"
            "/pair <code> - Pair your Telegram ID using code from terminal\n"
            "/doctor - Run system health diagnostics\n"
            "/help - Show help\n"
            "/projects - List projects\n"
            "/use - Select a project\n"
            "/status - Check task status\n"
        )

async def projects_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user and auth_service.is_allowed(user.id) and update.effective_message:
        from pocketrelay.application.project_service import project_service
        projects = project_service.get_projects()
        if not projects:
            await update.effective_message.reply_text("No projects found.")
            return
        project_list = "\n".join([f"- {p.display_name} (slug: {p.slug})" for p in projects])
        await update.effective_message.reply_text(f"Available projects:\n{project_list}\n\nUse /use <slug> to select one.")

async def prompt_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    user = update.effective_user

    if message is None or user is None or not message.text:
        return

    if not auth_service.is_allowed(user.id):
        return

    if len(message.text) > config.telegram.max_prompt_length:
        await message.reply_text(
            f"Prompt too long ({len(message.text)} chars). "
            f"Maximum allowed: {config.telegram.max_prompt_length}"
        )
        return

    task = await task_service.create_from_prompt(
        user_id=user.id,
        chat_id=message.chat_id,
        prompt=message.text,
    )

    await message.reply_text(f"Task {task.id} received. Status: {task.status.value}")

