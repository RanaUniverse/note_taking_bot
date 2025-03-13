"""
This module is for making new handler for conversation to make new account
"""

from telegram import Update

from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    # MessageHandler,
    ContextTypes,
)

from telegram.constants import ParseMode


EMAIL, OTP, PASSWORD, PASSWORD_AGAIN, CONFIRMATION = range(5)


async def new_account_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    This will start message shows to user on when they
    start the new account making conversation.
    Assume this fun will run when user want to create a new account.
    """
    if update.message is None or update.message.from_user is None:
        return 100

    user = update.message.from_user
    text = (
        f"Hello <b>{user.first_name}</b>"
        f"Thanks for your interest to make new account here.\n\n"
        f"Send your email address to verify and start making new account."
    )
    await context.bot.send_message(user.id, text, ParseMode.HTML)

    return EMAIL


async def close_this_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """This will execute when user want to stop this making for now."""
    if update.message is None or update.message.from_user is None:
        return 100

    user = update.message.from_user
    text = (
        f"Hello <b>{user.full_name}</b>, "
        f"This time you are leaving this converstaion, "
        f"You can start this converstaion again with "
        f"/new, /new_account, /register "
        f"anytime you want to create a new accout here."
    )
    await context.bot.send_message(user.id, text, ParseMode.HTML)

    return ConversationHandler.END


conv_new_account = ConversationHandler(
    entry_points=[
        CommandHandler("new", new_account_start),
        CommandHandler("new_account", new_account_start),
        CommandHandler("register", new_account_start),
    ],
    states={},
    fallbacks=[
        CommandHandler("cancel", close_this_chat),
        CommandHandler("abord_setup", close_this_chat),
        CommandHandler("start_later", close_this_chat),
    ],
)
