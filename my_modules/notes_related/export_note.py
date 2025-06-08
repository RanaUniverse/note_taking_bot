"""
Here i will write code which will able and help me to export a note
    export_note_txt_
    export_note_pdf_
"""

from datetime import datetime

from pathlib import Path


from telegram import Update
from telegram import User, Message

from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from my_modules.database_code import db_functions
from my_modules.database_code.database_make import engine
from my_modules.database_code.models_table import NotePart


from my_modules.logger_related import RanaLogger

from my_modules.rana_needed_things import make_footer_text

from my_modules.some_constants import BotSettingsValue


TEMPORARY_FOLDER_NAME = BotSettingsValue.FOLDER_NOTE_TEM_NAME.value


def make_txt_file_from_note(
    note_obj: NotePart,
    user: User,
    msg: Message,
    use_corrent_time: bool = False,
) -> Path:
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

    timestamp = datetime.now() if use_corrent_time else msg.date
    readable_time = timestamp.strftime("%Y-%m-%d_%H_%M_%S")

    filename = f"time_{readable_time}.txt"
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


async def export_note_as_txt_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    When User will press the button for export his note as txt
    This will execute.
    Callback Data:- `export_note_txt_`
    """

    msg = update.effective_message
    user = update.effective_user

    if msg is None or user is None:
        RanaLogger.warning("Export Txt Note Button must has the msg and user")
        return None

    query = update.callback_query
    if query is None or query.data is None:
        RanaLogger.warning("Export Note as txt button must has the query and its data")
        return None

    note_id = query.data.removeprefix("export_note_txt_")

    note_row = db_functions.note_obj_from_note_id(
        engine=engine,
        note_id=note_id,
    )

    if note_row is None:
        text = (
            f"🚫 <b>Note Not Accessible</b>\n\n"
            f"😢 This note is no longer available.\n"
            f"It might have been <b>deleted</b> or "
            f"there was an <b>unexpected issue</b>.\n\n"
            f"📌 Try checking your other notes using /all_notes."
        )
        await msg.reply_html(text)
        return None

    # Below line executes means Note_row is available

    if note_row.user_id != user.id:
        RanaLogger.warning(
            "The user who pressed the button for export note "
            "his user id is not own the note owner, "
            "maybe this is a issue as i cannot think properly."
        )
        return None

    file_path = make_txt_file_from_note(
        note_obj=note_row,
        user=user,
        msg=msg,
        use_corrent_time=True,
    )

    caption_text = f"This Is Your Note as TXT File."

    await query.answer(f"Note Exported Successfully")
    await msg.reply_document(
        document=file_path,
        filename=f"ExportedNote_{file_path.name}",
        caption=caption_text,
        parse_mode=ParseMode.HTML,
    )

    file_path.unlink(missing_ok=True)


async def export_note_as_pdf_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    When User presses the button to export their note as a PDF,
    this function will be called.

    Callback Data:- `export_note_pdf_`
    """

    msg = update.effective_message
    user = update.effective_user

    if msg is None or user is None:
        RanaLogger.warning("Export PDF Note Button must have the msg and user")
        return None

    query = update.callback_query
    if query is None or query.data is None:
        RanaLogger.warning("Export Note as PDF button must have the query and its data")
        return None

    note_id = query.data.removeprefix("export_note_pdf_")

    note_row = db_functions.note_obj_from_note_id(
        engine=engine,
        note_id=note_id,
    )

    if note_row is None:
        text = (
            f"🚫 <b>Note Not Accessible</b>\n\n"
            f"😢 This note is no longer available.\n"
            f"It might have been <b>deleted</b> or "
            f"there was an <b>unexpected issue</b>.\n\n"
            f"📌 Try checking your other notes using /all_notes."
        )
        await msg.reply_html(text)
        return None

    if note_row.user_id != user.id:
        RanaLogger.warning(
            "User trying to export a note they don't own. "
            "Potential issue or misuse attempt."
        )
        return None

    await query.answer("Coming Soon!")
    await msg.reply_html(
        "<b>📄 Export as PDF</b>\n\n"
        "🛠 This feature is not available yet.\n"
        "🚧 It will be added in a future update. Stay tuned!"
    )


# this fun need to be in a good module
async def share_note_coming_soon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Placeholder for future 'Share Note' feature.
    Callback Data: 'share_note_<note_id>'
    """

    msg = update.effective_message
    user = update.effective_user

    if msg is None or user is None:
        RanaLogger.warning("Share Note Button must have the msg and user")
        return None

    query = update.callback_query
    if query is None or query.data is None:
        RanaLogger.warning("Share Note button must have the query and its data")
        return None

    note_id = query.data.removeprefix("share_note_")

    note_row = db_functions.note_obj_from_note_id(
        engine=engine,
        note_id=note_id,
    )

    if note_row is None:
        text = (
            f"🚫 <b>Note Not Accessible</b>\n\n"
            f"😢 This note is no longer available.\n"
            f"It might have been <b>deleted</b> or "
            f"there was an <b>unexpected issue</b>.\n\n"
            f"📌 Try checking your other notes using /all_notes."
        )
        await msg.reply_html(text)
        return None

    if note_row.user_id != user.id:
        RanaLogger.warning("User tried to share a note they do not own.")
        return None

    await query.answer("Coming Soon!")
    await msg.reply_html(
        "<b>🔗 Share Note</b>\n\n"
        "🚧 This feature is not available yet.\n"
        "✨ It will be added in a future update. Stay tuned!"
    )


async def duplicate_note_coming_soon(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """
    Placeholder for future 'Duplicate Note' feature.
    Callback Data: 'duplicate_note_<note_id>'
    """

    msg = update.effective_message
    user = update.effective_user

    if msg is None or user is None:
        RanaLogger.warning("Duplicate Note Button must have the msg and user")
        return None

    query = update.callback_query
    if query is None or query.data is None:
        RanaLogger.warning("Duplicate Note button must have the query and its data")
        return None

    note_id = query.data.removeprefix("duplicate_note_")

    note_row = db_functions.note_obj_from_note_id(
        engine=engine,
        note_id=note_id,
    )

    if note_row is None:
        text = (
            f"🚫 <b>Note Not Accessible</b>\n\n"
            f"😢 This note is no longer available.\n"
            f"It might have been <b>deleted</b> or "
            f"there was an <b>unexpected issue</b>.\n\n"
            f"📌 Try checking your other notes using /all_notes."
        )
        await msg.reply_html(text)
        return None

    if note_row.user_id != user.id:
        RanaLogger.warning("User tried to duplicate a note they do not own.")
        return None

    await query.answer("Coming Soon!")
    await msg.reply_html(
        "<b>📋 Duplicate Note</b>\n\n"
        "🚧 This feature is not available yet.\n"
        "✨ It will be added in a future update. Stay tuned!"
    )
