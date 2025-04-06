"""
i will write help cmd code here
"""

import os

from telegram import Update

from telegram.ext import ContextTypes

from my_modules.logger_related import RanaLogger


GROUP_LINK = os.environ.get("GROUP_LINK", None)

if GROUP_LINK is None:
    raise ValueError("❌ GROUP_LINK is not present in .env file!")


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
        f"Hello you are requesting for a help in the private chat with bot. "
        f"You can just start chat with the admin privately, the button for "
        f"admin contact will added soon."
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
