from telegram import Update
from telegram.ext import ContextTypes


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """When user will send /start this should execute"""

    if update.message is None or update.message.from_user is None:
        print("I used this to prevent the type hint of pyright.")
        return

    user = update.message.from_user
    text = f"Thanks {user.first_name.upper()} For starting this bot"
    await context.bot.send_message(user.id, text)
