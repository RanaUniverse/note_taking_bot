'''
i tried to make a quote from the original message using the same formatiing
but till now i am not able to achieve this
'''

import os
from telegram.constants import ParseMode
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)


from telegram.ext import ContextTypes
from telegram import ReplyParameters
from telegram import MessageEntity
from telegram.constants import MessageEntityType


async def check_msg_sending(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    "just for checking how different message send works"

    if update.message is None or update.message.from_user is None:
        return

    if update.message.text is None:
        return

    user = update.message.from_user
    user_msg = update.message.text

    quote_text = user_msg[0 : len(user_msg) // 2]

    entities = MessageEntity(
        type=update.message.entities[0].type,
        offset=0,
        length=len(user_msg) // 2,
    )
    quote_part = ReplyParameters(
        update.message.message_id,
        allow_sending_without_reply=True,
        quote=quote_text,
        quote_entities=[entities],
    )

    text = f"This is a text to return user {user.full_name}"
    await context.bot.send_message(
        user.id,
        text,
        reply_parameters=quote_part,
    )


async def reply_to_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    This will execute to reply to the email address user will send
    """
    print("This is executing.")
    if update.message is None or update.message.from_user is None:
        return

    if update.message.text is None:
        return

    user = update.message.from_user
    user_msg = update.message.text

    for entity in update.message.entities:
        if entity.type == MessageEntityType.EMAIL:
            # i want first email will work and then exit
            email_start = entity.offset
            email_end = email_start + entity.length
            user_email = user_msg[email_start:email_end]
            break






    if not user_email:
        return

    quote_text = user_email

    reply_parameters = ReplyParameters(
        update.message.message_id,
        allow_sending_without_reply=True,
        quote=quote_text,
        quote_parse_mode=ParseMode.HTML,
    )

    text = f"Hello sir, your email is: \n\n <blockquote>{user_email}</blockquote>"
    await context.bot.send_message(
        user.id,
        text,
        parse_mode=ParseMode.HTML,
        reply_parameters=reply_parameters,
    )


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    load_dotenv()

    BOT_TOKEN = os.environ.get("BOT_TOKEN")

    if BOT_TOKEN is None:
        print(
            ".no .env file or env file has not any bot token. Please make sure the token is there and re run this program."
        )
        return

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", check_msg_sending))

    application.add_handler(
        MessageHandler(filters.Entity(MessageEntityType.EMAIL), reply_to_email)
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
