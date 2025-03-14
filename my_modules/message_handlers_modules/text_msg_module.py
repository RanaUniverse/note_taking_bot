"""
This python code is for just checking, though this not need, maybe i will use echo just for nothing
"""

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode


async def echo_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """This is just send same message to user with the"""

    if (
        update.message is None
        or update.message.from_user is None
        or update.message.text is None
    ):
        print("I used this to prevent the type hint of pyright.")
        return
    user = update.message.from_user
    user_text = update.message.text

    text_100 = f"{user_text.upper()[0:100]} ..."
    text = (
        f"Hello {user.first_name} You have send me the text of {len(user_text)} character, whose first max 100 character is below: \n\n"
        f"<blockquote>{text_100}</blockquote>"
    )

    await context.bot.send_message(user.id, text, ParseMode.HTML)

