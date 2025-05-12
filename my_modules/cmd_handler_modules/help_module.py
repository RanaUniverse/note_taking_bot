"""
i will write help cmd code here
"""

from telegram import Update

from telegram.ext import ContextTypes

from my_modules.logger_related import RanaLogger
from my_modules.some_constants import BotSettingsValue


GROUP_LINK = BotSettingsValue.GROUP_LINK.value


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    When user send help command in private chat,
    """

    user = update.effective_user

    if user is None:
        RanaLogger.warning("This user need to be there")
        return

    if update.effective_message is None:
        RanaLogger.warning(f"Message need to be there.")
        return

    text = (
        "🤖 <b>Bot Help Guide</b>\n\n"
        "Hello! 👋\n\n"
        "I'm here to assist you. Here's what you can do:\n\n"
        "• <b>/start</b> – Initiate a conversation with the bot.\n"
        "• <b>/help</b> – Display this help message.\n"
        "• <b>/contact</b> – Reach out to the administrator for further assistance.\n\n"
        "Feel free to explore and let me know if you need any help!"
    )
    await update.effective_message.reply_html(text)


async def help_cmd_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    When user sends /help in a group chat, inform them that the bot is not available for group use.
    """

    user = update.effective_user

    if user is None:
        RanaLogger.warning("This user needs to be present for group /help.")
        return

    if update.effective_message is None:
        RanaLogger.warning("Message is required for group /help.")
        return

    text = (
        f"You have send /help in a group message publically to others. "
        f"⚠️ <b>Sorry, this bot is not available for use in groups at the moment.</b>\n\n"
        f"💡 However, you can join our <b>Main Group</b> for discussions and support:\n"
        f"👉 <a href='https://t.me/{GROUP_LINK}'>Join Main Group</a>"
    )

    await update.effective_message.reply_html(text)
