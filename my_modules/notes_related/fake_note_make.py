"""
This will make a fake note and insert in the database

"""

import asyncio


from faker import Faker

from sqlmodel import Session

from telegram import Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import ContextTypes

from my_modules import message_templates

from my_modules.database_code.database_make import engine
from my_modules.database_code import db_functions
from my_modules.database_code.models_table import NotePart

from my_modules.logger_related import RanaLogger

from my_modules.notes_related.export_note import make_txt_file_from_note

from my_modules import bot_config_settings


MAX_TITLE_LEN = bot_config_settings.MAX_TITLE_LEN
MAX_CONTENT_LEN = bot_config_settings.MAX_CONTENT_LEN
MAX_FAKE_NOTE_COUNT = bot_config_settings.MAX_FAKE_NOTE_COUNT
WILL_TEM_NOTE_DELETE = bot_config_settings.WILL_TEM_NOTE_DELETE


fake = Faker()


async def fake_note_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /fake_note
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

    user_row = db_functions.user_obj_from_user_id(engine, user.id)

    if user_row is None:
        text_no_user = message_templates.prompt_user_to_register(user=user)
        await msg.reply_html(text=text_no_user)
        return None

    # below line will executes when user_row is present

    user_points = user_row.points

    if user_points <= 0:
        text_no_point = message_templates.user_has_no_valid_points(user)
        await msg.reply_html(text=text_no_point)
        return None

    # below line comes means user has valid positive int value of token

    fake_title = fake.sentence(20)[:MAX_TITLE_LEN]
    fake_content = fake.paragraph(50)[:MAX_CONTENT_LEN]

    note_row = NotePart(
        note_title=fake_title,
        note_content=fake_content,
        is_available=True,
    )

    # This below fun run will changes the user row and note row update
    db_functions.add_one_note_and_update_the_user(engine, user_row, note_row)

    # As the upper fun re value the variable, so this is just automatically
    note_maked_text = message_templates.new_note_making_confirmation_yes(
        note_obj=note_row,
        user_balance=user_row.points,
    )

    caption_text = (
        f"🧪 1 Fake Note created.\n"
        f"{note_maked_text}"
        f"If you want to make many fake note pls send: <code> /fake_note Number </code>\n\n"
        f"📂 View them with /all_notes or /my_notes\n"
    )

    file_path = make_txt_file_from_note(note_obj=note_row, user=user, msg=msg)

    await msg.reply_document(
        document=file_path,
        filename=f"FakeNote_{file_path.name}",
        caption=caption_text,
        parse_mode=ParseMode.HTML,
    )

    if WILL_TEM_NOTE_DELETE:
        file_path.unlink(missing_ok=True)
        return None


async def fake_notes_many(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    This is for when user want to make many fake note for his own
    This will be a simple things this is when user will send
    '/fake_note 5'
    this fun will only execute when it will has only 1 args.
    And it will make 5 notes and save in the database.

    """

    msg = update.effective_message
    user = update.effective_user

    if msg is None or user is None:
        RanaLogger.warning("When /fake_note args come the user and msg must has exists")
        return None

    if context.args is None:
        RanaLogger.warning(
            f"When /fake_note int like this come the args should has some value"
        )
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

    if how_many_note > MAX_FAKE_NOTE_COUNT:

        text += (
            f"🚫 Please don't send too many notes at once. "
            f"<b>Maximum allowed is {MAX_FAKE_NOTE_COUNT}.</b>\n\n"
            "📌 Example: <code>/fake_note 10</code>"
        )

        await new_msg.edit_text(
            text=text,
            parse_mode=ParseMode.HTML,
        )
        return None

    user_row = db_functions.user_obj_from_user_id(engine, user.id)
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
        user_row.note_count += how_many_note

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
