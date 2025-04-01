"""
Here i will check some text logic to know how i am going on
"""

from telegram import Update

from telegram.ext import ContextTypes
from telegram.constants import MessageEntityType


async def email_find_old(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    I am trying to find the email id from user message
    """

    if (
        update.message is None
        or update.message.from_user is None
        or update.message.text is None
    ):
        print("I used this to prevent the type hint of pyright.")
        return

    user = update.message.from_user
    user_msg = update.message.text

    email_1_start = update.message.entities[0].offset
    email_1_end = email_1_start + update.message.entities[0].length
    first_email = user_msg[email_1_start:email_1_end]

    email_2_start = update.message.entities[1].offset
    email_2_end = email_2_start + update.message.entities[0].length
    second_email = user_msg[email_2_start:email_2_end]

    text = f"The total Emails are:\n\n" f"{first_email} \n\n" f"{second_email} \n\n"
    print(update)
    await context.bot.send_message(user.id, text=text)


async def email_find(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    This functions is not usable, this is not used yet

    I am trying to find the email id from user message
    this fun will execute where filters = filters.EMAIL in text like this
    """

    if (
        update.message is None
        or update.message.from_user is None
        or update.message.text is None
    ):
        print("I used this to prevent the type hint of pyright.")
        return

    user = update.message.from_user
    user_msg = update.message.text
    emails: list[str] = []

    for entity in update.message.entities:
        if entity.type == MessageEntityType.EMAIL:
            email_start = entity.offset
            email_end = email_start + entity.length
            emails.append(user_msg[email_start:email_end])

    if emails:

        email_count = len(emails)
        text = (
            f"You have send me {email_count} Email Addresses, which are:\n\n"
            "The extracted email addresses are:\n\n" + "\n".join(emails)
        )

    else:
        print("This should not execute")
        text = "No email addresses found! 😕"

    await context.bot.send_message(user.id, text=text)
