"""
This here i will keep some user register related commands
    1. /register_me

Some User related command will be here, for now register me
is single command not a converstaion so this is ok for now
"""

import asyncio
import random

from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import OperationalError

from sqlmodel import Session, select

from telegram import Update
from telegram import InlineKeyboardMarkup

from telegram.constants import ChatAction, ParseMode
from telegram.ext import ContextTypes


from my_modules import bot_config_settings
from my_modules import inline_keyboard_buttons
from my_modules import message_templates

from my_modules.logger_related import RanaLogger

from my_modules.database_code import db_functions
from my_modules.database_code.database_make import engine
from my_modules.database_code.models_table import UserPart


MessageEffectEmojies = bot_config_settings.MessageEffectEmojies


GOOD_EFFECTS = [
    MessageEffectEmojies.LIKE.value,
    MessageEffectEmojies.HEART.value,
    MessageEffectEmojies.TADA.value,
]

IST_TIMEZONE = bot_config_settings.IST_TIMEZONE
DEFAULT_REGISTER_TOKEN = bot_config_settings.DEFAULT_REGISTER_TOKEN
REGISTER_ACCOUNT_WAIT_TIME = bot_config_settings.REGISTER_ACCOUNT_WAIT_TIME


async def register_me_cmd_old(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    ❌❌❌ Not for using
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
            db_user_row=user_obj,
        )
        await msg.reply_html(
            text=text_success,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard_buttons.USER_NEW_REGISTER_KEYBOARD
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
            db_user_row=user_row,
            msg_obj=msg,
        )
        await msg.reply_html(
            text=text_user_exists,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard_buttons.USER_ALREADY_REGISTER_KEYBOARD
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


async def register_me_cmd_confused_old_2(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    ❌❌❌ Not Using Now
    I Got Confused To Use This functions, so i am making new fun for this
    This is just a practise register me to check how to handle database
    insert of user row in my table.
    """

    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None:
        RanaLogger.warning(
            f"When user will send /register_me it should have "
            f"exists the user and msg object"
        )
        return None

    with Session(engine) as session:
        statement = select(UserPart).where(UserPart.user_id == user.id)
        result = session.exec(statement)
        existing_user = result.first()

        # This existing_user gives give None if not present user already

        if not existing_user:
            user_obj = UserPart(
                user_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                points=DEFAULT_REGISTER_TOKEN,
                account_creation_time=msg.date.astimezone(IST_TIMEZONE),
            )

            try:
                session.add(user_obj)
                session.commit()
                text = message_templates.user_register_success_text(
                    tg_user_obj=user,
                    db_user_row=user_obj,
                )
                await msg.reply_html(text)

            except OperationalError as e:
                RanaLogger.warning("Operation error which describe as \n" f"{e}")
                text = f"Database is locaked please try after a minute"
                await msg.reply_html(text)

            except Exception as e:
                RanaLogger.error(f"Error while registering user {user.id}: {e}")
                await msg.reply_text(
                    "An error occurred during registration. Please try again later."
                )
                return None

        else:
            # Means existing_user is note equal's to None, it is must UserPart Row value present
            text = message_templates.user_already_register_text(
                tg_user_obj=user,
                db_user_row=existing_user,
                msg_obj=msg,
            )
            await msg.reply_html(text)


async def register_me_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /register_me
    This function will execute,i though this register will run
    always user start my bot i will think about this later time.
    """
    msg = update.effective_message
    user = update.effective_user

    if msg is None or user is None:
        RanaLogger.warning("On /register_me The msg and user must present")
        return None

    user_present = db_functions.user_obj_from_user_id(
        engine=engine,
        user_id=user.id,
    )

    if user_present:
        text_user_already = message_templates.user_already_register_text(
            tg_user_obj=user,
            db_user_row=user_present,
            msg_obj=msg,
        )
        await msg.reply_html(text_user_already)
        return None

    # It means user is not present so i need to add him in database
    text = f"I am Registering You in our system. please wait."
    response_msg = await msg.reply_html(text)
    await msg.reply_chat_action(action=ChatAction.TYPING)
    await asyncio.sleep(REGISTER_ACCOUNT_WAIT_TIME)

    user_obj = UserPart(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        points=DEFAULT_REGISTER_TOKEN,
    )

    after_insert_user_obj = db_functions.add_new_user_to_user_table(engine, user_obj)

    text_new_user_create = message_templates.user_register_success_text(
        tg_user_obj=user,
        db_user_row=after_insert_user_obj,
    )

    await response_msg.edit_text(text_new_user_create, parse_mode=ParseMode.HTML)
