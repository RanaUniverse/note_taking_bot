"""
here i will keep the notes logic so that a user can find all his notes
this will allow users to find how many notes he has
the lists of notes

"""

from sqlmodel import (
    select,
    Session,
)

from telegram import Update
from telegram.ext import ContextTypes

from my_modules.logger_related import RanaLogger
from my_modules.database_code.database_make import engine
from my_modules.database_code.models_table import NotePart, UserPart


async def all_notes_cmd_old(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    The work of this functions is for when user want to
    know all his notes he want to see

                "/all_notes",
                "/my_notes",

    """

    user = update.effective_user

    if user is None:
        RanaLogger.warning("User need to have in this case")
        return

    if update.effective_message is None:
        RanaLogger.warning("User should has the message obj")
        return

    with Session(engine) as session:
        statement = select(UserPart).where(UserPart.user_id == user.id)
        results = session.exec(statement)
        user_row = results.first()

    if user_row is None:
        text = (
            f"You Have Not Any Note & you have not made any note yet. "
            f"To make new note send /new_note to make new note"
        )
        await update.effective_message.reply_html(text)
        return

    all_notes = user_row.notes

    text = f"You Have Total {len(all_notes)} Notes."
    await update.effective_message.reply_html(text)


async def all_notes_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    The work of this functions is for when user want to
    know all his notes he want to see

                "/all_notes",
                "/my_notes",
    """

    user = update.effective_user

    if user is None:
        RanaLogger.warning("User need to have in this case")
        return

    if update.effective_message is None:
        RanaLogger.warning("User should has the message obj")
        return

    with Session(engine) as session:
        statement = select(NotePart).where(NotePart.user_id == user.id)
        results = session.exec(statement)
        notes = results.all()

    text = f"📜 <b>You have {len(notes)} notes:</b>\n\n"

    for idx, note in enumerate(notes, start=1):
        text += (
            f"{idx}. <b><u>Title</u></b>: <b>{note.note_title}</b> - "
            f"<b><u>ID</u></b>: <code>{note.note_id}</code>\n\n"
        )

    await update.effective_message.reply_html(
        text,
    )
