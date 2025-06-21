"""
No Use Of This Module ❌❌❌

this will help me to check some logics
"""

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


from my_modules import message_templates

from my_modules.database_code import db_functions
from my_modules.database_code.database_make import engine
from my_modules.logger_related import RanaLogger


async def rana_checking_old(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """This is for checking purpose only"""

    if update.message is None or update.message.from_user is None:
        print("I used this to prevent the type hint of pyright. in ranachecking")
        return

    user = update.message.from_user
    text = f"Please send me a text now,"
    await context.bot.send_message(
        chat_id=user.id,
        text=text,
        parse_mode=ParseMode.HTML,
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


async def my_account_details_cmd(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    When user want to get his account details by the command this will executes
    """

    user = update.effective_user
    msg = update.effective_message
    if msg is None or user is None:
        RanaLogger.warning(
            f"user msg should be present when account details button pressed"
        )
        return None

    user_row = db_functions.user_obj_from_user_id(engine, user.id)

    if user_row is None:
        no_register_text = message_templates.prompt_user_to_register(user)
        await msg.reply_html(text=no_register_text)
        return None

    user_info_text = message_templates.user_complete_details_text(
        tg_user_obj=user,
        user_row=user_row,
    )
    await msg.reply_html(text=user_info_text)
