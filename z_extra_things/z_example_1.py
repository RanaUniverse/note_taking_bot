"""
No Use Of This Module ❌❌❌

This is i add some new thing to add.
This is checking how to work with conversation
"""

import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from telegram.constants import ParseMode

from dotenv import load_dotenv
import os

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO = range(4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [["Boy", "Girl", "Other"]]

    await update.message.reply_text(
        "Hi! My name is Professor Bot. I will hold a conversation with you. "
        "Send /cancel to stop talking to me.\n\n"
        "Are you a boy or a girl?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="Boy or Girl?",
        ),
    )

    return GENDER


async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "I see! Please send me a photo of yourself, "
        "so I know what you look like, or send /skip if you don't want to.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return PHOTO


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the photo and asks for a location."""
    user = update.message.from_user
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive("user_photo.jpg")
    logger.info("Photo of %s: %s", user.first_name, "user_photo.jpg")
    await update.message.reply_text(
        "Gorgeous! Now, send me your location please, or send /skip if you don't want to."
    )

    return LOCATION


async def skip_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the photo and asks for a location."""
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    await update.message.reply_text(
        "I bet you look great! Now, send me your location please, or send /skip."
    )

    return LOCATION


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the location and asks for some info about the user."""
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of %s: %f / %f",
        user.first_name,
        user_location.latitude,
        user_location.longitude,
    )
    await update.message.reply_text(
        "Maybe I can visit you sometime! At last, tell me something about yourself."
    )

    return BIO


async def skip_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the location and asks for info about the user."""
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    await update.message.reply_text(
        "You seem a bit paranoid! At last, tell me something about yourself."
    )

    return BIO


async def bio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text("Thank you! I hope we can talk again some day.")

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


async def str_checking_logic(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """This is just send same message to user with the"""

    if update.message is None or update.message.from_user is None:
        print("this should not happens.")
        return
    user = update.message.from_user

    text = "This has filters.all"
    await context.bot.send_message(user.id, text, ParseMode.HTML)


async def bad_for_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """When user need photo or /skip but user send anything else this exectue"""

    user = update.effective_chat
    text = f"You should only send a photo of urself or send /skip only."
    await context.bot.send_message(user.id, text)
    return PHOTO


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    load_dotenv()

    BOT_TOKEN = os.environ.get("BOT_TOKEN")

    if BOT_TOKEN is None:
        print(
            ".no .env file or env file has not any bot token. Please make sure the token is there and rerun this program."
        )
        return
    application = Application.builder().token(BOT_TOKEN).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler(
                "start",
                start,
            ),
            CommandHandler("help", start),  # Add /help as an entry point
            CommandHandler("now", start),  # Add /now as an entry point
        ],
        states={
            GENDER: [MessageHandler(filters.Regex("^(Boy|Girl|Other)$"), gender)],
            PHOTO: [
                MessageHandler(filters.PHOTO, photo),
                CommandHandler("skip", skip_photo),
                CommandHandler("cancel", cancel),  # Allow cancellation at this step
                MessageHandler(
                    filters.ALL,
                    bad_for_photo,
                ),
            ],
            LOCATION: [
                MessageHandler(filters.LOCATION, location),
                CommandHandler("skip", skip_location),
            ],
            BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,
        conversation_timeout=5,
    )

    application.add_handler(conv_handler)

    application.add_handler(
        MessageHandler(
            ~filters.TEXT,
            str_checking_logic,
        )
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
