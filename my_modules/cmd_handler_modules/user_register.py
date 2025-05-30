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


from my_modules.logger_related import RanaLogger

from my_modules.database_code import db_functions
from my_modules.database_code.database_make import engine
from my_modules.database_code.models_table import UserPart

from my_modules.some_constants import IST_TIMEZONE
from my_modules.some_constants import BotSettingsValue
from my_modules.some_constants import MessageEffectEmojies

from my_modules.some_inline_keyboards import MyInlineKeyboard


GOOD_EFFECTS = [
    MessageEffectEmojies.LIKE.value,
    MessageEffectEmojies.HEART.value,
    MessageEffectEmojies.TADA.value,
]


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
        points=BotSettingsValue.DEFAULT_REGISTER_TOKEN.value,
        account_creation_time=msg.date.astimezone(IST_TIMEZONE),
    )

    try:
        with Session(engine) as session:
            session.add(user_obj)
            session.commit()
            session.refresh(user_obj)

        text_success = (
            f"🎉 Hello, <b>{user.mention_html()}</b>! 🎉\n\n"
            f"✅ You have successfully registered with <b>{user_obj.points} "
            f"Tokens as Welcome Bonus</b> 🪙.\n\n"
            f"📋 To Manually Add More Information You can:\n"
            f"   🔹 Use the Buttons below ⬇️\n"
            f"   🔹 Or type the appropriate Commands ⌨️\n\n"
            f"🚀 Let's get started!"
            f"\n\n"
            f"For Now The Buttons is not working as this is not "
            f"developed yet will come later."
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
                f"but i got the user_row as none, so it maybbe a real problem as usrrow if none, it means the integrity error should not be shows."
            )
            return None

        # This means the user is present in the database

        time_formatting = f"%Y-%m-%d"
        old_register_time = user_row.account_creation_time.strftime(time_formatting)

        text_user_exists = (
            f"⚠️ Hello <b>{user.mention_html()}, you are already registered!</b>⚠️"
            f"\n\n"
            "✅ No need to register again. Simply use this bot and explore its features! 🚀"
            f"\n\n"
            f"Your Information: \n"
            f"Already Account Creation Time: {old_register_time}"
            f"\n"
            f"You have total {user_row.points} tokens."
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
        text_error = (
            f"Its seems some problem in the side of database, "
            f"Please contact a adming or /help"
        )
        await msg.reply_html(
            text=text_error,
            message_effect_id=MessageEffectEmojies.DISLIKE.value,
        )
