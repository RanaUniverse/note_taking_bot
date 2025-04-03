"""

Here i will keep the code having send the response to user when he want to get his notes
When user will press the buttons and it will handle the callback data.


here i will keep the notes logic so that a user can find all his notes
this will allow users to find how many notes he has
the lists of notes

In this code i started using this below like logic

    user = update.effective_user
    if not user:
        return

    msg = update.effective_message
    if msg is None:
        return

So that i can work easily and more effectively like,
    await msg.reply_html(text)


Below is a code example:

    # Below is just for checking
    # This below is for showsin one button per one line
    text = (
        f"This is a checking test for testing purpose only."
    )
    all_buttons: list[list[InlineKeyboardButton]] = []

    for i in range(1, 10):
        title = f"This is Button No. {i}"
        note_id = f"Button_{i}"

        button_row = [
            InlineKeyboardButton(
                text=title,
                callback_data=note_id,
            )
        ]
        all_buttons.append(button_row)

    await msg.reply_html(
        text=text,
        reply_markup=InlineKeyboardMarkup(all_buttons),
    )


"""

from sqlmodel import (
    select,
    Session,
)

from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

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


async def all_notes_cmd_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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

    if not notes:
        await update.effective_message.reply_html("📭 You have no saved notes.")
        return

    text = f"📜 <b>You have {len(notes)} notes:</b>\n\n"

    for idx, note in enumerate(notes, start=1):
        text += (
            f"{idx}. <b><u>Title</u></b>: <b>{note.note_title}</b> - "
            f"<b><u>ID</u></b>: <code>{note.note_id}</code>\n\n"
        )

    await update.effective_message.reply_html(
        text,
    )


async def all_notes_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not user:
        return

    msg = update.effective_message
    if msg is None:
        return

    with Session(engine) as session:
        statement = select(NotePart).where(NotePart.user_id == user.id)
        results = session.exec(statement)
        notes = results.all()

    print(f"{user.name} has total notes of count:-", len(notes))

    if len(notes) == 0:
        text = (
            f"Hello <b>{user.mention_html()}</b>, You have not made any note yet. "
            f"Please make a note by sending /new_note."
        )

        await msg.reply_html(text)
        return None

    text = (
        f"Hello <b>{user.mention_html()}</b>, You have total {len(notes)} Notes. "
        f"You can see the notes below after pressing on the buttons."
    )

    all_buttons: list[list[InlineKeyboardButton]] = []

    for note_row in notes:
        title = f"{note_row.note_title}"
        note_id = note_row.note_id

        button_row = [
            InlineKeyboardButton(
                text=title,
                callback_data=note_id,
            )
        ]

        all_buttons.append(button_row)

    await msg.reply_html(
        text=text,
        reply_markup=InlineKeyboardMarkup(all_buttons),
    )


async def button_for_search_notes_1(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    This will when user want to get his notes which he press on the search notes
    """

    query = update.callback_query

    if query is None:
        RanaLogger.warning(
            f"When user press button on search note, it should have the data."
        )
        return

    await query.answer("Please check Your Message.", True)

    note_id = query.data

    with Session(engine) as session:
        statement = select(NotePart).where(NotePart.note_id == note_id)
        results = session.exec(statement)
        note_row = results.one()

    text = f"The Note Information is: \n\n" f"{note_row}"

    await query.edit_message_text(text)

    msg = query.message

    if msg is None:
        RanaLogger.warning("When button is pressed which has a message")
        return

    from telegram import Message, InaccessibleMessage

    if isinstance(msg, Message):
        print("This has a message")
        user = msg.from_user
        if user is None:
            return
        text = f"this is your note"
        await context.bot.send_message(user.id, text)

    elif isinstance(msg, InaccessibleMessage):
        print("Maybe message got deleted.")


async def button_for_search_notes(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    This will when user want to get his notes which he press on the search notes
    """

    query = update.callback_query

    if query is None:
        RanaLogger.warning(
            f"When user press button on search note, it should have the data."
        )
        return

    await query.answer("Please check Your Message.")

    msg = update.effective_message

    if msg is None:
        RanaLogger.warning("When button is pressed this should have the msg obj")
        return

    # This data is attached with the button user has just pressed
    note_id = query.data

    with Session(engine) as session:
        statement = select(NotePart).where(NotePart.note_id == note_id)
        results = session.exec(statement)
        note_row = results.first()

    if note_row is None:
        text = (
            f"This Note is Not Accessable Anymore 😢😢😢\n"
            f"Maybe This got deleted or some problem"
        )
        await msg.reply_html(text)
        return

    # Format the timestamps
    created_time = (
        note_row.created_time.strftime("%Y-%m-%d %H:%M:%S")
        if note_row.created_time
        else "Unknown"
    )
    edited_time = (
        note_row.edited_time.strftime("%Y-%m-%d %H:%M:%S")
        if note_row.edited_time
        else "Never Edited"
    )

    # Create the formatted message
    text = (
        f"📝 <b>Note Details:</b>\n\n"
        f"📌 <b>Title:</b> {note_row.note_title}\n\n"
        f"📖 <b>Content:</b>\n{note_row.note_content}\n\n"
        f"🕒 <b>Created On:</b> {created_time}\n\n"
        f"🛠 <b>Last Edited:</b> {edited_time}\n\n"
        f"🆔 <b>Note ID:</b> <code>{note_row.note_id}</code>\n\n"
    )

    await msg.reply_html(text)
