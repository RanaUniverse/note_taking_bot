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

from typing import Sequence

from telegram import Message, User
from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from telegram.ext import ContextTypes

from my_modules.logger_related import RanaLogger

from my_modules.database_code.database_make import engine
from my_modules.database_code.models_table import NotePart

from my_modules.database_code import db_functions

from my_modules.some_constants import BotSettingsValue
from my_modules.some_inline_keyboards import generate_view_note_buttons


NOTES_PER_PAGE: int = BotSettingsValue.NOTES_PER_PAGE.value
OFFSET_VALUE = BotSettingsValue.OFFSET_VALUE.value


async def reply_user_has_no_notes(msg: Message, user: User):
    """
    This will send a reply msg just.
    This is for reuse code.
    When user has 0 notes this reply send usually.
    """
    text_no_note = (
        f"Hey <b>{user.mention_html()}</b>! 📭 "
        f"You haven’t created any notes yet. "
        f"Why not get started? "
        f"Just send <code>/new_note</code> to make your first one.\n\n"
        f"Feeling playful? Try <code>/fake_note</code> or "
        f"even add a number like <code>/fake_note 3</code> for some fun examples!"
    )
    await msg.reply_html(text_no_note)


def all_notes_button_text(how_many_note: int, user: User) -> str:
    """
    This will generate the text which is assign with the buttons of the all notes first time.
    """
    text = (
        f"👋 <b>Hey {user.mention_html()}!</b>\n\n"
        f"🗂️ <b>Total Notes:</b> <code>{how_many_note}</code>\n"
        f"📖 Ready to explore or edit them?\n\n"
        f"👇 Tap a note below to open it:"
    )

    return text


def make_all_note_buttons(
    some_notes: Sequence[NotePart],
    how_many_note: int,
    current_page: int = 1,
) -> list[list[InlineKeyboardButton]]:
    """
    It will make some notes button of title and then it will return this buttons
    and this buttons value will be use in the reply-keyboard in send msg.
    This just make first part buttons
    How many notes: how many notes he has own
    """
    all_buttons: list[list[InlineKeyboardButton]] = []

    for i, note_row in enumerate(iterable=some_notes, start=1):
        title = f"{i}. {note_row.note_title}"
        note_id = f"view_note_{note_row.note_id}"

        button_row = [InlineKeyboardButton(text=title, callback_data=note_id)]
        all_buttons.append(button_row)

    # The Below logic is when the button numbers are greater than notes per page
    # Then it will have end button else next page button

    # As this is the starting of the note lists send, so it means it will be start
    # from current page as 1, and nextpage value will be used in the button pressed
    if how_many_note > NOTES_PER_PAGE * current_page:
        current_page = current_page
        next_page = current_page + 1

        # send next_page value in query.data in a button
        next_button = [
            InlineKeyboardButton(
                text=f"Go To Next Page: {next_page}→",
                callback_data=f"next_page_{next_page}",
            )
        ]
        all_buttons.append(next_button)
    else:
        end_button = [
            InlineKeyboardButton(
                text="📄 No More Notes",
                callback_data=f"no_more_notes_{how_many_note}",
            )
        ]
        all_buttons.append(end_button)

    # When the end button is present it means it no note left

    return all_buttons


async def my_notes_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /my_notes in private chat
    First i will try to search the total number of notes row only count
    2nd i will try to get full some row's data completely so that i can work with this,
    and i will send some row's information using some buttons as note's title.
    """
    msg = update.effective_message
    user = update.effective_user
    if msg is None or user is None:
        RanaLogger.warning(f"When /my_notes come the msg and user should be present")
        return None

    all_note_count = db_functions.count_user_notes(
        engine=engine,
        user_id=user.id,
    )

    if all_note_count == 0:
        await reply_user_has_no_notes(msg=msg, user=user)
        return None

    some_notes = db_functions.get_user_notes(
        engine=engine,
        offset_value=OFFSET_VALUE,
        limit_value=NOTES_PER_PAGE,
        user_id=user.id,
    )

    text_with_button = all_notes_button_text(how_many_note=all_note_count, user=user)
    notes_buttons = make_all_note_buttons(
        some_notes=some_notes,
        how_many_note=all_note_count,
    )

    await msg.reply_html(
        text=text_with_button,
        reply_markup=InlineKeyboardMarkup(notes_buttons),
        do_quote=True,
    )


async def handle_my_all_notes_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Handles the 'Find All Notes To Edit' button press.
    'my_all_notes'
    This functions logics are same as /my_notes.
    """

    user = update.effective_user
    msg = update.effective_message
    if msg is None or user is None:
        RanaLogger.warning(f"user msg should be present on the button pressed")
        return

    query = update.callback_query
    if query is None:
        RanaLogger.warning(f"Query should be present of press button of 'all_my_notes'")
        return None

    await query.answer(text="You Can See All Your Notes Below ⬇️⬇️⬇️")

    all_note_count = db_functions.count_user_notes(
        engine=engine,
        user_id=user.id,
    )

    if all_note_count == 0:
        await reply_user_has_no_notes(msg=msg, user=user)
        return None

    some_notes = db_functions.get_user_notes(
        engine=engine,
        offset_value=OFFSET_VALUE,
        limit_value=NOTES_PER_PAGE,
        user_id=user.id,
    )

    text_with_button = all_notes_button_text(how_many_note=all_note_count, user=user)

    notes_buttons = make_all_note_buttons(
        some_notes=some_notes,
        how_many_note=all_note_count,
    )

    await msg.reply_html(
        text=text_with_button,
        reply_markup=InlineKeyboardMarkup(notes_buttons),
        do_quote=True,
    )


async def button_for_search_notes(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    The Note't Title Buttons which also assign the note_id,
    When those button is pressed this fun is executs.
        `pattern=r"^view_note_.*$",`

    """

    msg = update.effective_message
    user = update.effective_user
    if msg is None or user is None:
        RanaLogger.warning("When Note Title Button is pressed msg obj & user also")
        return None

    query = update.callback_query
    if query is None:
        RanaLogger.warning(
            f"When user press button on search note, it should have the data."
        )
        return
    await query.answer("Please check Your Note Below.")

    # When the data is pressed the note_id in callback data will come
    # so it means i need to extract the note id,

    callback_data = query.data
    if callback_data is None:
        RanaLogger.warning(
            "Note Title, button include the callback data, if not means something bad happens in title callback data."
        )
        return None

    note_id = callback_data.removeprefix("view_note_")

    # This upper value should be the note_id which i need to serach on the database

    # with Session(engine) as session:
    #     statement = select(NotePart).where(NotePart.note_id == note_id)
    #     results = session.exec(statement)
    #     note_row = results.first()

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
            f"📌 Try checking your other notes using /my_notes."
        )
        await msg.reply_html(text)
        return None

    # Below part will execute when note id match the value.

    # i will check the owner for a security step, though i dont see any need

    if note_row.user_id != user.id:
        RanaLogger.warning(
            "When Note's Title button is pressed the note owner should pressed as for now"
        )
        await msg.reply_html("Maybe You are not the owner, please message admin /help")
        return None

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

    text = (
        f"🕒 <b>Created On:</b> {created_time}\n\n"
        f"🛠 <b>Last Edited:</b> {edited_time}\n\n"
        f"🆔 <b>Note ID:</b> <code>{note_row.note_id}</code>\n\n"
        f"📝 <b>Note Details:</b>\n\n"
        f"{'👇' * 10}\n"
        f"📌 <b>Title:</b> \n{note_row.note_title}\n\n"
        f"📖 <b>Content:</b>\n{note_row.note_content}\n\n"
        f"Below BUttons is in Development will not work maybe"
    )

    keyboard_view_note = generate_view_note_buttons(note_id=note_row.note_id)

    # 🔍 Check if text exceeds Telegram's 4000-character limit
    if len(text) > 4000:
        text = text[: 4000 - 100]
        text += "\n\n⚠️ This message exceeds the limit and was truncated."

    await msg.reply_html(
        text=text,
        do_quote=True,
        reply_markup=InlineKeyboardMarkup(keyboard_view_note),
    )


async def button_for_next_page(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    `next_page_ int value ` is the callback data.
    when user will press the next button to see more extra notes user want to see
    here it will search for the page number which is attached with the button
    from there it will search the page number, and it will calculate the offser and limit value
    """
    user = update.effective_user
    msg = update.effective_message
    if user is None or msg is None:
        RanaLogger.warning("User & msg should has some value in the next button press")
        return None

    query = update.callback_query
    if query is None:
        RanaLogger.warning(
            f"When user press button on search note, it should have the data."
        )
        return None

    await query.answer("Please check Your Notes Below 👇👇👇.")

    callback_data = query.data

    if callback_data is None:
        RanaLogger.warning("The query should be a button attached with next button")
        return None

    if callback_data.startswith("next_page_"):
        current_page = int(callback_data.split("_")[-1])
        # this upper formatting is when i am using the constitanty value in the button

    if callback_data.startswith("next_page_"):
        try:
            current_page = int(callback_data.split("_")[-1])
        except Exception as _:
            RanaLogger.error(
                "maybe any error from user side as callback "
                "data is not int in next page button"
            )
            return None
    else:
        current_page = 1
        RanaLogger.warning("Current page should not be 1 ever as i can think")

    OFFSET_VALUE = (current_page - 1) * NOTES_PER_PAGE

    some_notes = db_functions.get_user_notes(
        engine=engine,
        offset_value=OFFSET_VALUE,
        limit_value=NOTES_PER_PAGE,
        user_id=user.id,
    )

    if len(some_notes) == 0:
        await msg.reply_html("📭 You have no More saved notes.")
        return None

    total_notes = db_functions.count_user_notes(engine=engine, user_id=user.id)

    total_pages = (total_notes + NOTES_PER_PAGE - 1) // NOTES_PER_PAGE

    text = (
        f"👤 Hello <b>{user.mention_html()}</b>,\n\n"
        f"📄 Page <b>{current_page}</b> of <b>{total_pages}</b>\n"
        f"🗒️ Displaying <b>{len(some_notes)}</b> notes out of <b>{total_notes}</b> total.\n\n"
        f"Select a note below to view its details."
    )

    all_buttons = make_all_note_buttons(
        some_notes=some_notes,
        how_many_note=total_notes,
        current_page=current_page,
    )

    await msg.reply_html(
        text=text,
        reply_markup=InlineKeyboardMarkup(all_buttons),
    )


async def button_for_no_more_notes(
    update: Update, cotnext: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Callback Data: `no_more_notes_`
    This time when user has no more notes and the last button will pressed by user this
    below funcions logic will be executed and this will run

    For now i though when user will press this it will just say this infromation
    """

    query = update.callback_query

    if query is None:
        RanaLogger.warning(
            f"When user press button on search note, it should have the data."
        )
        return None

    if query.data is None:
        RanaLogger.warning("The query should be a button attached with next button")
        return None

    if query.data.startswith("no_more_notes_"):
        note_count = int(query.data.split("_")[-1])

    else:
        note_count = 0
        RanaLogger.warning("Current page should not be 1 ever as i can think")

    text = (
        f"You Have just own {note_count} Numbers of Notes. \n"
        f"Please Make More if you want."
    )

    await query.answer(text, show_alert=True)


async def handle_edit_note_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:

    query = update.callback_query

    if query is None or query.data is None:
        RanaLogger.warning("Edit Note button pressed but no callback data found.")
        return

    await query.answer(
        text="✏️Not come yet, but you can send the below command now to edit.! 🚧",
        show_alert=True,
    )
    msg = update.effective_message
    if msg is None:
        RanaLogger.warning(
            f"When the edit button is pressed on note seen, the msg should be here"
        )
        return None

    note_id = query.data.replace("edit_note_", "")

    text = (
        f"📝 To edit this note, please send the following command:\n\n"
        f"<code>/edit_note {note_id}</code>\n\n"
        f"Once you send this, I’ll guide you through editing the note. ✨"
    )

    await msg.reply_html(text)


async def handle_transfer_note_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query

    if query is None or query.data is None:
        RanaLogger.warning("Transfer Note button pressed but no callback data found.")
        return

    await query.answer(
        text="🔄 Transfer Note feature is under development. Coming soon! 🛠️",
        show_alert=True,
    )


async def handle_duplicate_note_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query

    if query is None or query.data is None:
        RanaLogger.warning("Duplicate Note button pressed but no callback data found.")
        return

    await query.answer(
        text="📋 Duplicate Note feature will be added in future update. 🚧",
        show_alert=True,
    )
