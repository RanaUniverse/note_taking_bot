import logging
import os

from dotenv import load_dotenv


from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)


from my_modules.cmd_handler_modules.start_module import start_cmd
from my_modules.cmd_handler_modules.help_module import help_cmd

from my_modules.message_handler.text_msg_module import echo_text

load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# if BOT_TOKEN:
#     print("BotToken got ✅ This is come from the .env file")

# else:
#     BOT_TOKEN = "RanaUniverse🍌🍌🍌"  # type: ignore
#     print(".no .env file or env file has not any bot token.")


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    if BOT_TOKEN is None:
        print(
            ".no .env file or env file has not any bot token. Please make sure the token is there and rerun this program."
        )
        return

    application = Application.builder().token(BOT_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start_cmd))
    application.add_handler(CommandHandler("help", help_cmd))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_text))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
