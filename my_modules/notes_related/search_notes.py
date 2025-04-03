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
from my_modules.database_code.models_table import NotePart


NOTES_PER_PAGE = 5
OFFSET_VALUE = 0


async def all_notes_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not user:
        return

    msg = update.effective_message
    if msg is None:
        return

    with Session(engine) as session:
        statement = (
            select(NotePart)
            .where(NotePart.user_id == user.id)
            .offset(OFFSET_VALUE)
            .limit(NOTES_PER_PAGE)
        )
        results = session.exec(statement)
        notes = results.all()

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

    current_page = 1
    next_page = current_page + 1

    next_button = [
        InlineKeyboardButton(
            text=f"More Notes (Page {next_page}) →",
            callback_data=f"notes_page_{next_page}",  # Send next page number
        )
    ]
    all_buttons.append(next_button)

    await msg.reply_html(
        text=text,
        reply_markup=InlineKeyboardMarkup(all_buttons),
    )


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

    # Format the timestamps for clearification saw.
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
        f"📌 <b>Title:</b> \n{note_row.note_title}\n\n"
        f"📖 <b>Content:</b>\n{note_row.note_content}\n\n"
        f"🕒 <b>Created On:</b> {created_time}\n\n"
        f"🛠 <b>Last Edited:</b> {edited_time}\n\n"
        f"🆔 <b>Note ID:</b> <code>{note_row.note_id}</code>\n\n"
    )

    await msg.reply_html(text)


async def button_for_next_page(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    when user will press the next button to see more extra notes user want to see
    here it will search for the page number which is attached with the button
    from there it will search the page number, and it will calculate the offser and limit value

    """

    query = update.callback_query

    if query is None:
        RanaLogger.warning(
            f"When user press button on search note, it should have the data."
        )
        return

    await query.answer("Please check Your Notes Below 👇👇👇.")

    user = update.effective_user

    if user is None:
        RanaLogger.warning("User should has some value in the next button press")
        return

    msg = update.effective_message

    if msg is None:
        RanaLogger.warning("When button is pressed this should have the msg obj")
        return

    # This data is attached with the button user has just pressed
    print("A User Has send", query.data)

    if query.data is None:
        RanaLogger.warning("The query should be a button attached with next button")
        return None

    if query.data.startswith("notes_page_"):
        current_page = int(query.data.split("_")[-1])
        # this upper formatting is when i am using the constitanty value in the button

    else:
        current_page = 1
        RanaLogger.warning("Current page should not be 1 ever as i can think")

    OFFSET_VALUE = (current_page - 1) * NOTES_PER_PAGE

    with Session(engine) as session:
        statement = (
            select(NotePart)
            .where(NotePart.user_id == user.id)
            .offset(OFFSET_VALUE)
            .limit(NOTES_PER_PAGE)
        )
        results = session.exec(statement)
        notes = results.all()

    if len(notes) == 0:
        await msg.reply_html("📭 You have no MOre saved notes.")

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

    next_page = current_page + 1

    next_button = [
        InlineKeyboardButton(
            text=f"More Notes (Page {next_page}) →",
            callback_data=f"notes_page_{next_page}",
        )
    ]
    all_buttons.append(next_button)

    await msg.reply_html(
        text=text,
        reply_markup=InlineKeyboardMarkup(all_buttons),
    )
