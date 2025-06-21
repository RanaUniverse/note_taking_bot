"""
When user is trying to find his notes by viewing
This module has the features to shows notes to user.

Here i will keep the code having send the response to user when he want to get his notes
When user will press the buttons and it will handle the callback data.


"""

from typing import Sequence


from telegram import (
    Message,
    User,
    Update,
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from telegram.ext import ContextTypes


from my_modules import bot_config_settings
from my_modules import inline_keyboard_buttons
from my_modules import message_templates

from my_modules.logger_related import RanaLogger

from my_modules.message_templates import WhatMessageAction

from my_modules.database_code import db_functions
from my_modules.database_code.database_make import engine
from my_modules.database_code.models_table import NotePart


NOTES_PER_PAGE = bot_config_settings.NOTES_PER_PAGE
OFFSET_VALUE = bot_config_settings.OFFSET_VALUE
DISLIKE_EFFECT = bot_config_settings.MessageEffectEmojies.DISLIKE.value

USER_HAS_NO_NOTE_KEYBOARD = inline_keyboard_buttons.USER_HAS_NO_NOTE_KEYBOARD
VIEW_ONE_NOTE_DYNAMIC_BUTTON = inline_keyboard_buttons.VIEW_ONE_NOTE_DYNAMIC_BUTTON


async def reply_user_has_no_notes(msg: Message, user: User):
    """
    This function need to call when bot need to say the user
    That he has no note in the database.
    """
    text_no_note = (
        f"😢 <b>Hey {user.mention_html()}</b>! 📭\n\n"
        f"You haven't created any notes yet.\n\n"
        f"✨ Why not get started?\n"
        f"Just send <code>/new_note</code> to create your very first note!\n\n"
        f"🎲 Feeling playful? Try <code>/fake_note</code> or even "
        f"<code>/fake_note 3</code> for some fun sample notes!"
    )

    await msg.reply_html(
        text_no_note,
        message_effect_id=DISLIKE_EFFECT,
        reply_markup=InlineKeyboardMarkup(USER_HAS_NO_NOTE_KEYBOARD),
    )


def text_upper_of_view_notes(how_many_note: int, user: User) -> str:
    """
    When user is viewing all his notes,
    The upper text is getting from it.
    """
    text = (
        f"👋 <b>Hey {user.mention_html()}!</b>\n\n"
        f"🗂️ <b>Total Notes:</b> <code>{how_many_note}</code>\n"
        f"📖 Ready to explore or edit them?\n\n"
        f"👇 Tap a Note's Title below to open it:"
    )

    return text


def make_some_view_notes_button(
    some_notes: Sequence[NotePart],
    how_many_note: int,
    current_page: int = 1,
) -> list[list[InlineKeyboardButton]]:
    """
    When bot will send users some note's Title as button, i need to use this
    This function will make the buttons with the note's Title
    And the callback data will the Note's unique id.
    Here i will pass some Note's Row Object.
    """

    all_buttons: list[list[InlineKeyboardButton]] = []

    for i, note_row in enumerate(iterable=some_notes, start=1):
        title_view = f"{i}. {note_row.note_title}"[0:100]
        # callback_data_value = f"view_note_{note_row.note_id}"
        callback_data_value = (
            f"{VIEW_ONE_NOTE_DYNAMIC_BUTTON.callback_data}{note_row.note_id}"
        )

        one_button_row = [
            InlineKeyboardButton(
                text=title_view,
                callback_data=callback_data_value,
            )
        ]
        all_buttons.append(one_button_row)

    # Next i will need to calculate if i need to say user that
    # all the notes has finished for him or how many page is there

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

    return all_buttons


async def my_notes_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /my_notes :- Privately
    This case first thsi will try to
    First i will try to search the total number of notes row only count,
    I will try to shows some note's to user
    """
    msg = update.effective_message
    user = update.effective_user

    if msg is None or user is None:
        RanaLogger.warning(f"When /my_notes come the msg and user should be present")
        return None

    users_note_count = db_functions.count_user_notes(
        engine=engine,
        user_id=user.id,
    )

    if users_note_count == 0:
        await reply_user_has_no_notes(msg=msg, user=user)
        return None

    some_notes_beginning = db_functions.get_some_note_rows(
        engine=engine,
        offset_value=OFFSET_VALUE,
        limit_value=NOTES_PER_PAGE,
        user_id=user.id,
    )

    some_notes_buttons = make_some_view_notes_button(
        some_notes=some_notes_beginning,
        how_many_note=users_note_count,
    )

    reply_text = text_upper_of_view_notes(
        how_many_note=users_note_count,
        user=user,
    )

    await msg.reply_html(
        text=reply_text,
        reply_markup=InlineKeyboardMarkup(some_notes_buttons),
        do_quote=True,
    )


async def handle_my_all_notes_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    This functions logics are same as /my_notes.
    This Below Button Pressing trigger this function.

    VIEW_ALL_NOTE_BUTTON = InlineKeyboardButton(
        text="🗒️ View All Notes",
        callback_data="my_all_notes",
    )
    """

    user = update.effective_user
    msg = update.effective_message
    if msg is None or user is None:
        RanaLogger.warning(f"user msg should be present on the button pressed")
        return None

    query = update.callback_query
    if query is None:
        RanaLogger.warning(f"Query should be present of press button of 'all_my_notes'")
        return None

    await query.answer(text="I am checking your Notes Now.")

    how_many_notes_user_has = db_functions.count_user_notes(
        engine=engine,
        user_id=user.id,
    )

    if how_many_notes_user_has == 0:
        await reply_user_has_no_notes(msg=msg, user=user)
        return None

    some_notes = db_functions.get_some_note_rows(
        engine=engine,
        offset_value=OFFSET_VALUE,
        limit_value=NOTES_PER_PAGE,
        user_id=user.id,
    )

    notes_buttons = make_some_view_notes_button(
        some_notes=some_notes,
        how_many_note=how_many_notes_user_has,
    )

    reply_text = text_upper_of_view_notes(
        how_many_note=how_many_notes_user_has,
        user=user,
    )

    await msg.reply_html(
        text=reply_text,
        reply_markup=InlineKeyboardMarkup(notes_buttons),
        do_quote=True,
    )


async def button_for_view_one_note(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    The Note't Title Buttons which also assign the note_id,
    When those button is pressed this fun is executs.
        `pattern=r"^view_note_.*$",`

    callback_data_value = f"view_note_{note_row.note_id}"
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
            "Note Title, button include the callback data, if not "
            "means something bad happens in title callback data."
        )
        return None

    note_id = callback_data.removeprefix("view_note_")

    # This upper value should be the note_id which i need to serach on the database

    note_row = db_functions.note_obj_from_note_id(
        engine=engine,
        note_id=note_id,
    )

    if note_row is None:
        text = (
            f"🚫 <b>Note Not Accessible</b>\n\n"
            f"😢 This note is no longer available.\n"
            f"It might have been 🗑️ <b>deleted</b> or there was an ⚠️ "
            f"<b>unexpected issue</b>.\n\n"
            f"🗂️ You can browse your other notes using /my_notes.\n"
            f"🆘 For help, contact the admin or visit /help."
        )
        await msg.reply_html(text)
        return None

    # Below part will execute when note id match the value and user note row get.

    # i will check the owner for a security step, though i dont see any need

    if note_row.user_id != user.id:
        RanaLogger.warning(
            f"{user.id} {user.full_name} Pressed to get the view note."
            "When Note's Title button is pressed the "
            "note owner should pressed as for now"
        )

        text_no_permission_to_view = message_templates.access_denied_messages(
            user=user,
            what_action=WhatMessageAction.VIEW,
        )

        await msg.reply_html(text_no_permission_to_view)
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
        f"🆔 <b>Note ID:</b> <code>{note_row.note_id}</code>\n\n"
        f"📝 <b>Note Details:</b>\n\n"
        f"🕒 <b>Created On:</b> {created_time}\n\n"
        f"🛠 <b>Last Edited:</b> {edited_time}\n\n"
        f"👇👇👇👇👇\n\n"
        f"📌 <b>Title:</b> \n{note_row.note_title}\n\n"
        f"📖 <b>Content:</b>\n{note_row.note_content}\n\n"
        f"Below BUttons is in Development will not work maybe"
    )

    keyboard_view_note = inline_keyboard_buttons.generate_buttons_with_note_view(
        note_id=note_row.note_id
    )

    # 🔍 Check if text exceeds Telegram's 4000-character limit
    if len(text) > 4000:
        text = text[: 4000 - 100]
        text += (
            "\n\n⚠️ This message exceeds the limit and was truncated. "
            "Please View This Full Note in Export Mode"
        )

    await msg.reply_html(
        text=text,
        do_quote=True,
        reply_markup=InlineKeyboardMarkup(keyboard_view_note),
    )


async def button_for_next_page(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    `next_page_ int value ` is the callback data.

                callback_data=f"next_page_{next_page}",

    When user will press the next button to see more extra notes user want to see
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

    if not callback_data.startswith("next_page_"):
        RanaLogger.warning(
            "Unexpected callback data format when getting next page "
            "button pressed by the user it should has 'next_page_' as beginning"
        )
        something_wrong = (
            f"Here is somethings wrong with the button please contact admin."
        )
        await msg.reply_html(text=something_wrong)
        return None

    try:
        current_page = int(callback_data.split("_")[-1])
    except Exception as _:
        RanaLogger.error(
            "in the next_page in view note the value must need to be a int value."
        )
        something_wrong = (
            f"Here is somethings wrong with the button please contact admin."
        )
        await msg.reply_html(text=something_wrong)
        return None

    OFFSET_VALUE = (current_page - 1) * NOTES_PER_PAGE

    some_notes = db_functions.get_some_note_rows(
        engine=engine,
        offset_value=OFFSET_VALUE,
        limit_value=NOTES_PER_PAGE,
        user_id=user.id,
    )

    if len(some_notes) == 0:
        await msg.reply_html("📭 You have no More Extra Saved notes.")
        return None

    total_notes = db_functions.count_user_notes(engine=engine, user_id=user.id)

    total_pages = (total_notes + NOTES_PER_PAGE - 1) // NOTES_PER_PAGE

    text = (
        f"👤 Hello <b>{user.mention_html()}</b>,\n\n"
        f"📄 Page <b>{current_page}</b> of <b>{total_pages}</b>\n"
        f"🗒️ Displaying <b>{len(some_notes)}</b> notes out of "
        f"<b>{total_notes}</b> total.\n\n"
        f"Select a note below to view its details."
    )

    all_buttons = make_some_view_notes_button(
        some_notes=some_notes,
        how_many_note=total_notes,
        current_page=current_page,
    )

    await msg.reply_html(
        text=text,
        reply_markup=InlineKeyboardMarkup(all_buttons),
    )


async def button_for_no_more_notes(
    update: Update,
    cotnext: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Callback Data: `no_more_notes_`
        callback_data=f"no_more_notes_{how_many_note}",

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
        RanaLogger.warning(
            "The query should be a button attached with no more notes left."
        )
        return None

    if query.data.startswith("no_more_notes_"):
        note_count = int(query.data.split("_")[-1])

    else:
        note_count = 0
        RanaLogger.warning("Current page should not be 1 ever as i can think")
        text = f"Some Problem occured here in the system."
        await query.answer(text)

    text = (
        f"You Have just own {note_count} Numbers of Notes. \n"
        f"Please Make More if you want."
    )

    await query.answer(text, show_alert=True)


async def handle_edit_note_button(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
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
        f"Once you send this, I'll guide you through editing the note. ✨"
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
