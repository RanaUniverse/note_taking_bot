"""
This here i will keep some user register related commands
    1. /register_me

Some User related command will be here, for now register me
is single command not a converstaion so this is ok for now
"""

import random

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from telegram import Update
from telegram import InlineKeyboardMarkup
from telegram.ext import ContextTypes


from my_modules import bot_config_settings
from my_modules import message_templates

from my_modules.logger_related import RanaLogger

from my_modules.database_code import db_functions
from my_modules.database_code.database_make import engine
from my_modules.database_code.models_table import UserPart

from my_modules.some_constants import MessageEffectEmojies

from my_modules.some_inline_keyboards import MyInlineKeyboard


GOOD_EFFECTS = [
    MessageEffectEmojies.LIKE.value,
    MessageEffectEmojies.HEART.value,
    MessageEffectEmojies.TADA.value,
]

IST_TIMEZONE = bot_config_settings.IST_TIMEZONE
DEFAULT_REGISTER_TOKEN = bot_config_settings.DEFAULT_REGISTER_TOKEN


async def register_me_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /register_me :- For now it will just save.
    I want this will just register the user directly, without asking anythings extra
    as this is for now will just register now...
    """

    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None:
        RanaLogger.warning(
            f"When user will send /register_me it should have "
            f"exists the user and msg object"
        )
        return None

    # What my Logic: When user will send this, it will try to add his obj in user row, if it throw a unique error or like something then it will go to say to make new row.
    # Here i thought to use cache like logic so that all time my machine will not open db for check if the user is register or not

    user_obj = UserPart(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        points=DEFAULT_REGISTER_TOKEN,
        account_creation_time=msg.date.astimezone(IST_TIMEZONE),
    )

    try:
        with Session(engine) as session:
            session.add(user_obj)
            session.commit()
            session.refresh(user_obj)

        text_success = message_templates.user_register_success_text(
            tg_user_obj=user,
            db_user_obj=user_obj,
        )
        await msg.reply_html(
            text=text_success,
            reply_markup=InlineKeyboardMarkup(
                MyInlineKeyboard.ACCOUNT_NEW_REGISTER.value
            ),
            message_effect_id=random.choice(GOOD_EFFECTS),
        )

    except IntegrityError as _:
        RanaLogger.warning(
            f"{user.full_name} want to register him but it say integrity error, "
            f"it means he is maybe a user register already. "
        )
        user_row = db_functions.user_obj_from_user_id(engine=engine, user_id=user.id)

        if user_row is None:
            RanaLogger.warning(
                f"i got itegrity error of /register_me but i got integrity error "
                f"but i got the user_row as none, so it maybbe a real problem as user row if none, it means the integrity error should not be shows."
            )
            return None

        # This means the user is present in the database,
        # and i will fetch data from the user row below.
        text_user_exists = message_templates.user_already_register_text(
            tg_user_obj=user,
            db_user_obj=user_row,
            msg_obj=msg,
        )
        await msg.reply_html(
            text=text_user_exists,
            reply_markup=InlineKeyboardMarkup(
                MyInlineKeyboard.ACCOUNT_ALREADY_REGISTER.value
            ),
        )

    except Exception as e:
        RanaLogger.warning(
            f"When user send /register_me but got not entry in the new record "
            f"or maybe this not come into the integrity error, so "
            f"it maybe some database file related problem "
            f"i cannot think what is this. "
            f"Please see the below informaion:\n"
            f"{e}"
        )
        text_error = message_templates.user_register_unknown_error()
        await msg.reply_html(
            text=text_error,
            message_effect_id=MessageEffectEmojies.DISLIKE.value,
        )
