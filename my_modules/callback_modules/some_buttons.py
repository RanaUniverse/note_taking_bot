"""
some buttons will be separated in this file
i will kept them for easy editable and easy to separate the logics
"""

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from my_modules.logger_related import RanaLogger


async def update_profile_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    When the button having this callback_data =update_profile
    i will make this separate just for easy development.
    """

    query = update.callback_query

    if query is None:
        return

    text = (
        f"You Need To Register here to use this bot, To register please send, \n"
        f"/register_me"
    )

    if query.data == "update_profile":
        # await query.answer(
        #     text="⚠️ You are going to edit your profile.🚧",
        #     show_alert=True,
        # )
        await query.edit_message_text(
            text=text,
            parse_mode=ParseMode.HTML,
        )


async def new_note_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = update.effective_message
    if msg is None:
        RanaLogger.warning("Button pressed but msg is none for new note making.")
        return None

    query = update.callback_query
    if query is None or query.data is None:
        RanaLogger.warning("Button pressed on new note confirm , but not query :cry")
        return None

    await query.answer()

    action, _ = query.data.split("_", 1)

    # Default messages for each action
    if action == "view":
        reply = "👀 Viewing note feature in development."
    elif action == "export":
        reply = "📤 Export feature in development."
    elif action == "delete":
        reply = "🗑️ Delete feature in development."
    elif action == "share":
        reply = "🔗 Share feature in development."
    else:
        reply = "⚠️ Unknown action."

    reply_text = reply + "\n" + "Please wait for next update"

    await msg.reply_html(text=reply_text, do_quote=True)
