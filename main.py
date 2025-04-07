"""
i just need to run this
"""

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

# Below is for checking my string logic

from my_modules.cmd_handler_modules import start_module
from my_modules.cmd_handler_modules.help_module import help_cmd, help_cmd_group

from my_modules.conv_handlers_modules.account_register import (
    account_register_conv_handler,
)

from my_modules.message_handlers_modules.z_text_related_module import email_find

from my_modules.database_code.database_make import create_db_and_engine

from my_modules.cmd_handler_modules.zzz_extra_things import rana_checking
from my_modules.cmd_handler_modules.add_points import add_points_cmd


from my_modules.callback_modules.start_cmd_buttons import button_for_start
from my_modules.callback_modules.some_buttons import update_profile_button

from my_modules.notes_related import search_notes

from my_modules.notes_related import fake_note_make

from my_modules.admin_related_code import update_commands_cmd, show_bot_commands

GROUP_LINK = os.environ.get("GROUP_LINK", None)

if GROUP_LINK is None:
    raise ValueError("❌ GROUP_LINK is not present in .env file!")


from telegram import Update
from telegram.ext import ContextTypes


async def echo_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """for testing how message will come to user"""

    user = update.effective_user
    msg = update.effective_message
    if user is None or msg is None:
        return

    text = msg.text_html
    print(text)
    await msg.reply_html(f"{text}")


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

    # This is first user register conversation this need

    from my_modules.conv_handlers_modules import new_note

    # This will start making a note, when user send "/new_note"
    application.add_handler(new_note.new_note_conv_handler)

    application.add_handler(account_register_conv_handler)

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
    from my_modules.cmd_handler_modules.all_edited_command import handle_edited_command

    application.add_handler(
        MessageHandler(
            filters=filters.Command()
            & filters.ChatType.PRIVATE
            & filters.UpdateType.EDITED_MESSAGE,
            callback=handle_edited_command,
            block=False,
        )
    )

    # this was just for a testing very warning code is update_commands
    # this is just for testing how to use command handle when bot is
    # running from the admin commands and admin update

    application.add_handler(
        CommandHandler(
            command=["update_commands"],
            callback=update_commands_cmd,
            block=False,
        )
    )
    application.add_handler(
        CommandHandler(
            command=["show_commands"],
            callback=show_bot_commands,
            block=False,
        )
    )

    # Below is when user press a button in gropup and this automaticaly
    # send a deep link to the bot in private chat. i need to keep this at before others

    application.add_handler(
        CommandHandler(
            command="start",
            callback=start_module.start_cmd_from_group_to_private,
            filters=filters.ChatType.PRIVATE & filters.UpdateType.MESSAGE,
            block=False,
            has_args=1,
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

    # Below is user start the bot in private chat from user.
    application.add_handler(
        CommandHandler(
            command="start",
            callback=start_module.start_cmd,
            filters=filters.ChatType.PRIVATE & filters.UpdateType.MESSAGE,
            block=False,
        )
    )

    application.add_handler(
        CommandHandler(
            command="help",
            callback=help_cmd,
            filters=filters.ChatType.PRIVATE,
            block=False,
        )
    )

    application.add_handler(
        CommandHandler(
            command="help",
            callback=help_cmd_group,
            filters=filters.ChatType.GROUPS,
            block=False,
        )
    )

    # This is for user has a ability to make some fake note in this account it
    # need to specefy how many notes he wants to make in this account
    # /fake_note 10
    application.add_handler(
        CommandHandler(
            command=[
                "f",
                "fake_note",
                "generate_fake_note",
                "new_fake_note",
            ],
            callback=fake_note_make.fake_notes_many,
            filters=filters.ChatType.PRIVATE & filters.UpdateType.MESSAGE,
            block=False,
            has_args=1,
        )
    )

    # i twill just make one note and show user the note informaiton back to user
    application.add_handler(
        CommandHandler(
            command=[
                "f",
                "fake_note",
                "generate_fake_note",
                "new_fake_note",
            ],
            callback=fake_note_make.fake_note_cmd,
            filters=filters.ChatType.PRIVATE & filters.UpdateType.MESSAGE,
            block=False,
        )
    )

    # this will help to search all notes of a user
    application.add_handler(
        CommandHandler(
            command=[
                "all_notes",
                "my_notes",
                "n",
            ],
            callback=search_notes.all_notes_cmd,
            filters=filters.ChatType.PRIVATE & filters.UpdateType.MESSAGE,
            block=False,
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback=search_notes.handle_edit_note_button,
            pattern=r"^edit_note_.*$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback=search_notes.handle_delete_note_button,
            pattern=r"^delete_note_.*$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback=search_notes.handle_transfer_note_button,
            pattern=r"^transfer_note_.*$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback=search_notes.handle_duplicate_note_button,
            pattern=r"^duplicate_note_.*$",
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
            callback=new_note.new_note_button_press,
            pattern="new_note",
            block=False,
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback=button_for_start,
            pattern="^(new_note|view_notes|edit_note|search_note|delete_note|export_notes|help_section)$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback=search_notes.button_for_next_page,
            pattern=r"^notes_page_\d+$",
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            callback=search_notes.button_for_no_more_notes_last_page,
            pattern="no_more_notes_end_page",
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            callback=search_notes.button_for_no_more_notes,
            pattern=r"^no_more_notes_\d+$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback=search_notes.button_for_search_notes,
            pattern=None,
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
        MessageHandler(
            filters=filters.Entity(
                entity_type=MessageEntityType.EMAIL,
            ),
            callback=email_find,
        )
    )
    # application.add_handler(MessageHandler(filters.ALL, filters_all))

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            echo_text,
        )
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    create_db_and_engine()
    main()
