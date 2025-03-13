"""
i will write help cmd code here
"""

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """This is when user will send /help"""

    if update.message is None or update.message.from_user is None:
        print("I used this to prevent the type hint of pyright.")
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
