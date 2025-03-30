"""
this will help me to check some logics
"""

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


async def rana_checking_old(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """This is for checking purpose only"""

    if update.message is None or update.message.from_user is None:
        print("I used this to prevent the type hint of pyright. in ranachecking")
        return
    from telegram import ReplyKeyboardMarkup
    from my_modules.some_reply_keyboards import yes_no_reply_keyboard

    user = update.message.from_user
    text = f"Please send me a text now,"
    await context.bot.send_message(
        chat_id=user.id,
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=ReplyKeyboardMarkup(
            yes_no_reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="yes not button here.",
        ),
    )


async def rana_checking_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """This is for checking purpose only"""

    if update.message is None or update.message.from_user is None:
        print("I used this to prevent the type hint of pyright. in ranachecking")
        return

    user = update.message.from_user
    text = f"Please send me a text now,"

    await context.bot.send_message(
        chat_id=user.id,
        text=text,
    )


async def rana_checking(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """This is for checking purpose only"""

    if update.message is None:
        print("just to warning remove of the below pylance")
        return

    text = f"Please send me a texts"

    await update.message.reply_text(text=text, do_quote=True)
