"""
this module will contains the code for delete a note
i not think fully should i will delete the notes or i will keep those and mark as delete

"""

import html

from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from telegram.constants import ChatAction, ParseMode

from telegram.ext import ContextTypes

from my_modules import message_templates
from my_modules import inline_keyboard_buttons

from my_modules.message_templates import WhatMessageAction

from my_modules.logger_related import RanaLogger

from my_modules.database_code.database_make import engine

from my_modules.database_code import db_functions


async def delete_note_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    When user will send /delete_note without any args it will execute
    and it will say user to pass the correct note id and how to use.
    """

    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None:
        RanaLogger.warning(
            "User and MSG should be present when user send "
            "/delete_note without any args"
        )
        return None

    if not context.args:

        reply_text = (
            "⚠️ You didn't provide a note ID.\n\n"
            "To delete a specific note, please use:\n"
            "<code>/delete_note &lt;note_id&gt;</code>\n\n"
            "❓ Don't know your note ID?\n"
            "Use the buttons below to:\n"
            "• View all your notes\n"
            "• Search by keyword\n"
            "• Or delete all notes at once\n"
        )

        await msg.reply_html(
            text=reply_text,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard_buttons.NOTE_DELETE_KEYBOARD
            ),
        )

    else:
        RanaLogger.warning("This should not execute as i will use args value to 0")


async def delete_note_one_arg(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Assume the note_id has passed as context.args when this fun triggers
    When user will send /delete_note without any args it will execute
    and it will say user to pass the correct note id and how to use.
    """

    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None:
        RanaLogger.warning(
            "User and MSG should be present when user send "
            "/delete_note with one any args"
        )
        return None

    await msg.reply_chat_action(action=ChatAction.TYPING)

    if not context.args:
        # This part should not execute as this is must have 1 args
        # But i keep this to check and know how in any case it work
        RanaLogger.error(
            f"context.args should be present when /delete_note with 1 args has come."
        )
        text_error = (
            "⚠️ <b>Missing Note ID!</b>\n\n"
            "To delete a note, please provide its unique Note ID.\n"
            "Usage: <code>/delete_note &lt;note_id&gt;</code>\n\n"
            "You can also browse your notes(/my_notes) using the available "
            "options and find the Note ID easily. 📚\n"
            "This is a problem maybe plesse report to admin."
        )

        await msg.reply_html(text=text_error)
        return None

    note_id = context.args[0]
    RanaLogger.info(f"{user.full_name} want to delete the note id of: {note_id}")

    note_row = db_functions.note_obj_from_note_id(
        engine=engine,
        note_id=note_id,
    )

    if note_row is None:
        safe_note_id = html.escape(note_id)
        text = (
            f"🚫 The Note ID You provided (<code>{safe_note_id}</code>) "
            f"seems to be invalid.\n\n"
            f"{message_templates.NOTE_NO_FOUND_TEXT}"
        )
        await msg.reply_html(text=text)
        return None

    # Below Means Note row is present
    owner_id = note_row.user_id

    if user.id != owner_id:

        text = message_templates.access_denied_messages(
            user=user,
            what_action=WhatMessageAction.DELETE,
        )

        await msg.reply_html(text)
        return None

    # this line executes means the owner id of the note and the user is same
    # so it means the note can be delted now properly.

    deletion_confirmation = db_functions.delete_note_obj(
        engine=engine,
        note_id=note_id,
        user_id=owner_id,
    )

    if deletion_confirmation:
        note_del_confirm = f"{message_templates.SUCCESS_NOTE_DELETE_TEXT}"

        await msg.reply_html(note_del_confirm)
        return None

    else:
        RanaLogger.warning(
            f"delete fun has been run for note so it should be yes / no."
        )
        text = f"{message_templates.FAIL_NOTE_DELETE_TEXT}"

        await msg.reply_html(text)
        return None


async def delete_note_many_args(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Wehn user will send /delete_note arg1 arg2... argn
    it will just say user to send in correct format
    """

    user = update.effective_user
    msg = update.effective_message

    if msg is None or user is None:
        RanaLogger.warning(
            f"User send many args with /delete_note so msg and user should be present"
        )
        return None

    text_many_args = (
        f"⚠️ <b>Too Many Arguments!</b>\n\n"
        f"Hello {user.mention_html()}, you’ve sent more arguments than expected.\n\n"
        f"✅ <b>Correct Usage:</b>\n"
        f"<code>/delete_note &lt;note_id&gt;</code>\n\n"
        f"💡 Tip: Use /view_notes to find the correct Note ID before deleting."
    )

    await msg.reply_html(
        text=text_many_args,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard_buttons.NOTE_DELETE_KEYBOARD,
        ),
    )


async def handle_delete_note_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
        pattern = "delete_note_<note_id>"
    On this type of case i will use this function which will execute.
    It will ask The user for one confirmation to delete note.
    """
    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None:
        RanaLogger.warning(
            "When user press delete button of note it should "
            f"have the user and msg obj available"
        )
        return None

    query = update.callback_query
    if query is None or query.data is None:
        RanaLogger.warning("Delete Note button pressed but no callback data found.")
        return None

    note_id = query.data.replace("delete_note_", "")

    note_row = db_functions.note_obj_from_note_id(
        engine=engine,
        note_id=note_id,
    )
    if note_row is None:
        RanaLogger.warning(f"This time the note row should present")
        text_no_note = message_templates.NOTE_NO_FOUND_TEXT

        if msg.text:
            await query.edit_message_text(
                text=text_no_note,
                parse_mode=ParseMode.HTML,
            )

        elif msg.caption:
            await query.edit_message_caption(
                caption=text_no_note,
                parse_mode=ParseMode.HTML,
            )

        return None

    await query.answer(
        text="🗑️ Please Read all carefully must ⏳",
        show_alert=True,
    )
    reply_text = message_templates.generate_delete_confirmation_with_note_info_text(
        note_row=note_row,
    )

    buttons = inline_keyboard_buttons.generate_delete_note_confirmation_buttons(
        note_id=note_id
    )

    if msg.text:
        await query.edit_message_text(
            text=reply_text,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.HTML,
        )

    elif msg.caption:
        await query.edit_message_caption(
            caption=reply_text,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.HTML,
        )


async def confirm_note_del_button(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    `note_del_confirm_ <note_id>` :- This is callback data
    When user press the delete the note button for a note
    it will execute and del the note completely.
    """

    user = update.effective_user
    msg = update.effective_message
    if user is None or msg is None:
        RanaLogger.warning(
            "When user press Confirm delete button of note it should "
            f"have the user and msg obj available"
        )
        return None

    query = update.callback_query
    if query is None or query.data is None:
        RanaLogger.warning(
            "Confirm Delete Note button pressed but no callback data found."
        )
        return None
    # await query.answer("Your Request is in Processing ...")

    note_id = query.data.removeprefix("note_del_confirm_")

    waiting_text = (
        f"⏳ Deleting your note...\n"
        f"Please wait!\n\n"
        f"Your Request is in processing... \n\n"
        f"Note ID: <code>{note_id}</code>\n"
    )

    msg_waiting = await msg.reply_html(waiting_text, do_quote=True)

    RanaLogger.info(
        f"{user.full_name} want to delete the note id of: "
        f"{note_id} by pressing the confirm button attached with the note view"
    )

    note_row = db_functions.note_obj_from_note_id(
        engine=engine,
        note_id=note_id,
    )

    if note_row is None:
        RanaLogger.warning(f"Note id should be present when del confirm callback.")
        text_no_note = f"{waiting_text}\n\n" f"{message_templates.NOTE_NO_FOUND_TEXT}"

        button = [
            [
                InlineKeyboardButton(
                    text="Note Delete Failed 😢",
                    callback_data="note_delete_failed",
                )
            ]
        ]

        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(button))

        await msg_waiting.edit_text(text=text_no_note, parse_mode=ParseMode.HTML)

        return None

    delection_confirmation = db_functions.delete_note_obj(
        engine=engine,
        note_id=note_id,
        user_id=user.id,
    )

    # here i need to do serach note with note id, then i need to
    # check note owner and user id is same or not, if not then say
    # user specefically,otherwise it can be problem

    if delection_confirmation:
        text = f"{waiting_text}\n\n" f"{message_templates.SUCCESS_NOTE_DELETE_TEXT}"

        await msg_waiting.edit_text(text, parse_mode=ParseMode.HTML)

        button = [
            [
                InlineKeyboardButton(
                    text="Note Already Deleted 😭",
                    callback_data="note_deleted_already",
                )
            ]
        ]

        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(button))
        return None

    # else:

    #     RanaLogger.warning(
    #         f"When the note id is ok and user id is matched, then it should delete the note "
    #         "i dont understand maybe some inner problem is happening in db."
    #     )
    #     text = f"{waiting_text}\n\n" f"{message_templates.FAIL_NOTE_DELETE_TEXT}"

    #     await msg_waiting.edit_text(text, parse_mode=ParseMode.HTML)
    #     return None

    else:
        RanaLogger.warning(
            f"When the note id is ok and user id is matched, then it should delete the note "
            "i dont understand maybe some inner problem is happening in db."
        )
        text = f"{waiting_text}\n\n" f"{message_templates.FAIL_NOTE_DELETE_TEXT}"

        await msg_waiting.edit_text(text, parse_mode=ParseMode.HTML)

        button = [
            [
                InlineKeyboardButton(
                    text="Note Delete Failed 😢",
                    callback_data="note_delete_failed",
                )
            ]
        ]

        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(button))
        return None


async def note_del_cancel_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Callback Data: `note_delete_cancel`
    When user choose he dont want to delete his note this callback
    data will come and it will just say nothing now.
    """
    msg = update.effective_message
    user = update.effective_user

    if msg is None or user is None:
        RanaLogger.warning(
            f"When user choose not to delte his note in a button "
            "The note_delete_cancel data will should has the information of msg and user"
        )
        return None

    query = update.callback_query

    if query is None or query.data is None:
        RanaLogger.warning(
            f"When user choose not to delte his note by "
            "note_delete_cancel callback data must be present"
        )
        return None

    button = [
        [
            InlineKeyboardButton(
                text="Note Deletion Stopped 🚫",
                callback_data="note_delete_stopped",
            )
        ]
    ]

    # For now this will just remove the buttons when this is pressed
    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(button))


async def note_deletion_stopped_button(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Callback Data: note_delete_stopped
    When the user presses the "Note Deletion Stopped 🚫" button,
    show an alert that it was already cancelled.
    """
    query = update.callback_query

    if query is None or query.data is None:
        RanaLogger.warning(
            "note_delete_stopped button pressed but no callback data found."
        )
        return

    text = "Note Deletion Was Already Cancelled 🚫"
    await query.answer(
        text=text,
        show_alert=True,
    )


async def note_deleted_already_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Callback Data: note_deleted_already
    When user press the buttton it will just say it got deleted
    """
    query = update.callback_query

    if query is None or query.data is None:
        RanaLogger.warning(
            "already note deleted button pressed but no callback data found."
        )
        return

    text = f"Note Already Deleted 😁😁😁"
    await query.answer(
        text=text,
        show_alert=True,
    )


async def note_delete_failed_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Callback Data: note_delete_failed
    When user presses the button, it shows a failure message.
    """
    query = update.callback_query

    if query is None or query.data is None:
        RanaLogger.warning(
            "Note delete failed button pressed but no callback data found."
        )
        return

    await query.answer(
        text="Note Delete Failed 😢 Please try again Freshly!",
        show_alert=True,
    )


async def all_note_delete_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    When user want to delete all his note by pressing the button
    Callback Data: delete_my_all_notes
    """

    user = update.effective_user
    msg = update.effective_message
    if user is None or msg is None:
        RanaLogger.warning(
            f"When user want to delete all his note by pressing this button "
            f"so user and msg must present always"
        )
        return None

    query = update.callback_query
    if query is None or query.data is None:
        RanaLogger.warning(
            "When all note delete button pressed but no callback data found."
        )
        return None

    await query.answer(
        "I am trying to delete all of your notes.",
        show_alert=True,
    )

    # await query.edit_message_reply_markup()

    how_many_note_delete = db_functions.delete_all_notes_of_user(
        engine=engine,
        user_id=user.id,
    )

    if how_many_note_delete == 0:
        no_note_text = (
            "⚠️ No notes were deleted.\n\n"
            "👉 This could be because:\n"
            "- You have no notes.\n"
            "- Or there was a database issue on our server.\n\n"
            "Please try again later or contact support if the issue persists."
        )
        await query.edit_message_text(text=no_note_text)
        return None

    elif how_many_note_delete >= 1:
        some_note_deleted_text = (
            f"🗑️ Successfully deleted **{how_many_note_delete}** of your notes.\n"
            "✅ No more notes left to delete!"
        )
        await query.edit_message_text(text=some_note_deleted_text)
        return None
