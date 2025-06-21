"""
This will make a fake note and insert in the database.

"""

from faker import Faker

from sqlmodel import Session

from telegram import Update
from telegram import InlineKeyboardMarkup
from telegram.constants import ChatAction, ParseMode
from telegram.ext import ContextTypes

from my_modules import bot_config_settings
from my_modules import message_templates
from my_modules import inline_keyboard_buttons

from my_modules.database_code.database_make import engine
from my_modules.database_code import db_functions
from my_modules.database_code.models_table import NotePart

from my_modules.logger_related import RanaLogger
from my_modules.notes_related import export_note


MAX_CONTENT_LEN = bot_config_settings.MAX_CONTENT_LEN
MAX_TITLE_LEN = bot_config_settings.MAX_TITLE_LEN
MAX_FAKE_NOTE_COUNT = bot_config_settings.MAX_FAKE_NOTE_COUNT
WILL_TEM_NOTE_DELETE = bot_config_settings.WILL_TEM_NOTE_DELETE
FAKE_NOTE_MAKING_BUTTON = inline_keyboard_buttons.FAKE_NOTE_MAKING_BUTTON

fake = Faker()


async def fake_note_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /fake_note
    This Fun will Execute and it will add one fake note to user.
    """

    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None:
        RanaLogger.warning("User & msg not found when user send /fake_note.")
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
        f"📂 View them with /my_notes\n"
    )

    file_path = export_note.make_txt_file_from_note(
        note_obj=note_row, user=user, msg=msg
    )

    buttons_successfull_note = inline_keyboard_buttons.generate_buttons_with_note_view(
        note_row.note_id
    )

    await msg.reply_document(
        document=file_path,
        filename=f"FakeNote_{file_path.name}",
        caption=caption_text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(buttons_successfull_note),
    )

    if WILL_TEM_NOTE_DELETE:
        file_path.unlink(missing_ok=True)
        return None


async def fake_notes_many(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /fake_note some_int_value
    It will make some notes and then save those notes in the database.
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

    first_arg_value = context.args[0]

    if not first_arg_value.isdigit():
        await msg.reply_html(
            "⚠️ Invalid input!\n"
            "Please provide a valid number. Example:\n"
            "<blockquote><code>/fake_note 10</code></blockquote>"
        )
        return

    try:
        how_many_note = int(first_arg_value)
        ...

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
            f"When user will pass some arg value to the /fake_note command"
            f"the Value need to be converted as i found there "
            f"is no more possible for this error for now\n"
            f"{e}"
        )
        text = f"⚠️ Something went wrong. Please use /help or contact support."
        await msg.reply_html(text)
        return None

    await context.bot.send_chat_action(user.id, ChatAction.TYPING)

    if how_many_note <= 0:
        text = (
            f"⚠️ Please provide a <b>positive number</b> of notes to create.\n\n"
            f"📌 Example: <code>/fake_note 5</code>"
        )
        await msg.reply_html(
            text=text,
        )
        return None

    if how_many_note > MAX_FAKE_NOTE_COUNT:

        text = (
            f"🚫 Sorry, I can't create that many notes at the moment.\n"
            f"The maximum allowed is <b>{MAX_FAKE_NOTE_COUNT}</b>.\n\n"
            f"Please consider upgrading your account to Pro for Higher Limit.\n"
            f"If you believe this is a mistake or need assistance, "
            f"feel free to contact the admin.\n\n"
            f"📌 Example usage: <code>/fake_note 10</code>"
        )

        await msg.reply_html(
            text=text,
        )
        return None

    user_row = db_functions.user_obj_from_user_id(engine, user.id)
    if user_row is None:
        text_no_user = message_templates.prompt_user_to_register(user=user)
        await msg.reply_html(text=text_no_user)
        return None

    user_points = user_row.points

    if how_many_note > user_points:

        required_points = how_many_note
        missing_points = required_points - user_points
        text = (
            f"🚫 <b>Not Enough Points!</b>\n\n"
            f"👤 You currently have <b>{user_points} point(s)</b>, "
            f"but you're trying to create <b>{how_many_note} fake notes</b>.\n\n"
            f"💡 Each note costs 1 point, so you need at least "
            f"<b>{required_points} points</b>.\n"
            f"❗ You are missing <b>{missing_points} point(s)</b>.\n\n"
            f"➡️ To continue, please reduce the number or add more points using:\n"
            f"<code>/add_points {missing_points}</code>"
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

        note_info_text = ""

        for idx, note in enumerate(notes_to_add, start=1):
            note_info_text += (
                f"Note No. {idx}"
                "\n"
                f"Note ID: {note.note_id}"
                "\n"
                f"Title: {note.note_title}\n\n"
            )

        caption_text = (
            f"🎉 <b>Success!</b>\n\n"
            f"🧪 <b>{how_many_note}</b> fake notes created.\n"
            f"➖ Points spent: <b>{how_many_note}</b>\n"
            f"💰 Remaining Points: <b>{user_row.points}</b>\n\n"
            f"📂 View them with /my_notes\n"
            f"➕ Need more points? Try /add_points"
        )

    file_path = export_note.txt_file_making_for_many_fake_note(
        note_text=note_info_text,
        user=user,
        msg=msg,
        use_corrent_time=True,
    )

    await msg.reply_document(
        document=file_path,
        filename=f"Many_FakeNote_{file_path.name}",
        caption=caption_text,
        parse_mode=ParseMode.HTML,
    )

    if WILL_TEM_NOTE_DELETE:
        file_path.unlink(missing_ok=True)
        return None


async def fake_note_making_by_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    When user will want to make one note just pressing the button

        FAKE_NOTE_MAKING_BUTTON = InlineKeyboardButton(
        text="🌀 Make A Fake Note",
        callback_data="make_fake_note",
    )
    """
    query = update.callback_query

    if query is None or query.data is None:
        RanaLogger.warning(
            f"When making fake note button is pressed "
            "callback query data should exists"
        )
        return None
    await query.answer("One Fake Note is Trying To Make Against You.")

    await fake_note_cmd(update=update, context=context)
