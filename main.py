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
from telegram.ext import CallbackQueryHandler
from telegram.ext import ContextTypes

# Below is for checking my string logic

from my_modules.cmd_handler_modules import start_module
from my_modules.cmd_handler_modules.help_module import help_cmd
from my_modules.cmd_handler_modules.user_register import new_acc_register

from my_modules.conv_handlers_modules.account_register import (
    account_register_conv_handler,
)


from my_modules.message_handlers_modules.z_text_related_module import email_find


from my_modules.database_code.database_make import create_db_and_engine


from my_modules.conv_handlers_modules.note_making import conv_new_note
from my_modules.cmd_handler_modules.zzz_extra_things import rana_checking
from my_modules.cmd_handler_modules.add_points import add_points_cmd


from my_modules.callback_modules.start_cmd_buttons import button_for_start
from my_modules.callback_modules.some_buttons import update_profile_button


async def handle_edited_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    This will execute when any command comes here edited condition
    """

    user = update.effective_user
    if user is None:
        print("This should be a user has")
        return

    text = "⚠️ Please don't edit a message to a command. Instead, send a fresh command."

    await context.bot.send_message(user.id, text)


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


    # application.add_handler(conv_example_1)
    # application.add_handler(conv_new_account)

    application.add_handler(account_register_conv_handler)

    application.add_handler(conv_new_note)

    application.add_handler(
        CommandHandler(
            "rana",
            rana_checking,
        )
    )

    application.add_handler(
        CommandHandler(
            command=["add_points", "add_point"],
            callback=add_points_cmd,
            block=False,
        )
    )

    # This below is for when user send any edited command, i
    # keep it as firs so that i don't need to worry about edited messag in any place

    application.add_handler(
        MessageHandler(
            filters=filters.Command()
            & filters.ChatType.PRIVATE
            & filters.UpdateType.EDITED_MESSAGE,
            callback=handle_edited_command,
            block=False,
        )
    )

    # Below is user start the bot in private chat from user.
    application.add_handler(
        CommandHandler(
            command="start",
            callback=start_module.start_cmd,
            filters=filters.ChatType.PRIVATE & filters.UpdateType.MESSAGE,
            block=False,
        )
    )

    # Below start is comes from any group
    application.add_handler(
        CommandHandler(
            command="start",
            callback=start_module.start_cmd_group,
            filters=filters.ChatType.GROUPS & filters.UpdateType.MESSAGE,
            block=False,
        )
    )

    # i have separate this one button for now just for checking
    application.add_handler(
        CallbackQueryHandler(
            callback=update_profile_button,
            pattern="^update_profile$",
        )
    )

    ## for this will handle the buttons having this callback data, for now
    # i kept all at once maybe it need to separate each to different functions for easy works
    application.add_handler(
        CallbackQueryHandler(
            callback=button_for_start,
            pattern="^(new_note|view_notes|edit_note|search_note|delete_note|export_notes|help_section)$",
        )
    )

    application.add_handler(
        CommandHandler(
            command="register",
            callback=new_acc_register,
            block=False,
        )
    )

    # This below will be come in conversation handler,

    # application.add_handler(
    #     CommandHandler(
    #         command="new_note",
    #         callback=new_note_cmd,
    #         block=False,
    #     )
    # )

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
    # application.add_handler(MessageHandler(filters.ALL, filters_all))

    # application.add_handler(
    #     MessageHandler(
    #         filters.TEXT & ~filters.COMMAND,
    #         echo_text,
    #     )
    # )

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    create_db_and_engine()
    main()
