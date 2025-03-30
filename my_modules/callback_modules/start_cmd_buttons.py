"""
The buttons which are attached with the /start message reply
i will handle the buttons having on this message.
"""

from telegram import Update
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
        print("New Button Has Been pressed")
        await query.answer(
            text="This Button is in Development",
            show_alert=True,
        )
        await query.edit_message_text(
            text="Please send /new_note and then you can make a note here.",
        )
