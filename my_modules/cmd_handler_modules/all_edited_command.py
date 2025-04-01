"""
This module has the logic of how to handle edited command so that
it will not make any error and make it more good
"""

from telegram import Update
from telegram.ext import ContextTypes


async def handle_edited_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    This will execute when any command comes here edited condition
    """

    user = update.effective_user
    if user is None:
        print("This should be a user has")
        return

    text = "⚠️ Please don't edit a message to a command. Instead, send a fresh command."

    await context.bot.send_message(user.id, text)
