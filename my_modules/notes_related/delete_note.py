"""
this module will contains the code for delete a note
i not think fully should i will delete the notes or i will keep those and mark as delete

"""

import html

from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from telegram.constants import ChatAction

from telegram.ext import ContextTypes

from my_modules.logger_related import RanaLogger

from my_modules.database_code.database_make import engine

# from my_modules.database_code.models_table import NotePart
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

    print(context.args)

    if not context.args:
        keyboard = [
            [
                InlineKeyboardButton("View All Notes", callback_data="my_all_notes"),
                InlineKeyboardButton("Help", callback_data="help"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await msg.reply_html(
            "⚠️ <b>Missing Note ID!</b>\n\n"
            "To delete a note, please provide its unique Note ID.\n"
            "Usage: <code>/delete_note &lt;note_id&gt;</code>\n\n"
            # "Usage: <code>/delete_note <note_id> </code>\n\n"
            "You can also view your saved notes to find the correct ID, then come back and delete it. 👇",
            reply_markup=reply_markup,
        )

    else:
        RanaLogger.warning("This should not execute as i will use args value to 0")


async def delete_note_one_arg(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    This is very careful function as by the note id it will
    delete the note permentatly.
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
            "You can also browse your notes using the available options and find the Note ID easily. 📚"
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
            f"🚫 The Note ID You provided (<code>{safe_note_id}</code>) seems to be invalid.\n\n"
            f"Please double-check the ID.\n"
            f"You can:\n"
            f"• Search your notes 📖\n"
            f"• View old chats 💬\n"
            f"• Export your notes 💾\n"
            f"Or simply contact admin for help via <b>/help</b> 🛠️"
        )

        await msg.reply_html(text=text)
        return None

    # Below Means Note row is present
    owner_id = note_row.user_id

    if user.id != owner_id:
        text = (
            "🚫 <b>Access Denied!</b>\n\n"
            "This note does not belong to your account, so you cannot delete it.\n"
            "Only the original note creator has the permission to delete it."
            f"If You you think you r the owner pls bug report at /help"
        )

        await msg.reply_html(text)
        return None

    # this line executes means the owner id of the note and the user is same

    deletion_confirmation = db_functions.delete_note_obj(
        engine=engine,
        note_id=note_id,
        user_id=owner_id,
    )

    if deletion_confirmation:
        note_del_confirm = (
            "✅ <b>Note Deleted!</b>\n\n"
            "Your note has been successfully removed from the database. 🗑️\n"
            "If it was deleted by mistake, sadly, there's no going back 😢"
            f"\n\n"
            f"Title Was:- <s>{note_row.note_title}</s>"
        )

        await msg.reply_html(note_del_confirm)
        return None

    else:
        RanaLogger.warning(
            f"delete fun has been run for note so it should be yes / no."
        )
        text = (
            "⚠️ <b>Deletion Failed</b>\n\n"
            "Something went wrong while trying to delete your note.\n"
            "Please try again later or use <b>/help</b> to contact support. 🛠️"
        )

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

    await msg.reply_html(text=text_many_args)
