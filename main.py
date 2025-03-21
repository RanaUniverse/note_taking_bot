import os

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from telegram.constants import MessageEntityType

# Below is for checking my string logic
from my_modules.message_handlers_modules.z_checking_msg import (
    str_checking_logic,
    filters_all,
)

from my_modules.cmd_handler_modules.start_module import start_cmd
from my_modules.cmd_handler_modules.help_module import help_cmd

from my_modules.conv_handlers_modules.example_1 import conv_example_1
from my_modules.conv_handlers_modules.new_account import conv_new_account

from my_modules.message_handlers_modules.text_msg_module import echo_text
from my_modules.message_handlers_modules.z_text_related_module import email_find


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

    # on different commands - answer in Telegram

    application.add_handler(conv_example_1)
    application.add_handler(conv_new_account)

    application.add_handler(CommandHandler("start", start_cmd))
    application.add_handler(CommandHandler("help", help_cmd))

    application.add_handler(
        MessageHandler(
            filters=filters.Entity(entity_type=MessageEntityType.EMAIL),
            callback=email_find,
        )
    )
    application.add_handler(MessageHandler(filters.ALL, filters_all))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_text))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, str_checking_logic)
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
