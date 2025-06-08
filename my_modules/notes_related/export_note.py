"""
Here i will write code which will able and help me to export a note
    export_note_txt_
    export_note_pdf_
"""

from pathlib import Path


from telegram import Update
from telegram import User, Message
from telegram.ext import ContextTypes

from my_modules.database_code.models_table import NotePart
from my_modules.logger_related import RanaLogger

from my_modules.rana_needed_things import make_footer_text

from my_modules.some_constants import BotSettingsValue


TEMPORARY_FOLDER_NAME = BotSettingsValue.FOLDER_NOTE_TEM_NAME.value


def make_txt_file_from_note(note_obj: NotePart, user: User, msg: Message) -> Path:
    """
    This will generate the txt file with also footer and so on
    this is good for now, i want to use this for single
    note export
    """

    note_description = (
        f"📝 Title:\n"
        f"{note_obj.note_title}"
        f"\n\n\n"
        f"📄 Content:\n"
        f"{note_obj.note_content}"
        f"\n\n\n"
        f"Note ID: {note_obj.note_id}"
    )

    full_text = note_description + make_footer_text(user, msg)
    filename = f"user_id_{user.id}_time_{int(msg.date.timestamp())}.txt"
    file_dir = Path.cwd() / TEMPORARY_FOLDER_NAME
    file_dir.mkdir(parents=True, exist_ok=True)
    file_path = file_dir / filename
    file_path.write_text(full_text)

    return file_path


async def export_note_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    This is a general button no need in reality.
    It will maybe make a text file and share this file to user
    """

    query = update.callback_query

    if query is None:
        RanaLogger.warning(
            f"When export note button pressed the query shoudl be present"
        )
        return None

    text = f"Export NOte Features will come soon here"

    await query.answer(
        text=text,
        show_alert=True,
    )


async def export_note_txt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    When User will press the button for export his note as txt
    This will execute.
    Callback Data:- `export_note_txt_`

    """

    ...
