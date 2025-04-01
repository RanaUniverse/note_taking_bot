"""
i will write help cmd code here
"""

import os

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode


from my_modules.logger_related import RanaLogger


GROUP_LINK = os.environ.get("GROUP_LINK", None)

if GROUP_LINK is None:
    raise ValueError("❌ GROUP_LINK is not present in .env file!")


async def help_cmd_old(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """This is when user will send /help"""

    if update.message is None or update.message.from_user is None:
        print("I used this to prevent the type hint of pyright. in help cmd")
        return

    user = update.message.from_user

    text = (
        f"<b>Hello {user.first_name.upper()},</b>\n"
        "I think you may need some help! 😊\n\n"
        "For more assistance, you can visit our website.\n"
        "Meanwhile, here is your account information:\n\n"
        f"🔹 <b>Full Name:</b> {user.full_name}\n"
        + (
            f"🔹 <b>Username:</b> @{user.username}\n"
            if user.username
            else "<b>🔹 Usernme:</b> N/A\n"
        )  # Only add if username exists
        + f"🔹 <b>User ID:</b> <code>{user.id}</code>\n"
        f"Thanks"
    )

    await context.bot.send_message(user.id, text, parse_mode=ParseMode.HTML)


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
        f"Hello if You need some help, You can Join Our Channel and then also contact "
        f"any admin for personal asking.\n"
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
        f"⚠️ <b>Sorry, this bot is not available for use in groups at the moment.</b>\n\n"
        f"💡 However, you can join our <b>Main Group</b> for discussions and support:\n"
        f"👉 <a href='https://t.me/{GROUP_LINK}'>Join Main Group</a>"
    )

    await update.effective_message.reply_html(text)
