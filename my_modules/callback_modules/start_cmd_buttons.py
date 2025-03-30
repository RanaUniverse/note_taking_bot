"""
The buttons which are attached with the /start message reply
i will handle the buttons having on this message.
"""

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


async def button_for_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    This means the buttons attached with the /start reply, will
    be here in this funcion
    """
    query = update.callback_query

    if query is None:
        return

    if query.data == "new_note":
        await query.answer(
            text="⚠️ This feature is still in development. Please use the corresponding command instead! 🚧",
            show_alert=True,
        )
        await query.edit_message_text(
            text="📝 To create a new note, use the command:\n<b>/new_note</b>",
            parse_mode=ParseMode.HTML,
        )

    elif query.data == "view_notes":
        await query.answer(
            text="⚠️ This feature is still in development. Please use the corresponding command instead! 🚧",
            show_alert=True,
        )
        await query.edit_message_text(
            text="📂 To view all notes, use the command:\n<b>/view_notes</b>",
            parse_mode=ParseMode.HTML,
        )

    elif query.data == "edit_note":
        await query.answer(
            text="⚠️ This feature is still in development. Please use the corresponding command instead! 🚧",
            show_alert=True,
        )
        await query.edit_message_text(
            text="✏️ To edit an existing note, use the command:\n<b>/edit_note</b>",
            parse_mode=ParseMode.HTML,
        )

    elif query.data == "search_note":
        await query.answer(
            text="⚠️ This feature is still in development. Please use the corresponding command instead! 🚧",
            show_alert=True,
        )
        await query.edit_message_text(
            text="🔍 To search for a note, use the command:\n<b>/search_note</b>",
            parse_mode=ParseMode.HTML,
        )

    elif query.data == "delete_note":
        await query.answer(
            text="⚠️ This feature is still in development. Please use the corresponding command instead! 🚧",
            show_alert=True,
        )
        await query.edit_message_text(
            text="❌ To delete a note, use the command:\n<b>/delete_note</b>",
            parse_mode=ParseMode.HTML,
        )

    elif query.data == "export_notes":
        await query.answer(
            text="⚠️ This feature is still in development. Please use the corresponding command instead! 🚧",
            show_alert=True,
        )
        await query.edit_message_text(
            text="📤 To export all notes, use the command:\n<b>/export_notes</b>",
            parse_mode=ParseMode.HTML,
        )

    elif query.data == "update_profile":
        await query.answer(
            text="⚠️ This feature is still in development. Please use the corresponding command instead! 🚧",
            show_alert=True,
        )
        await query.edit_message_text(
            text="⚙️ To update your profile, use the command:\n<b>/update_profile</b>",
            parse_mode=ParseMode.HTML,
        )

    elif query.data == "help_section":
        await query.answer(
            text="⚠️ This feature is still in development. Please use the corresponding command instead! 🚧",
            show_alert=True,
        )
        await query.edit_message_text(
            text=f"This is same as /help",
            parse_mode=ParseMode.HTML,
        )
