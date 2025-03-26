"""
This module has the conversation part for asking user about his information
and save his data in the UserPart table.
Mostly: /new_account or /register_me

And the bot will ask about some infomations one by one until user satisfy with this.

"""

import random

from telegram import Update

from telegram.ext import ContextTypes

from telegram.ext import filters

from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler,
)

from telegram import InlineKeyboardMarkup

from telegram.constants import ParseMode


from my_modules.some_constants import MessageEffectEmojies
from my_modules.logger_related import logger


from my_modules.some_inline_keyboards import keyboard_account_register


EMAIL, PHONE, REFERRAL, CONFIRMATION, UNKNOWN_ERROR = range(5)

GOOD_EFFECTS = [
    MessageEffectEmojies.LIKE.value,
    MessageEffectEmojies.HEART.value,
    MessageEffectEmojies.TADA.value,
]


async def new_account_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    This will start the account activate for a user
    """
    if update.message is None or update.message.from_user is None:
        print("This should not execute.")
        return ConversationHandler.END

    user = update.message.from_user

    text = (
        f"Hello {user.first_name}, You are going to register yourself in the bot. "
        f"After you will register successfully, you can add new notes here. "
        f"Please make sure you have kept your Email Address, Phone Number."
        f"After you will send all Press the 'confirmation' button or send /finish_now"
    )

    await context.bot.send_message(
        chat_id=user.id,
        text=text,
        parse_mode=ParseMode.HTML,
        message_effect_id=random.choice(GOOD_EFFECTS),
        reply_markup=InlineKeyboardMarkup(keyboard_account_register),
    )

    return EMAIL


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
        CommandHandler(
            command=[
                "new_account",
                "register_me",
            ],
            callback=new_account_cmd,
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
