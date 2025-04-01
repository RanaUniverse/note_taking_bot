"""
This will make a fake note and insert in the database

"""

import os

from faker import Faker

from sqlmodel import (
    select,
    Session,
)

from telegram import Update
from telegram.ext import ContextTypes


from my_modules.database_code.database_make import engine
from my_modules.database_code.models_table import UserPart, NotePart

from my_modules.logger_related import RanaLogger

fake = Faker()


MAX_TITLE_STR = os.environ.get("MAX_TITLE", None)

if not MAX_TITLE_STR:
    raise ValueError("❌ MAX_TITLE not found in .env file!")
try:
    MAX_TITLE_LEN = int(MAX_TITLE_STR)  # Convert to int
except ValueError:
    raise ValueError("❌ MAX_TITLE must be a valid integer!")


MAX_CONTENT_STR = os.environ.get("MAX_CONTENT", None)

if not MAX_CONTENT_STR:
    raise ValueError("❌ MAX_CONTENT not found in .env file!")
try:
    MAX_CONTENT_LEN = int(MAX_CONTENT_STR)  # Convert to int
except ValueError:
    raise ValueError("❌ MAX_CONTENT must be a valid integer!")


async def fake_note_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /new_fake_note or /fake_note /generate_fake_note.
    And this function will executes when user will send it and it will save this
    it will have some idea
    """

    user = update.effective_user
    if user is None:
        RanaLogger.warning("User not found.")
        return

    if update.effective_message is None:
        RanaLogger.warning("No message object found.")
        return

    with Session(engine) as session:
        statement = select(UserPart).where(UserPart.user_id == user.id)
        results = session.exec(statement)
        user_row = results.first()

    if user_row is None:
        text = (
            f"Hello <b>{user.mention_html()}</b>, You Are Not Registered Yet 😢\n"
            f"Please send /register_me and then come back to use this bot.\n"
            f"Else Contact Customer Support /help."
        )
        await update.effective_message.reply_html(
            text=text,
        )
        return None

    user_points = user_row.points

    if user_points <= 0:
        text = (
            f"You Have Finished All Your Points, Now You Cannot "
            f"make new note until you add new points, /add_points followed by int.\n\n"
            f"Example if you want 20 Token, <blockquote><code>/add_points 20</code></blockquote>"
        )

        await update.effective_message.reply_html(
            text=text,
        )
        return None

    fake_title = fake.sentence(20)[:MAX_TITLE_LEN]
    fake_content = fake.paragraph(50)[:MAX_CONTENT_LEN]

    note_row = NotePart(
        note_title=fake_title,
        note_content=fake_content,
        is_available=True,
    )

    with Session(engine) as session:

        user_row.points -= 1
        note_row.user = user_row

        session.add(note_row)
        session.commit()
        session.refresh(note_row)
        session.refresh(user_row)

    text = (
        f"Your Note Has Been saved Successfully.\n"
        f"Your Note Id is: <code>{note_row.note_id}</code>."
    )

    if update.effective_message is None:
        RanaLogger.warning(f"This must have a message")
        return None

    await update.effective_message.reply_html(
        text,
        do_quote=True,
    )
    return None
