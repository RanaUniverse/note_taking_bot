"""
i just need to run this
"""

from my_modules.cmd_handler_modules.zzz_extra_things import rana_checking

# This upper is just for checking different logics only.


from telegram import Update

from telegram.constants import MessageEntityType


from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from my_modules.admin_related_code import update_commands_cmd, show_bot_commands

from my_modules.callback_modules.start_cmd_buttons import button_for_start
from my_modules.callback_modules.some_buttons import update_profile_button

from my_modules.cmd_handler_modules import add_points_module
from my_modules.cmd_handler_modules import help_module
from my_modules.cmd_handler_modules import start_module
from my_modules.cmd_handler_modules import user_register
from my_modules.cmd_handler_modules.all_edited_command import handle_edited_command

from my_modules.conv_handlers_modules import account_register


# This should be a conversation but for now this is for no more things
from my_modules.conv_handlers_modules import new_note


from my_modules.database_code.database_make import create_db_and_engine


from my_modules.message_handlers_modules.text_msg_module import text_msg_to_txt_file
from my_modules.message_handlers_modules.z_text_related_module import email_find

# This upper two is just for checking string logics


from my_modules.notes_related import delete_note
from my_modules.notes_related import edit_note
from my_modules.notes_related import export_note
from my_modules.notes_related import fake_note_make
from my_modules.notes_related import search_notes

from my_modules.some_constants import PrivateValue


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.

    BOT_TOKEN = PrivateValue.BOT_TOKEN.value

    application = Application.builder().token(BOT_TOKEN).build()

    # Below is a conversation /register_me_manually in development
    application.add_handler(account_register.new_acc_conv)

    # New Note Making conv with button or /new_note will be below
    application.add_handler(new_note.new_note_conv)

    # Edit Note conv, a button or /edit_note
    application.add_handler(edit_note.edit_note_conv)

    # Below is for all the edited command
    application.add_handler(
        MessageHandler(
            filters=filters.Command()
            & filters.ChatType.PRIVATE
            & filters.UpdateType.EDITED_MESSAGE,
            callback=handle_edited_command,
            block=False,
        )
    )

    # This below two is for admin now experimental
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

    # Below rana checking is just a concepts for checking my logics
    application.add_handler(
        CommandHandler(
            command="rana",
            callback=rana_checking,
        )
    )

    # This below is seems a simple deep_link come from group i need to change logic
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

    # Below is user send simple start the bot in private chat from user.
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
            callback=help_module.help_cmd,
            filters=filters.ChatType.PRIVATE,
            block=False,
        )
    )

    application.add_handler(
        CommandHandler(
            command="help",
            callback=help_module.help_cmd_group,
            filters=filters.ChatType.GROUPS,
            block=False,
        )
    )

    application.add_handler(
        CommandHandler(
            command="register_me",
            callback=user_register.register_me_cmd,
            filters=filters.ChatType.PRIVATE & filters.UpdateType.MESSAGE,
        )
    )

    application.add_handler(
        CommandHandler(
            command=["add_points"],
            callback=add_points_module.add_points_cmd_no_arg,
            block=False,
            has_args=0,
        )
    )

    application.add_handler(
        CommandHandler(
            command=["add_points"],
            callback=add_points_module.add_points_cmd_one_arg,
            block=False,
            has_args=1,
        )
    )

    application.add_handler(
        CommandHandler(
            command=["add_points"],
            callback=add_points_module.add_points_cmd_many_args,
            block=False,
            has_args=None,
        )
    )

    # /fake_note integer value for make fake notes
    application.add_handler(
        CommandHandler(
            command=["fake_note"],
            callback=fake_note_make.fake_notes_many,
            filters=filters.ChatType.PRIVATE & filters.UpdateType.MESSAGE,
            block=False,
            has_args=1,
        )
    )

    # i twill just make one note and show user the note informaiton back to user
    application.add_handler(
        CommandHandler(
            command=["fake_note"],
            callback=fake_note_make.fake_note_cmd,
            filters=filters.ChatType.PRIVATE & filters.UpdateType.MESSAGE,
            block=False,
        )
    )

    # this will help to search all notes of a user
    application.add_handler(
        CommandHandler(
            command="my_notes",
            callback=search_notes.my_notes_cmd,
            filters=filters.ChatType.PRIVATE & filters.UpdateType.MESSAGE,
            block=False,
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            search_notes.handle_my_all_notes_callback,
            pattern="my_all_notes",
        )
    )

    application.add_handler(
        CommandHandler(
            command="delete_note",
            callback=delete_note.delete_note_one_arg,
            filters=filters.ChatType.PRIVATE & filters.UpdateType.MESSAGE,
            block=False,
            has_args=1,
        )
    )

    application.add_handler(
        CommandHandler(
            command="delete_note",
            callback=delete_note.delete_note_cmd,
            filters=filters.ChatType.PRIVATE & filters.UpdateType.MESSAGE,
            block=False,
            has_args=0,
        )
    )

    application.add_handler(
        CommandHandler(
            command="delete_note",
            callback=delete_note.delete_note_many_args,
            filters=filters.ChatType.PRIVATE & filters.UpdateType.MESSAGE,
            block=False,
            has_args=None,
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback=search_notes.handle_edit_note_button,
            pattern=r"^edit_note_.*$",
        )
    )

    # Below is asking user for a confirmation with a new button not conversation
    application.add_handler(
        CallbackQueryHandler(
            callback=search_notes.handle_delete_note_button,
            pattern=r"^delete_note_.*$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback=search_notes.confirm_note_del_button,
            pattern="^note_del_confirm_.*",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback=search_notes.note_deleted_already_button,
            pattern="note_deleted_already",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback=export_note.export_note_button,
            pattern="^export_note_.*$",
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

    application.add_handler(
        MessageHandler(
            filters=filters.Entity(
                entity_type=MessageEntityType.EMAIL,
            ),
            callback=email_find,
        )
    )

    application.add_handler(
        MessageHandler(
            filters=filters.TEXT & ~filters.COMMAND,
            callback=text_msg_to_txt_file,
            block=False,
        )
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    create_db_and_engine()
    main()
