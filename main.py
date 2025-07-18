"""
i just need to run this
"""

from telegram import Update

from telegram.constants import MessageEntityType


from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from my_modules import admin_related_code
from my_modules import bot_config_settings
from my_modules import inline_keyboard_buttons

from my_modules.callback_modules.start_cmd_buttons import button_for_start
from my_modules.callback_modules import some_buttons

from my_modules.cmd_handler_modules import add_points_module
from my_modules.cmd_handler_modules import ai_answer_module
from my_modules.cmd_handler_modules import help_module
from my_modules.cmd_handler_modules import start_module
from my_modules.cmd_handler_modules import user_register
from my_modules.cmd_handler_modules import zzz_extra_things
from my_modules.cmd_handler_modules.all_edited_command import handle_edited_command

from my_modules.conv_handlers_modules import account_register


# This should be a conversation but for now this is for no more things
from my_modules.conv_handlers_modules import new_note


from my_modules.database_code.database_make import create_db_and_engine


from my_modules.message_handlers_modules import text_msg_module
from my_modules.message_handlers_modules.z_text_related_module import email_find

# This upper two is just for checking string logics

from my_modules.notes_related import delete_note
from my_modules.notes_related import edit_note
from my_modules.notes_related import export_note
from my_modules.notes_related import fake_note_make
from my_modules.notes_related import view_notes


ACCOUNT_DETAILS_BUTTON = inline_keyboard_buttons.ACCOUNT_DETAILS_BUTTON
REFRESH_ACCOUNT_DETAILS = inline_keyboard_buttons.REFRESH_ACCOUNT_DETAILS
UPGRADE_PRO_BUTTON = inline_keyboard_buttons.UPGRADE_PRO_BUTTON
SETTINGS_BUTTON = inline_keyboard_buttons.SETTINGS_BUTTON
FEEDBACK_BUTTON = inline_keyboard_buttons.FEEDBACK_BUTTON
VIEW_ALL_NOTE_BUTTON = inline_keyboard_buttons.VIEW_ALL_NOTE_BUTTON
VIEW_ONE_NOTE_DYNAMIC_BUTTON = inline_keyboard_buttons.VIEW_ONE_NOTE_DYNAMIC_BUTTON
FAKE_NOTE_MAKING_BUTTON = inline_keyboard_buttons.FAKE_NOTE_MAKING_BUTTON


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.

    BOT_TOKEN = bot_config_settings.BOT_TOKEN

    application = Application.builder().token(BOT_TOKEN).build()

    # Below is a conversation /register_me_manually in development
    application.add_handler(account_register.new_acc_conv)

    # New Note Making conv with button or /new_note will be below
    # The new note making button is also in others places so it should be
    # keep like first so that other handler don't override those.
    application.add_handler(new_note.new_note_conv)

    # Edit Note conv, a button or /edit_note, also edit note attached
    # button which are attacged with the view note will now be come here.
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
            callback=admin_related_code.update_commands_cmd,
            block=False,
        )
    )
    application.add_handler(
        CommandHandler(
            command=["show_commands"],
            callback=admin_related_code.show_bot_commands,
            block=False,
        )
    )
    application.add_handler(
        CommandHandler(
            command=["get_logger_file"],
            callback=admin_related_code.get_logger_file,
            block=False,
        )
    )
    application.add_handler(
        CommandHandler(
            command=["get_database_file"],
            callback=admin_related_code.get_database_file,
            block=False,
        )
    )

    # Below rana checking is just a concepts for checking my logics
    application.add_handler(
        CommandHandler(
            command="rana",
            callback=admin_related_code.rana_checking,
        )
    )

    # Below Handler i am just doing checkin now later i will replaced those in good places

    application.add_handler(
        CallbackQueryHandler(
            callback=some_buttons.account_details_of_user_button_handler,
            pattern=f"{ACCOUNT_DETAILS_BUTTON.callback_data}",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback=some_buttons.refresh_account_details_button_handler,
            pattern=f"{REFRESH_ACCOUNT_DETAILS.callback_data}",
        )
    )

    application.add_handler(
        CommandHandler(
            command="my_account_details",
            callback=zzz_extra_things.my_account_details_cmd,
            filters=filters.ChatType.PRIVATE & filters.UpdateType.MESSAGE,
            block=False,
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback=some_buttons.upgrade_to_pro_member_button_handler,
            pattern=f"{UPGRADE_PRO_BUTTON.callback_data}",
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            callback=some_buttons.settings_button_pressed_handler,
            pattern=f"{SETTINGS_BUTTON.callback_data}",
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            callback=some_buttons.feedback_button_pressed_handler,
            pattern=f"{FEEDBACK_BUTTON.callback_data}",
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
            command="ai",
            callback=ai_answer_module.ai_cmd_but_no_args,
            filters=filters.ChatType.PRIVATE,
            block=False,
            has_args=0,
        )
    )

    application.add_handler(
        CommandHandler(
            command="ai",
            callback=ai_answer_module.ai_response_cmd,
            filters=filters.ChatType.PRIVATE,
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
    # /fake_note will make one fake note and shows this note.
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
            callback=view_notes.my_notes_cmd,
            filters=filters.ChatType.PRIVATE & filters.UpdateType.MESSAGE,
            block=False,
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback=fake_note_make.fake_note_making_by_button,
            pattern=rf"{FAKE_NOTE_MAKING_BUTTON.callback_data}",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            view_notes.handle_my_all_notes_callback,
            pattern=rf"{VIEW_ALL_NOTE_BUTTON.callback_data}*",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback=view_notes.button_for_view_one_note,
            # pattern=r"^view_note_.*$",
            pattern=rf"^{VIEW_ONE_NOTE_DYNAMIC_BUTTON.callback_data}.*$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback=view_notes.button_for_next_page,
            pattern=r"^next_page_.*",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback=view_notes.button_for_no_more_notes,
            pattern=r"^no_more_notes_\d+$",
        )
    )

    # Below is asking user for a confirmation with a new button not conversation
    application.add_handler(
        CallbackQueryHandler(
            callback=delete_note.handle_delete_note_button,
            pattern=r"^delete_note_.*$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback=delete_note.confirm_note_del_button,
            pattern=r"^note_del_confirm_.*",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback=delete_note.note_del_cancel_button,
            pattern="note_delete_cancel",
        )
    )

    # After a note del successfull, this is just a button
    application.add_handler(
        CallbackQueryHandler(
            callback=delete_note.note_deleted_already_button,
            pattern="note_deleted_already",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback=delete_note.note_delete_failed_button,
            pattern="note_delete_failed",
        )
    )

    # This is when user has cancel his note deletion will shows this
    application.add_handler(
        CallbackQueryHandler(
            callback=delete_note.note_deletion_stopped_button,
            pattern="note_delete_stopped",
        )
    )

    # This is currently think not fully understandable
    application.add_handler(
        CallbackQueryHandler(
            callback=delete_note.all_note_delete_button,
            pattern="delete_my_all_notes",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback=export_note.export_note_as_txt_file,
            pattern=r"^export_note_txt_.*$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback=export_note.export_note_as_pdf_file,
            pattern=r"^export_note_pdf_.*$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback=export_note.share_note_coming_soon,
            pattern=r"^share_note_.*$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback=export_note.duplicate_note_coming_soon,
            pattern=r"^duplicate_note_.*$",
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
            callback=some_buttons.new_note_button_handler,
            pattern=r"^(view|export|delete|share)_",
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
            callback=view_notes.handle_transfer_note_button,
            pattern=r"^transfer_note_.*$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback=view_notes.handle_duplicate_note_button,
            pattern=r"^duplicate_note_.*$",
        )
    )

    # i have separate this one button for now just for checking
    application.add_handler(
        CallbackQueryHandler(
            callback=some_buttons.update_profile_button,
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
            callback=text_msg_module.text_msg_come_from_private,
            block=False,
        )
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    create_db_and_engine()
    main()
