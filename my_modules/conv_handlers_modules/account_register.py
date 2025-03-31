"""
This module has the conversation part for asking user about his information
and save his data in the UserPart table.
Mostly: /new_account or /register_me


This module is for making new handler for conversation
Will Delete, You are going to register yourself in this
successfully, you can add new notes

Here will the code for users can activate their account
information and then their account will be activated.


And the bot will ask about some infomations one by one until user satisfy with this.

"""

import datetime
import os
import random


from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select


from telegram import InlineKeyboardMarkup
from telegram import Update
from telegram.ext import ContextTypes

from telegram.ext import filters

from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
)

from telegram.constants import ParseMode

from my_modules.database_code.database_make import engine
from my_modules.database_code.models_table import UserPart

from my_modules.logger_related import logger, RanaLogger
from my_modules.some_constants import MessageEffectEmojies

from my_modules.some_inline_keyboards import MyInlineKeyboard


DEFAULT_REG_TOKEN_STR = os.environ.get("DEFAULT_REG_TOKEN", None)

if not DEFAULT_REG_TOKEN_STR:
    raise ValueError("❌ DEFAULT_REG_TOKEN not found in .env file!")

try:
    DEFAULT_REG_TOKEN = int(DEFAULT_REG_TOKEN_STR)  # Convert to int

except ValueError:
    raise ValueError("❌ DEFAULT_REG_TOKEN must be a valid integer!")


IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))


EMAIL, PHONE, REFERRAL, CONFIRMATION, UNKNOWN_ERROR = range(5)

GOOD_EFFECTS = [
    MessageEffectEmojies.LIKE.value,
    MessageEffectEmojies.HEART.value,
    MessageEffectEmojies.TADA.value,
]


# Now what i though this command is not need to be in the conversatin, rather the
# button attached with this return Message need to be in the entry_points and
# then use the conversationn with this.


async def user_register_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    If User will press /register or /register_me it will execute which
    need to ask users some question and save some of his information.

    """

    user = update.effective_user

    if user is None or update.message is None:
        RanaLogger.warning(f"Some Error Happens Now it should not happens")
        return ConversationHandler.END

    user_row = UserPart(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        account_creation_time=update.message.date.astimezone(IST),
        points=DEFAULT_REG_TOKEN,
    )

    try:
        with Session(engine) as session:
            session.add(user_row)
            session.commit()
            session.refresh(user_row)

        text = (
            f"🎉 Hello, <b>{user.mention_html()}</b>! 🎉\n\n"
            f"✅ You have successfully registered with <b>{user_row.points} Tokens</b> 🪙.\n\n"
            f"📋 To Manually Add More Information You can:\n"
            f"   🔹 Use the Buttons below ⬇️\n"
            f"   🔹 Or type the appropriate Commands ⌨️\n\n"
            f"🚀 Let's get started!"
        )
        await context.bot.send_message(
            chat_id=user.id,
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                MyInlineKeyboard.ACCOUNT_NEW_REGISTER.value
            ),
            message_effect_id=random.choice(GOOD_EFFECTS),
        )
        return ConversationHandler.END  # NEED TO CHANGE

    except IntegrityError as e:
        RanaLogger.warning(e)

        # It means some column value has same, it maybe the userid column, i dont sure for this till now, maybe i need to refactor this code later.
        with Session(engine) as session:
            statement = select(UserPart).where(UserPart.user_id == user.id)
            results = session.exec(statement)
            user_row = results.first()

        if user_row is None:
            RanaLogger.error(
                f"As the user row is none, so userid is not need to same, this need to check explicitely in future."
            )
            return ConversationHandler.END

        # Below lines means user row is present, and user is already there in the database.

        text = (
            "⚠️ <b>You are already registered!</b> ⚠️\n\n"
            "✅ No need to register again. Simply use this bot and explore its features! 🚀"
            f"You have total {user_row.points} tokens."
        )
        await context.bot.send_message(
            chat_id=user.id,
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                MyInlineKeyboard.ACCOUNT_ALREADY_REGISTER.value,
            ),
        )

        return ConversationHandler.END  # NEED TO CHANGE

    except Exception as e:
        RanaLogger.warning(f"I didn't thought about this error type, this looks new.")

        text = f"Somethings Unexpected Happens, Pls Contact admin, /help or /admin"
        await context.bot.send_message(user.id, text)
        return ConversationHandler.END  # NEED TO CHANGE


async def add_email_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    This will execute when the add email button is pressed by user
    and it will ask user to send his email id, and if this match then it will go nowhere
    """

    if update.callback_query is None:
        print("This should not execute, as always this has query")
        return ConversationHandler.END

    query = update.callback_query
    user = query.from_user

    await context.bot.answer_callback_query(
        callback_query_id=query.id,
    )
    text = (
        f"Hello <b>{user.first_name}</b> Please write Your Email Address and Send me 👇"
    )
    await context.bot.send_message(
        chat_id=user.id,
        text=text,
        parse_mode=ParseMode.HTML,
    )

    return EMAIL


async def any_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    When any button will presss this will execute, for now this not made yet
    """
    if update.callback_query is None:
        print("This should not execute, as always this has query")
        return ConversationHandler.END

    query = update.callback_query
    user = query.from_user

    await context.bot.answer_callback_query(
        callback_query_id=query.id,
        text=f"This button has not implimented yet 😢. Please use commands.",
        show_alert=True,
    )
    text = (
        f"/<b>add_email</b> :- To add your email address\n\n"
        f"/<b>add_phone</b> :- To add your phone number\n\n"
        f"/<b>referral_code</b> :- To add a code for any offers.\n\n"
        f"/<b>terminate</b> :- If you dont want to proceed and exit account making.\n\n"
        f"/<b>save_now</b> :- Add all your current information now.\n\n"
        f"/<b>help</b> :- To see others things and got help.\n"
    )

    await context.bot.send_message(
        chat_id=user.id,
        text=text,
        parse_mode=ParseMode.HTML,
    )

    return EMAIL


async def email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message is None or update.message.from_user is None:
        print("This should not execute.")
        return ConversationHandler.END

    user = update.message.from_user
    email_id = update.message.text

    if context.user_data is None:
        return ConversationHandler.END

    context.user_data["email"] = email_id

    logger.info("Email of %s: %s", user.first_name, email_id)

    text = (
        f"Got it! Now, please enter your phone number, or type "
        "/skip if you prefer not to provide it."
    )

    await context.bot.send_message(
        chat_id=user.id,
        text=text,
        parse_mode=ParseMode.HTML,
    )
    return PHONE


async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message is None or update.message.from_user is None:
        print("This should not execute.")

        return ConversationHandler.END

    user = update.message.from_user
    phone_no = update.message.text

    if context.user_data is None:
        return ConversationHandler.END

    context.user_data["phone"] = phone_no
    text = f"Thanks! If you have a referral code, enter it now, or type /skip."
    await context.bot.send_message(
        chat_id=user.id,
        text=text,
        parse_mode=ParseMode.HTML,
    )
    return CONFIRMATION


async def skip_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    if update.message is None or update.message.from_user is None:
        print("This should not execute.")

        return ConversationHandler.END

    user = update.message.from_user

    if context.user_data is None:
        return ConversationHandler.END

    context.user_data["phone"] = None
    text = f"Hello you have not enter your phone no. thanks"

    await context.bot.send_message(
        chat_id=user.id,
        text=text,
        parse_mode=ParseMode.HTML,
    )
    return CONFIRMATION


async def confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    if update.message is None or update.message.from_user is None:
        print("This should not execute.")

        return ConversationHandler.END

    user = update.message.from_user

    text = f"Thanks for confirmation of your account"

    await context.bot.send_message(
        chat_id=user.id,
        text=text,
        parse_mode=ParseMode.HTML,
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    if update.message is None or update.message.from_user is None:
        print("This should not execute.")

        return ConversationHandler.END

    user = update.message.from_user
    text = f"Thanks for cancel now"
    await context.bot.send_message(
        chat_id=user.id,
        text=text,
        parse_mode=ParseMode.HTML,
    )
    return ConversationHandler.END


async def not_need_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """This will come to execute which i dont need"""
    if update.message is None or update.message.from_user is None:
        print("This shouldn't execute")
        return ConversationHandler.END

    user = update.message.from_user

    await context.bot.send_message(user.id, f"This has nothing to do bye")
    return ConversationHandler.END


account_register_conv_handler = ConversationHandler(
    entry_points=[

        # This has now only command handler like beheaviour
        CommandHandler(
            command=[
                "register",
                "register_me",
                "r",
            ],
            callback=user_register_cmd,
            filters=filters.ChatType.PRIVATE & filters.UpdateType.MESSAGE,
            block=False,
        )
    ],
    states={
        EMAIL: [
            CallbackQueryHandler(
                callback=any_button,
                pattern=None,
                block=False,
            ),
            MessageHandler(
                filters=filters.TEXT & ~filters.COMMAND,
                callback=email,
                block=False,
            ),
        ],
        PHONE: [
            MessageHandler(
                filters=filters.TEXT & ~filters.COMMAND,
                callback=phone,
                block=False,
            ),
            CommandHandler(
                command="skip",
                callback=skip_phone,
                block=False,
            ),
        ],
        CONFIRMATION: [
            MessageHandler(
                filters=filters.Regex("^(Yes|No)$"),
                callback=confirmation,
                block=False,
            )
        ],
        UNKNOWN_ERROR: [
            MessageHandler(
                filters=filters.ALL,
                callback=not_need_text,
                block=False,
            ),
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    allow_reentry=True,
)
