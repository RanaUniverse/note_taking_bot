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

from my_modules.cmd_handler_modules.start_module import start_cmd
from my_modules.cmd_handler_modules.help_module import help_cmd
from my_modules.cmd_handler_modules.user_register import new_acc_register

from my_modules.conv_handlers_modules.account_register import (
    account_register_conv_handler,
)


from my_modules.message_handlers_modules.text_msg_module import echo_text
from my_modules.message_handlers_modules.z_text_related_module import email_find

from my_modules.message_handlers_modules.z_checking_msg import (
    str_checking_logic,
    filters_all,
)


from my_modules.database_code.database_make import create_db_and_engine


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

    # application.add_handler(conv_example_1)
    # application.add_handler(conv_new_account)

    application.add_handler(
        account_register_conv_handler,
    )

    from my_modules.conv_handlers_modules.note_making import conv_new_note

    application.add_handler(conv_new_note)

    from my_modules.cmd_handler_modules.zzz_extra_things import rana_checking

    application.add_handler(
        CommandHandler(
            "rana",
            rana_checking,
        )
    )
    application.add_handler(
        CommandHandler(
            "start",
            start_cmd,
        )
    )

    application.add_handler(
        CommandHandler(
            command=["register_me", "new_account", "register"],
            callback=new_acc_register,
            block=False,
        )
    )

    from my_modules.conv_handlers_modules.note_making import new_note_cmd

    application.add_handler(
        CommandHandler(
            command=["new_note"],
            callback=new_note_cmd,
            block=False,
        )
    )

    application.add_handler(
        CommandHandler(
            "help",
            help_cmd,
        )
    )
    application.add_handler(
        MessageHandler(
            filters=filters.Entity(
                entity_type=MessageEntityType.EMAIL,
            ),
            callback=email_find,
        )
    )
    application.add_handler(MessageHandler(filters.ALL, filters_all))

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            echo_text,
        )
    )
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            str_checking_logic,
        )
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    create_db_and_engine()
    main()
