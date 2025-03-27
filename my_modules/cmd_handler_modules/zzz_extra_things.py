"""
this will help me to check some logics
"""

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


async def rana_checking(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """This is for checking purpose only"""

    if update.message is None or update.message.from_user is None:
        print("I used this to prevent the type hint of pyright.")
        return

    user = update.message.from_user

    user_mention = f'<a href="tg://user?id={user.id}">{user.full_name}</a>'

    print(context.user_data)

    if context.user_data is None:
        print("user data value is None")
        return

    context.user_data.setdefault("total_messages", 0)

    context.user_data["a's"] = "A is a astring"

    context.user_data["B's"] = "B is a astring"

    text = f"{context.user_data}"

    await context.bot.send_message(
        chat_id=user.id,
        text=text,
        parse_mode=ParseMode.HTML,
    )

    context.user_data.clear()
    context.user_data["C's"] = "C is a astring"

    text = (
        f"<b>{user_mention}</b> below is ur information👇🏻👇🏻👇🏻"
        f"{context.user_data}"
    )

    await context.bot.send_message(
        chat_id=user.id,
        text=text,
        parse_mode=ParseMode.HTML,
    )
