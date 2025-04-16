"""
Here i will write code which will able and help me to export a note
"""

from telegram import Update
from telegram.ext import ContextTypes

from my_modules.logger_related import RanaLogger
async def export_note_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    It will maybe make a text file and share this file to user
    """

    query = update.callback_query

    if query is None:
        RanaLogger.warning(f"When export note button pressed the query shoudl be present")        
        return None
    
    text = f"Export NOte Features will come soon here"

    await query.answer(text=text , show_alert=True,)
