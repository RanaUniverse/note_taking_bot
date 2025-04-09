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

# from sqlmodel import (
#     select,
#     Session,
# )

import asyncio

import html

from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from telegram.constants import ParseMode

from telegram.ext import ContextTypes

from my_modules.logger_related import RanaLogger

from my_modules.database_code.database_make import engine

# from my_modules.database_code.models_table import NotePart
from my_modules.database_code import db_functions


NOTES_PER_PAGE: int = 5
OFFSET_VALUE = 0


async def all_notes_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /my_notes /all_notes /n
    First i will try to search the total number of notes row only count
    2nd i will try to get full some row's data completely so that i can work with this
    """
    user = update.effective_user
    if not user:
        return

    msg = update.effective_message
    if msg is None:
        return

    all_note_count = db_functions.count_user_notes(
        engine=engine,
        user_id=user.id,
    )

    notes = db_functions.get_user_notes(
        engine=engine,
        offset_value=OFFSET_VALUE,
        limit_value=NOTES_PER_PAGE,
        user_id=user.id,
    )

    if all_note_count == 0:
        text = (
            f"Hello <b>{user.mention_html()}</b>, You have not made any note yet. "
            f"Please make a note by sending /new_note ."
            f"If You want a fake note pls send /fake_note or followed by a number."
        )

        await msg.reply_html(text)
        return None

    # This below part is for when a user has some notes row
    text = (
        f"👋 Hello <b>{user.mention_html()}</b>,\n\n"
        f"📊 You have a total of <b>{all_note_count}</b> notes.\n\n"
        f"📝 You can view your notes by pressing the buttons below."
    )

    all_buttons: list[list[InlineKeyboardButton]] = []

    for i, note_row in enumerate(
        iterable=notes,
        start=1,
    ):
        title = f"{i}. {note_row.note_title}"
        note_id = f"{note_row.note_id}"

        button_row = [
            InlineKeyboardButton(
                text=title,
                callback_data=note_id,
            )
        ]
        all_buttons.append(button_row)

    # Here i faced a problem long long time because when below was checking and i was
    # using .limit(NOtesPerPage) it below will not execute ever, so else part will
    # execute always so i need to change some logic,

    if all_note_count > NOTES_PER_PAGE:
        # As this is the starting of the note lists send, so it means it will be start
        # from current page as 1, and nextpage value will be used in the button pressed

        current_page = 1
        next_page = current_page + 1

        next_button = [
            InlineKeyboardButton(
                text=f"More Notes (Page No. {next_page}) →",
                callback_data=f"notes_page_{next_page}",  # Send next page number in query.data
            )
        ]
        all_buttons.append(next_button)

    else:
        end_button = [
            InlineKeyboardButton(
                text="📄 No More Notes",
                callback_data=f"no_more_notes_{all_note_count}",
            )
        ]
        all_buttons.append(end_button)
        # when this upper button will be pressed it will just let the
        # user known that the not more note left in a pop up message

    await msg.reply_html(
        text=text,
        reply_markup=InlineKeyboardMarkup(all_buttons),
        do_quote=True,
    )


async def button_for_search_notes(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    When The Button is pressed on the note's title it will execute and send the
    note back to user. it will check note_id value.
    This will when user want to get his notes which he press on the search notes
    """

    query = update.callback_query

    if query is None:
        RanaLogger.warning(
            f"When user press button on search note, it should have the data."
        )
        return

    await query.answer("Please check Your Note Below.")

    msg = update.effective_message

    if msg is None:
        RanaLogger.warning("When button is pressed this should have the msg obj")
        return None

    # This data is attached with the button user has just pressed

    note_id = query.data

    if note_id is None:
        RanaLogger.warning("Some Problem happens in note_id in query")
        return None

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
            f"It might have been <b>deleted</b> or there was an <b>unexpected issue</b>.\n\n"
            f"📌 Try checking your other notes using /all_notes."
        )
        await msg.reply_html(text)
        return None

    # Below part will execute when note id match the value.
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

    text = (
        f"📝 <b>Note Details:</b>\n\n"
        f"📌 <b>Title:</b> \n{note_row.note_title}\n\n"
        f"📖 <b>Content:</b>\n{note_row.note_content}\n\n"
        f"🕒 <b>Created On:</b> {created_time}\n\n"
        f"🛠 <b>Last Edited:</b> {edited_time}\n\n"
        f"🆔 <b>Note ID:</b> <code>{note_row.note_id}</code>\n\n"
        f"Below BUttons is in Development will not work maybe"
    )

    keyboard_view_note = [
        [
            InlineKeyboardButton(
                "✏️ Edit Note ❌❌❌", callback_data=f"edit_note_{note_row.note_id}"
            ),
            InlineKeyboardButton(
                "🗑️ Delete Note 🟩", callback_data=f"delete_note_{note_row.note_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                "🔄 Transfer Ownership ❌❌❌",
                callback_data=f"transfer_note_{note_row.note_id}",
            ),
            InlineKeyboardButton(
                "📋 Duplicate Note ❌❌❌",
                callback_data=f"duplicate_note_{note_row.note_id}",
            ),
        ],
    ]

    await msg.reply_html(
        text=text,
        do_quote=True,
        reply_markup=InlineKeyboardMarkup(keyboard_view_note),
    )

    # This upper functions is a potential issue, when the last text exceed the
    # 4096 character limit it will raise a error, in future i need to add broke this text


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

    # with Session(engine) as session:
    #     statement = (
    #         select(NotePart)
    #         .where(NotePart.user_id == user.id)
    #         .offset(OFFSET_VALUE)
    #         .limit(NOTES_PER_PAGE)
    #     )
    #     results = session.exec(statement)
    #     notes = results.all()

    notes = db_functions.get_user_notes(
        engine=engine,
        offset_value=OFFSET_VALUE,
        limit_value=NOTES_PER_PAGE,
        user_id=user.id,
    )

    if len(notes) == 0:
        await msg.reply_html("📭 You have no MOre saved notes.")

        return None

    total_notes = db_functions.count_user_notes(engine=engine, user_id=user.id)

    total_pages = (total_notes + NOTES_PER_PAGE - 1) // NOTES_PER_PAGE

    text = (
        f"👤 Hello <b>{user.mention_html()}</b>,\n\n"
        f"📄 Page <b>{current_page}</b> of <b>{total_pages}</b>\n"
        f"🗒️ Displaying <b>{len(notes)}</b> notes out of <b>{total_notes}</b> total.\n\n"
        f"Select a note below to view its details."
    )

    all_buttons: list[list[InlineKeyboardButton]] = []

    for i, note_row in enumerate(
        iterable=notes,
        start=(current_page - 1) * NOTES_PER_PAGE + 1,
    ):
        title = f"{i}. {note_row.note_title}"
        note_id = f"{note_row.note_id}"

        button_row = [
            InlineKeyboardButton(
                text=title,
                callback_data=note_id,
            )
        ]
        all_buttons.append(button_row)

    # Below logic i checked when user's last page shows less than max page
    # note's count it will realize no more notes left and it will say user
    # directly there without showing 'next_page' button, but the problem is
    # it is not fully correct when user's last page reach same amount of notes button

    if len(notes) < NOTES_PER_PAGE:

        end_button = [
            InlineKeyboardButton(
                text="✅ No more notes.",
                callback_data=f"no_more_notes_end_page",
            )
        ]
        all_buttons.append(end_button)

    else:

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


async def button_for_no_more_notes(
    update: Update, cotnext: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    This time when user has no more notes and the last button will pressed by user this
    below funcions logic will be executed and this will run

    For now i though when user will press this it will just say this infromation
    """

    query = update.callback_query

    if query is None:
        RanaLogger.warning(
            f"When user press button on search note, it should have the data."
        )
        return

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

    await query.answer(text)


async def button_for_no_more_notes_last_page(
    update: Update, cotnext: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    This time when user has no more notes and the last button will pressed by user this
    below funcions logic will be executed and this will run

    For now i though when user will press this it will just say this infromation
    """

    query = update.callback_query

    if query is None:
        RanaLogger.warning(
            f"When user press button on search note, it should have the data."
        )
        return

    if query.data is None:
        RanaLogger.warning("The query should be a button attached with next button")
        return None

    text = (
        f"You have reached the end of your Notes.\n"
        f"You have not left any more note for now. 😢"
    )

    await query.answer(
        text=text,
        show_alert=True,
    )


# Below part is for when the buttons includes the view note has been pressed
# Below parts are not developed yet.


async def handle_edit_note_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query

    if query is None or query.data is None:
        RanaLogger.warning("Edit Note button pressed but no callback data found.")
        return

    await query.answer(
        text="✏️ Edit Note feature will be available soon. Stay tuned! 🚧",
        show_alert=True,
    )


async def handle_delete_note_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query

    if query is None or query.data is None:
        RanaLogger.warning("Delete Note button pressed but no callback data found.")
        return

    await query.answer(
        text="🗑️ Please Read all carefully must ⏳",
        show_alert=True,
    )

    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None:
        RanaLogger.warning(
            "When user press delete button of note it should "
            f"have the user and msg obj available"
        )
        return

    note_id = query.data.replace("delete_note_", "")

    note_row = db_functions.note_obj_from_note_id(
        engine=engine,
        note_id=note_id,
    )
    if note_row is None:
        RanaLogger.warning(f"This time the note row should present")
        await msg.reply_html(f"Something wrong the note not found")
        return

    title = f"{note_row.note_title}"

    created = (
        note_row.created_time.strftime("%d %b %Y, %I:%M %p")
        if note_row.created_time
        else "Unknown"
    )

    edited = (
        f"<b>✏️ Last Edited:</b> <code>{note_row.edited_time.strftime('%d %b %Y, %I:%M %p')}</code>\n"
        if note_row.edited_time
        else ""
    )
    text = (
        f"⚠️ <b>Are you sure you want to delete this note?</b>\n\n"
        f"<b>📝 Title:</b> <code>{html.escape(title)}</code>\n"
        f"<b>🕒 Created:</b> <code>{created}</code>\n"
        f"{edited}\n"
        f"🚫 <u>This action is permanent and cannot be undone!</u>\n"
        f"Please confirm your choice below 👇"
    )

    buttons: list[list[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(
                text="✅ Yes, Delete", callback_data=f"note_del_confirm_{note_id}"
            ),
            InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_del"),
        ]
    ]

    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=ParseMode.HTML,
    )


async def confirm_note_del_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    When user press teh delete the note button for a note
    it will execute
    """

    query = update.callback_query

    if query is None or query.data is None:
        RanaLogger.warning(
            "Confirm Delete Note button pressed but no callback data found."
        )
        return

    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None:
        RanaLogger.warning(
            "When user press Confirm delete button of note it should "
            f"have the user and msg obj available"
        )
        return

    note_id = query.data.replace("note_del_confirm_", "")

    waiting_text = (
        f"⏳ Deleting your note... Please wait!\n\n"
        f"Your Request is in processing... \n\n"
        f"Note ID: <code>{note_id}</code>\n"
    )

    msg_waiting = await msg.reply_html(waiting_text)

    await query.answer("Your Request is in Processing ...")

    RanaLogger.warning(
        f"{user.full_name} want to delete the note id of: "
        f"{note_id} by pressing the confirm button attached with the note view"
    )

    note_row = db_functions.note_obj_from_note_id(
        engine=engine,
        note_id=note_id,
    )

    await asyncio.sleep(1)

    if note_row is None:
        text = (
            f"{waiting_text}\n\n"
            "⚠️ <b>Note Not Found</b>\n\n"
            "It looks like this note may have already been deleted or the ID is invalid.\n\n"
            "If you believe this is a mistake, please contact support using /help. 🛠️"
        )
        RanaLogger.warning(
            "Note ID from confirm button should have been valid, but note not found."
        )
        # await msg.reply_html(text=text)
        await msg_waiting.edit_text(text, parse_mode=ParseMode.HTML)

        return None

    delection_confirmation = db_functions.delete_note_obj(
        engine=engine,
        note_id=note_id,
        user_id=user.id,
    )

    if delection_confirmation:
        text = (
            f"{waiting_text}\n\n"
            "✅ <b>Note Deleted Successfully!</b>\n\n"
            "🗑️ Your note has been permanently removed from the database.\n"
            "Please remember, this action cannot be undone.\n\n"
            "If you deleted it by mistake, unfortunately, it's gone for good. 😢"
        )

        # await query.edit_message_text(text=text, parse_mode=ParseMode.HTML)
        await msg_waiting.edit_text(text, parse_mode=ParseMode.HTML)

        await query.edit_message_text(f"Note has been deleted")
        return

    else:

        RanaLogger.warning(
            f"I wish This should not happens because delete fun has been run for notes."
        )
        text = (
            f"{waiting_text}\n\n"
            "⚠️ <b>Deletion Failed</b>\n\n"
            "Something went wrong while trying to delete your note.\n"
            "Please try again later or use <b>/help</b> to contact support. 🛠️"
        )

        # await query.edit_message_text(text=text, parse_mode=ParseMode.HTML)
        # await msg.reply_html(text)
        await msg_waiting.edit_text(text, parse_mode=ParseMode.HTML)
        await msg_waiting.edit_text(
            "It not delete means some internal problem is there."
        )

        return


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
