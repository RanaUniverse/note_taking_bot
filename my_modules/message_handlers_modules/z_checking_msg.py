"""
This module is for checking my differetn logic
"""

from pydantic import (
    BaseModel,
    EmailStr,
    ValidationError,
)


from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode


class EmailValidator(BaseModel):
    email: EmailStr


async def str_checking_logic(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """This is just send same message to user with the"""

    if (
        update.message is None
        or update.message.from_user is None
        or update.message.text is None
    ):
        print("I used this to prevent the type hint of pyright.")
        return
    user = update.message.from_user
    user_msg = update.message.text

    try:
        validated_email = EmailValidator(email=user_msg)
        email = validated_email.email
        text = f"✅ Valid email: \n\n<b>{email}</b>"
        await context.bot.send_message(user.id, text, ParseMode.HTML)

    except ValidationError as e:
        text = f"{e}"
        await context.bot.send_message(user.id, text, ParseMode.HTML)


async def checking_filters(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    i will just differet filters logic here in this function
    just to know how to use different filters
    """

    user = update.message.from_user

    text = f"Thanks i got ur message of custom filters,\n\n" f"<b>{user.full_name}</b>"

    await context.bot.send_message(user.id, text, ParseMode.HTML)


async def filters_all(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    this fun will execute when filters.ALL is used"
    """

    text = (
        f"Thanks i got ur message which do filters.ALL,\n\n"
        f"<b>{update.message.from_user.full_name}</b>"
        f"{update}"
    )
    await context.bot.send_message(update.message.from_user.id, text)
