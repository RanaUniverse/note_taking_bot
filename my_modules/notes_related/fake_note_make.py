"""
This will make a fake note and insert in the database

"""

import asyncio
import os

from faker import Faker

from sqlmodel import (
    Session,
)

from telegram import Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import ContextTypes


from my_modules.database_code.database_make import engine
from my_modules.database_code.db_functions import user_obj_from_user_id
from my_modules.database_code.models_table import NotePart

from my_modules.logger_related import RanaLogger


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


fake = Faker()


MAX_FAKE_NOTE = 100000


async def fake_note_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /fake_note or /f
    And this function will executes when user will send it and it will save this
    for now it will make a random one note and save it.
    """

    user = update.effective_user
    msg = update.effective_message
    if user is None:
        RanaLogger.warning("User not found when user send /fake_note.")
        return None

    if msg is None:
        RanaLogger.warning("No message object found when user send /fake_note.")
        return None

    # with Session(engine) as session:
    #     statement = select(UserPart).where(UserPart.user_id == user.id)
    #     results = session.exec(statement)
    #     user_row = results.first()

    user_row = user_obj_from_user_id(engine, user.id)

    if user_row is None:
        text_no_user = (
            f"Hello <b>{user.mention_html()}</b>, You Are Not Registered Yet 😢\n"
            f"Please send /register_me and then come back to use this bot.\n"
            f"Else Contact Customer Support /help."
        )
        await msg.reply_html(
            text=text_no_user,
        )
        return None

    # below line will executes when user_row is present

    user_points = user_row.points

    if user_points <= 0:
        text_no_point = (
            f"You Have Finished All Your Points, Now You Cannot "
            f"make new note until you add new points, /add_points followed by int.\n\n"
            f"Example if you want 20 Token, "
            f"<blockquote><code>/add_points 20</code></blockquote>"
        )

        await msg.reply_html(
            text=text_no_point,
        )
        return None

    # below line comes meaans user has valid positive int value of token

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

    # text_made_note = (
    #     f"Your Note Has Been saved Successfully.\n"
    #     f"Your Note Id is: <code>{note_row.note_id}</code>."
    # )

    text_made_note = (
        f"🎉 Your Note Has Been saved Successfully.\n\n"
        f"🧪 1 Fake Note created.\n"
        f"➖ Points spent: <b>One(1)</b>\n"
        f"Your Note Id is: <code>{note_row.note_id}</code>.\n"
        f"💰 Remaining Points: <b>{user_row.points}</b>\n\n"
        f"📂 View them with /all_notes or /my_notes\n"
        f"➕ Need more points? Try /add_points"
    )

    await msg.reply_html(
        text=text_made_note,
        do_quote=True,
    )


async def fake_notes_many(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    This is for when user want to make many fake note for his own
    This will be a simple things this is when user will send
    '/fake_note 5'
    this fun will only execute when it will has only 1 args.
    And it will make 5 notes and save in the database.

    """

    if context.args is None:
        RanaLogger.warning(
            f"When /fake_note int like this come the args should has some value"
        )
        return None

    msg = update.effective_message
    user = update.effective_user

    if user is None:
        RanaLogger.warning("user need to exists when he send /fake_note")
        return None

    if msg is None:
        RanaLogger.warning("msg is present when user send /fake_ntoe")
        return None

    # Below first i will check if user send correct format or not if not it will return

    try:
        how_many_note = int(context.args[0])
        text = (
            f"Hello <b>{user.mention_html()}</b>, You want to add "
            f"{how_many_note} notes in your account.\n\n"
        )
        new_msg = await msg.reply_html(text)

    except ValueError:
        text = (
            f"⚠️ Invalid input!\n"
            f"Please send a valid number. If You want to add 10 fake note, send,\n"
            f"<blockquote><code>/fake_note 10</code></blockquote>\n\n"
        )
        await msg.reply_html(text)
        return None

    except Exception as e:
        RanaLogger.warning(
            f"I dont know how it can work, when user send /fake_note some value {e}"
        )
        text = f"Somethings wrong here, please contact /help"
        await msg.reply_html(text)
        return None

    await context.bot.send_chat_action(user.id, ChatAction.TYPING)
    await asyncio.sleep(1)

    if how_many_note <= 0:
        text += (
            f"⚠️ Please provide a <b>positive number</b> of notes to create.\n\n"
            f"📌 Example: <code>/fake_note 5</code>"
        )
        await new_msg.edit_text(
            text=text,
            parse_mode=ParseMode.HTML,
        )
        return None

    if how_many_note > MAX_FAKE_NOTE:

        text += (
            f"🚫 Please don't send too many notes at once. "
            f"<b>Maximum allowed is {MAX_FAKE_NOTE}.</b>\n\n"
            "📌 Example: <code>/fake_note 10</code>"
        )

        await new_msg.edit_text(
            text=text,
            parse_mode=ParseMode.HTML,
        )
        return None

    # with Session(engine) as session:
    #     statement = select(UserPart).where(UserPart.user_id == user.id)
    #     results = session.exec(statement)
    #     user_row = results.first()

    user_row = user_obj_from_user_id(engine, user.id)
    if user_row is None:
        text = (
            f"Hello <b>{user.mention_html()}</b>, You Are Not Registered Yet 😢\n"
            f"Please send /register_me and then come back to use this bot.\n"
            f"If You already register but see this, please Contact Customer Support /help."
        )
        await msg.reply_html(
            text=text,
        )
        return None

    user_points = user_row.points

    if how_many_note > user_points:
        text = (
            f"🚫 <b>Not Enough Points!</b>\n\n"
            f"👤 You currently have <b>{user_points} points</b>, "
            f"but you want to create <b>{how_many_note} notes</b>.\n\n"
            f"💡 Each note requires 1 point.\n"
            f"➡️ Please reduce the number or earn more points to continue. /add_points"
        )
        await msg.reply_html(text)
        return None

    with Session(engine) as session:
        notes_to_add: list[NotePart] = []

        for _ in range(how_many_note):

            note_obj = NotePart(
                note_title=fake.sentence(20)[:MAX_TITLE_LEN],
                note_content=fake.paragraph(50)[:MAX_CONTENT_LEN],
                is_available=True,
                user_id=user_row.user_id,
            )
            notes_to_add.append(note_obj)

        user_row.points -= how_many_note

        session.add_all(notes_to_add)
        session.add(user_row)
        session.commit()

        text = (
            f"🎉 <b>Success!</b>\n\n"
            f"🧪 <b>{how_many_note}</b> fake notes created.\n"
            f"➖ Points spent: <b>{how_many_note}</b>\n"
            f"💰 Remaining Points: <b>{user_row.points}</b>\n\n"
            f"📂 View them with /all_notes or /my_notes\n"
            f"➕ Need more points? Try /add_points"
        )

        await msg.reply_text(text, parse_mode=ParseMode.HTML)
