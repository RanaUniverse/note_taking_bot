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
                InlineKeyboardButton("View All Notes", callback_data="view_notes"),
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


async def delete_note_one_args(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
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
        RanaLogger.error(f"context.args if not then this fun should not trigger.")
        text = (
            "⚠️ <b>Missing Note ID!</b>\n\n"
            "To delete a note, please provide its unique Note ID.\n"
            "Usage: <code>/delete_note &lt;note_id&gt;</code>\n\n"
            "You can also browse your notes using the available options and find the Note ID easily. 📚"
        )

        await msg.reply_html(text=text)
        return None

    note_id = context.args[0]
    RanaLogger.warning(f"{user.full_name} want to delete the note id of: {note_id}")

    note_row = db_functions.note_obj_from_note_id(
        engine=engine,
        note_id=note_id,
    )

    if note_row is None:
        safe_note_id = html.escape(note_id)  
        text = (
            f"🚫 The Note ID you provided (<code>{safe_note_id}</code>) seems to be invalid.\n\n"
            f"Please double-check the ID.\n"
            f"You can:\n"
            f"• Search your notes 📖\n"
            f"• View old chats 💬\n"
            f"• Export your notes 💾\n"
            f"Or simply contact admin for help via <b>/help</b> 🛠️"
        )

        await msg.reply_html(text=text)
        return

    # Below Means Note row is present
    owner_id = note_row.user_id

    if user.id != owner_id:
        text = (
            "🚫 <b>Access Denied!</b>\n\n"
            "This note does not belong to your account, so you cannot delete it.\n"
            "Only the original note creator has the permission to delete it."
        )

        await msg.reply_html(text)
        return

    deletion_confirmation = db_functions.delete_note_obj(
        engine=engine,
        note_id=note_id,
        user_id=owner_id,
    )

    if deletion_confirmation:
        text = (
            "✅ <b>Note Deleted!</b>\n\n"
            "Your note has been successfully removed from the database. 🗑️\n"
            "If it was deleted by mistake, sadly, there's no going back 😢"
        )

        await msg.reply_html(text)
        return

    else:
        print(f"I wish This should not happens.")
        RanaLogger.warning(
            f"I wish This should not happens because delete fun has been run for notes."
        )
        text = (
            "⚠️ <b>Deletion Failed</b>\n\n"
            "Something went wrong while trying to delete your note.\n"
            "Please try again later or use <b>/help</b> to contact support. 🛠️"
        )

        await msg.reply_html(text)
        return
