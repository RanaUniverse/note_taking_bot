"""
This will a edit note features, where user can
Edit his own note.


    context.user_data["old_note_id"] = note_id
    context.user_data["old_note_title"] = note_row.note_title
    context.user_data["old_note_content_preview"] = content_preview

    context.user_data["new_note_title"] = user_text
    context.user_data["new_note_content"] = user_msg_html


"""

import html


from telegram import Update
from telegram import (
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)

from telegram.constants import ParseMode

from telegram.ext import ContextTypes
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)


from my_modules import bot_config_settings

from my_modules import inline_keyboard_buttons
from my_modules.inline_keyboard_buttons import (
    CANCEL_EDIT_NOTE_CONV_BUTTON,
    DELETE_NOTE_BUTTON,
    EDIT_TITLE_BUTTON,
    EDIT_CONTENT_BUTTON,
    SAVE_CHANGES_BUTTON,
)

from my_modules import message_templates

from my_modules.database_code import db_functions
from my_modules.database_code.database_make import engine

from my_modules.logger_related import RanaLogger

from my_modules.message_templates import WhatMessageAction

from my_modules.some_inline_keyboards import note_del_confirmation_button

SELECT_OPTION, TITLE, CONTENT, CONFIRMATION = range(4)


MAX_TITLE_LEN = bot_config_settings.MAX_TITLE_LEN
MAX_CONTENT_LEN = bot_config_settings.MAX_CONTENT_LEN

# i will insert this to bot config settings value
NOTE_PREVIEW_CHAR_LIMIT = 100


def generate_content_preview(full_content: str, char_limit: int = 100) -> str:
    return (
        full_content
        if len(full_content) <= char_limit
        else full_content[:char_limit] + "..."
    )


async def edit_note_cmd_no_args(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """
    When user will only send /edit_note without anything else
    this function will execute it will say him to how to use this.
    context.args is the length of 0.
    """

    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None:
        RanaLogger.warning(f"/edit_note without args, it should has user and msg obj")
        return ConversationHandler.END

    text = (
        f"⚠️ <b>Missing Note ID</b>\n\n"
        f"Hello {user.mention_html()}, you didn’t specify <u>which note</u> "
        f"you want to edit.\n\n"
        f"🛠️ To edit a note, please provide the note ID right after the command.\n\n"
        f"✅ Example usage:\n"
        f"<code>/edit_note NOTE123</code>\n\n"
        f"🔍 Or, visit your notes and use the <b>EDIT NOTE</b> button after opening a note.\n\n"
        f"📌 Please try again!"
    )

    buttons = inline_keyboard_buttons.EDIT_NOTE_KEYBOARD

    await msg.reply_html(
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons),
    )

    return ConversationHandler.END


async def edit_note_cmd_many_args(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """'
    When user will send /edit_note a b c
    It will just inform user that user send unvalid response.
    """

    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None:
        RanaLogger.warning("edit_note_cmd_many_args missing user or msg.")
        return ConversationHandler.END

    text = (
        f"⚠️ <b>Too Many Arguments</b>\n\n"
        f"Hello {user.mention_html()}, you've passed too many values after "
        f"<code>/edit_note</code>. "
        f"This command expects <b>exactly one</b> argument — the <u>note ID</u> "
        f"you want to edit.\n\n"
        f"✅ Example usage:\n"
        f"<code>/edit_note NOTE123</code>\n\n"
        f"You can also Open Your note and edit directly.\n"
        f"Please try again with just the note ID."
    )
    buttons = inline_keyboard_buttons.EDIT_NOTE_KEYBOARD

    await msg.reply_html(text=text, reply_markup=InlineKeyboardMarkup(buttons))
    return ConversationHandler.END


async def edit_note_cmd_one_arg(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """
    `/edit_note NOTE_ID`
    This upper is the format of response this function will execute.
    Only 1 argument value this fun will take to start.
    """
    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None:
        RanaLogger.warning(f"/edit_note one_arg, it should has user and msg obj")
        return ConversationHandler.END

    if context.args is None:
        RanaLogger.warning(
            "On send /edit_note 1_value the context.args should has some value of list"
        )
        return ConversationHandler.END

    note_id = context.args[0]
    note_row = db_functions.note_obj_from_note_id(
        engine=engine,
        note_id=note_id,
    )

    if note_row is None:
        text = message_templates.generate_no_note_found_with_note_id(note_id)
        await msg.reply_html(text=text)
        return ConversationHandler.END

    # Below is execute when note_row is present
    owner_id = note_row.user_id

    if user.id != owner_id:
        text = message_templates.access_denied_messages(
            user=user,
            what_action=WhatMessageAction.EDIT,
        )
        await msg.reply_html(text=text)
        return ConversationHandler.END

    # Below part is the greatest part which is my main logic to do the note edit
    # i am thinking to keep the note's id to be in the dict so that i can know which note
    # i need to edit and what to do with this.

    content_full = f"{note_row.note_content}"
    if len(content_full) <= 100:
        content_preview = content_full
    else:
        content_preview = content_full[:100] + "..."

    content_preview = generate_content_preview(
        full_content=content_full,
        char_limit=NOTE_PREVIEW_CHAR_LIMIT,
    )
    if context.user_data is None:
        RanaLogger.warning(
            f"User Data Must be a empty list atleast not none when "
            f"editing note, Because this edit converstaion has now start only"
        )
        return ConversationHandler.END

    context.user_data["old_note_id"] = note_id
    context.user_data["old_note_title"] = note_row.note_title
    context.user_data["old_note_content_preview"] = content_preview

    reply_text = (
        f"Hello {user.mention_html()}, "
        f"Below is Your Old Note Content 🙋\n\n"
        f"<u>TITLE</u>: {note_row.note_title}\n\n"
        f"<u>CONTENT</u>: {content_preview}\n\n"
        f"Please select one of the buttons below to edit your note.\n"
        f"You can also send /cancel or press the 'Cancel Now' button to Exit Note Editing."
    )

    button = inline_keyboard_buttons.EDIT_NOTE_CONV_KEYBOARD

    await msg.reply_html(
        text=reply_text,
        reply_markup=InlineKeyboardMarkup(button),
    )
    return SELECT_OPTION


async def cancel_fallbacks_by_cmd(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """
    During the note editing time if user press the /cancel
    This will stop the note editing process and stop this.
    """
    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None:
        RanaLogger.warning("in conversation of edit note the msg and user is must need")
        return ConversationHandler.END

    if context.user_data is None:
        RanaLogger.warning(
            f"Context .user data at least is a empty "
            "dict, also i passed the note_id in the "
            "context.user data should exists when starting the note editing"
        )
        return ConversationHandler.END

    RanaLogger.info(
        f"📝 User ({user.name}) Stopped His Note Making. "
        f"Data Removed: {context.user_data}"
    )

    context.user_data.clear()

    text = (
        f"🛑 You've successfully canceled the note editing process.\n\n"
        f"If you'd like to continue editing later, just use the command:\n"
        f"<code>/edit_note &lt;NOTE_ID&gt;</code>\n\n"
        f"Your current editing data has been safely cleared 🧹"
    )

    await msg.reply_html(text=text)
    return ConversationHandler.END


async def cancel_fallbacks_by_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    When the Cancel Editing Note
    Button has been pressed this will executes.
    Callback Data:- `cancel_edit_note_conv`

    """
    query = update.callback_query
    msg = update.effective_message
    user = update.effective_user

    if query is None or query.data is None:
        RanaLogger.warning(
            f"When cancel edit note button is pressed "
            "callback query data should exists"
        )
        return ConversationHandler.END

    if msg is None or user is None:
        RanaLogger.warning(
            f"When cancel note is pressed the user, msg must need to present."
        )
        return ConversationHandler.END

    if query.data != f"{CANCEL_EDIT_NOTE_CONV_BUTTON.callback_data}":
        RanaLogger.warning(f"Button data is must need 'cancel_edit_note_conv'")
        await msg.reply_html(
            f"Some Query's Data has some issue but this edit "
            f"Note conversation has just ended."
        )
        return ConversationHandler.END

    await query.answer("You have pressed Cancel Button")

    if context.user_data is None:
        RanaLogger.warning(
            "Context.user_data should be empty dict or some value "
            "if the user has some edit beforehand"
        )
        return ConversationHandler.END

    RanaLogger.info(
        f"📝 User ({user.name})(TG ID: {user.id}) Stopped His Note Making. "
        f"Data Removed: {context.user_data}"
    )
    note_id = context.user_data.get("old_note_id", None)

    if note_id is None:
        new_text = (
            f"❌ You've canceled the note editing process.\n\n"
            f"ℹ️ This session appears to be old or incomplete, "
            f"but your editing session has still been safely closed.\n\n"
            f"You can restart editing any note by using:\n"
            f"<code>/edit_note &lt;NOTE_ID&gt;</code> 📝"
        )
    else:
        new_text = (
            f"❌ You've canceled the note editing process.\n\n"
            f"🧹 Your editing session has been safely closed.\n\n"
            f"If you'd like to resume editing, just run:\n"
            f"<code>/edit_note {note_id}</code> 📝"
        )

    context.user_data.clear()

    await query.edit_message_text(text=new_text, parse_mode=ParseMode.HTML)

    return ConversationHandler.END


async def get_note_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Handles the input when the user is in the 'Title' state.
    If a valid title String is provided, it is saved in context.user_data.
    Rejects when long titles and guides the user accordingly.
    I decided not to keep store any Formatting in title part.
    """

    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None:
        RanaLogger.warning(
            "when i got text msg for note title "
            "it should be present the user and msg"
        )
        return ConversationHandler.END

    user_text = html.escape(f"{msg.text}")

    if len(user_text) > MAX_TITLE_LEN:
        text = (
            f"The New Note Title exceed {MAX_TITLE_LEN} characters. "
            f"So i cannot take this note title, please resend me "
            f"note title in the limit of "
            f"{MAX_TITLE_LEN} Characters."
        )
        await msg.reply_html(text)
        return TITLE

    # else: i dont use else, as when title is in good condition it will executes below line.

    if context.user_data is None:
        RanaLogger.warning(
            f"User Data Must be a empty list atleast not none "
            "when new note title get by the user in edit note"
        )
        return ConversationHandler.END

    old_title = context.user_data.get("old_note_title", "Unknown Title")

    context.user_data["new_note_title"] = user_text

    reply_text = (
        f"🙋‍♂️ Hello {user.mention_html()}, here's your note info:\n\n"
        f"📝 <b>Old Title:</b> <i>{old_title}</i>\n\n"
        f"✨ <b>New Title:</b> {user_text}\n\n"
        f"Please choose what you'd like to do next using the buttons below.\n"
        f"You can also send /cancel or press 'Cancel Now' Button to exit.\n"
        f"👇👇👇👇👇"
    )

    button = inline_keyboard_buttons.EDIT_NOTE_CONV_KEYBOARD

    await msg.reply_html(text=reply_text, reply_markup=InlineKeyboardMarkup(button))

    return SELECT_OPTION


async def get_note_content(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    This time user got a new message to save it as the note content.
    I will also not store full text with html formatting in the content.
    """

    msg = update.effective_message
    user = update.effective_user

    if user is None or msg is None:
        RanaLogger.warning(
            "I got new content of my note so this time "
            "i should has the user and msg exists"
        )
        return ConversationHandler.END

    user_text = html.escape(f"{msg.text}")

    if len(user_text) > MAX_CONTENT_LEN:
        text = (
            f"⚠️ Your note content is too long! Please keep "
            f"it within {MAX_CONTENT_LEN} characters."
            f"Please resend your note's content properly "
            f"in {MAX_CONTENT_LEN} characters "
            f"Please send the new content again below.\n"
            f"👇👇👇👇👇"
        )

        await msg.reply_html(text)
        return CONTENT

    if context.user_data is None:
        RanaLogger.warning(
            "User data must not be None, should be at least an empty dictionary. "
            "When the new contetn is get in the edit note"
        )
        return ConversationHandler.END

    old_content_preview = context.user_data.get(
        "old_note_content_preview",
        "Unable To Fetch Old Content.",
    )

    context.user_data["new_note_content"] = user_text

    reply_text = (
        f"🙋‍♂️ Hello {user.mention_html()}, here's your note info:\n\n"
        f"📄 <b>OLD Note Content Preview:</b>\n<i>{old_content_preview}\n\n</i>"
        f"New NOTE CONTENT: {user_text}\n\n"
        f"Please choose what you'd like to do next using the buttons below.\n"
        f"You can also send /cancel or press 'Cancel Now' Button to exit.\n"
        f"👇👇👇👇👇"
    )

    button = inline_keyboard_buttons.EDIT_NOTE_CONV_KEYBOARD

    await msg.reply_html(text=reply_text, reply_markup=InlineKeyboardMarkup(button))

    return SELECT_OPTION


async def note_edit_confirmation_yes(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    when user will send "YES"
    it will save the sended edited note's title & content
    """
    msg = update.effective_message
    user = update.effective_user

    if msg is None or user is None:
        RanaLogger.warning(
            "on YES button or text got it should be present the msg and user"
        )
        return ConversationHandler.END

    user_msg = msg.text

    if user_msg == "YES":
        text = f"Your note has been edited successfully"
        await msg.reply_html(text)
        return ConversationHandler.END

    return ConversationHandler.END


async def note_edit_confirmation_no(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Handles the user's "NO" response, indicating they do not want to save the edited note.
    """
    msg = update.effective_message
    user = update.effective_user

    if msg is None or user is None:
        RanaLogger.warning("On NO response, both msg and user should be present.")
        return ConversationHandler.END

    user_msg = msg.text

    if user_msg == "NO":
        text = "Your note edit has been canceled."
        await msg.reply_html(text)
        return ConversationHandler.END

    return ConversationHandler.END


async def bad_note_title_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    When user need text based titel but user send /command this will come
    """
    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None:
        RanaLogger.warning(
            f"When user send wrong command in title user and msg should be exists."
        )
        return ConversationHandler.END

    text = (
        f"Hello {user.mention_html()}, you have only send me a command ({msg.text_html}) "
        f"But i need a real text to save as title in {MAX_TITLE_LEN} characters."
    )
    await msg.reply_html(text=text)
    return TITLE


async def bad_note_title_other_type(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    When user need title as text but user send anything else this will come
    """
    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None:
        RanaLogger.warning(f"it need text for note's title, but user send others")
        return ConversationHandler.END

    if msg.text:
        text = (
            f"You Send a Text But this is not checking for now. "
            "Some issue is here please contact admin or /help"
        )
    else:
        text = (
            f"Hello {user.mention_html()}, "
            "I just need text, "
            "just send me text"
            "So Please Send me normal Text or Emojies."
        )

    await msg.reply_html(text=text)
    return TITLE


async def bad_note_content_cmd(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    This is when need content but user send content wrong as in /command
    """

    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None:
        RanaLogger.warning(
            f"When user send wrong command in content user and msg should be exists."
        )
        return ConversationHandler.END

    text = (
        f"Hello {user.mention_html()}, you have only send me a command ({msg.text_html}) "
        f"But i need a real text to save as content in {MAX_CONTENT_LEN} characters."
    )
    await msg.reply_html(text=text)
    return TITLE


async def bad_note_content_other_type(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    when user need content but got differnt update of filters.ALL it will come
    """

    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None:
        RanaLogger.warning(f"it need text for note's title, but user send others")
        return ConversationHandler.END

    if msg.text:
        text = (
            f"You Send a Text But this is not checking for now. "
            "Some issue is here please contact admin or /help"
        )
    else:
        text = (
            f"Hello {user.mention_html()}, "
            "I just need text, "
            "just send me text"
            "So Please Send me normal Text or Emojies."
        )
    await msg.reply_html(text)

    return CONTENT


async def bad_note_confirmation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    user need yes or no from keyboard but user send different thigns
    """
    if update.effective_message is None:
        RanaLogger.warning("when user need yes no it need good why wrng")
        return ConversationHandler.END

    text = (
        f"Please Just send me 'Yes' or 'No', or /cancel. "
        f"Another Way Please try again with the buttons 👇🏽"
    )
    await update.effective_message.reply_html(text)
    return CONFIRMATION


async def select_option_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:

    query = update.callback_query
    msg = update.effective_message
    user = update.effective_user

    if query is None or query.data is None:
        RanaLogger.warning(
            "Selecting any Editing Button must need to have some "
            "Query's Callback Data present"
        )
        return ConversationHandler.END

    if msg is None or user is None:
        RanaLogger.warning(
            f"On going to select option it must need to have" "the user and msg object"
        )
        return ConversationHandler.END

    callback_data = query.data

    # This Need to Remove.
    await query.answer(f"'{callback_data}' is the value of callback data.")

    if context.user_data is None:
        RanaLogger.warning(
            "On all the callback query of note edit related always the "
            "context.user_data dictionary must need to present."
        )
        return ConversationHandler.END

    button = [
        [
            InlineKeyboardButton(
                text=f"Save Current State",
                callback_data="save_now",
            )
        ],
        [
            InlineKeyboardButton(
                text=f"Cancel Now",
                callback_data="cancel",
            )
        ],
    ]

    if callback_data == f"{EDIT_TITLE_BUTTON.callback_data}":
        old_title = context.user_data.get("old_note_title", "Unknown Title")
        text = (
            f"📝 <b>Old Title:</b> <i>{old_title}</i>\n\n"
            f"✏️ Please send the <b><u>new title</u></b> you'd "
            f"like to update your note with.\n\n"
            f"👇👇👇👇👇"
        )
        await query.edit_message_text(text=text, parse_mode=ParseMode.HTML)
        return TITLE

    elif callback_data == f"{EDIT_CONTENT_BUTTON.callback_data}":
        old_content_preview = context.user_data.get(
            "old_note_content_preview", "No preview available."
        )
        text = (
            f"📄 <b>Old Content Preview:</b>\n"
            f"<i>{old_content_preview}</i>\n\n"
            f"🖊️ Please send the <b><u>new content</u></b> you'd "
            f"like to update your note with.\n\n"
            f"👇👇👇👇👇"
        )
        await query.edit_message_text(text=text, parse_mode=ParseMode.HTML)
        return CONTENT

    elif callback_data == f"{DELETE_NOTE_BUTTON.callback_data}":

        note_id = context.user_data.get("old_note_id", None)

        if note_id is None:
            text = (
                "Here is Some Server Problem To find the Note Id to delete. "
                "Please Restart."
            )
            RanaLogger.warning(text)
            await msg.reply_html(text)
            return ConversationHandler.END

        title = context.user_data.get(
            "old_note_title",
        )
        content = context.user_data.get(
            "old_note_content_preview",
        )

        text = (
            f"🆔 <b>Note ID:</b> <code>{note_id}</code>\n\n"
            f"📝 <b>Note Details:</b>\n\n"
            f"{'👇' * 10}\n\n"
            f"📌 <b>Title:</b> \n{title}\n\n"
            f"📖 <b>Content Preview:</b>\n{content}\n\n"
        )

        delete_buttons = note_del_confirmation_button(note_id=note_id)

        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(delete_buttons),
            parse_mode=ParseMode.HTML,
        )
        return ConversationHandler.END

    elif callback_data == f"{CANCEL_EDIT_NOTE_CONV_BUTTON.callback_data}":

        note_id = context.user_data.get("old_note_id", None)

        if note_id is None:
            text = (
                f"Note ID Not Found \n"
                f"Maybe The Session Has Been Ended Already.\n"
                f"❌ <b>Note Editing Canceled</b>\n\n"
                f"🛑 You have exited the note editing process.\n"
                f"Feel free to start again with:\n"
                f"<code>/edit_note &lt;NOTE_ID&gt;</code>"
            )

        text = (
            f"❌ <b>Note Editing Canceled</b>\n\n"
            f"🛑 You have exited the note editing process.\n"
            f"🆔 <b>Note ID:</b> <code>{note_id}</code>\n\n"
            f"Don't worry, your original note remains unchanged.\n\n"
            f"👉 You can resume editing later using:\n"
            f"<code>/edit_note {note_id}</code>\n\n"
            f"Or simply explore other options from the menu."
        )

        await msg.reply_html(text=text, reply_markup=InlineKeyboardMarkup(button))
        return ConversationHandler.END

    elif callback_data == f"{SAVE_CHANGES_BUTTON.callback_data}":

        yes_no_reply_keyboard = [
            [
                KeyboardButton(text="Yes"),
                KeyboardButton(text="No"),
            ],
            [
                KeyboardButton(text="/cancel"),
            ],
        ]

        text_waiting = "Changes ready. Awaiting confirmation..."
        await query.edit_message_text(
            text=text_waiting,
            parse_mode=ParseMode.HTML,
        )

        new_title = context.user_data.get("new_note_title", "No New Title Provided")

        new_content = context.user_data.get("new_note_content", "Content Unavailable")

        text_ask = (
            f"🙋‍♂️ <b>Here is your updated note:</b>\n\n"
            f"📝 <b>New Title:</b> <i>{new_title}</i>\n\n"
            f"📄 <b>New Content:</b>\n"
            f"<i>{new_content}</i>\n\n"
            f"💾 <b>Would you like to save these changes?</b>\n\n"
            f"✅ Send <b>'Yes'</b> to save\n"
            f"❌ Send <b>'No'</b> to cancel\n"
            f"🚫 Or press /cancel to exit"
        )

        await msg.reply_html(
            text=text_ask,
            reply_markup=ReplyKeyboardMarkup(
                yes_no_reply_keyboard,
                resize_keyboard=True,
                one_time_keyboard=True,
            ),
        )

        return CONFIRMATION

    else:
        text = f"Not Valid Response For Now Please Contact Admin."
        await msg.reply_html(text=text, reply_markup=InlineKeyboardMarkup(button))
        return ConversationHandler.END


edit_note_conv = ConversationHandler(
    entry_points=[
        CommandHandler(
            command="edit_note",
            callback=edit_note_cmd_no_args,
            filters=filters.ChatType.PRIVATE & filters.UpdateType.MESSAGE,
            block=False,
            has_args=0,
        ),
        CommandHandler(
            command="edit_note",
            callback=edit_note_cmd_one_arg,
            filters=filters.ChatType.PRIVATE & filters.UpdateType.MESSAGE,
            block=False,
            has_args=1,
        ),
        CommandHandler(
            command="edit_note",
            callback=edit_note_cmd_many_args,
            filters=filters.ChatType.PRIVATE & filters.UpdateType.MESSAGE,
            block=False,
            has_args=None,
        ),
        CallbackQueryHandler(
            callback=cancel_fallbacks_by_button,
            pattern=f"{CANCEL_EDIT_NOTE_CONV_BUTTON.callback_data}",
        ),
    ],
    states={
        SELECT_OPTION: [
            # Handler for editing the title
            CallbackQueryHandler(
                callback=select_option_handler,
                pattern=f"{EDIT_TITLE_BUTTON.callback_data}",
            ),
            # Handler for editing the content
            CallbackQueryHandler(
                callback=select_option_handler,
                pattern=f"{EDIT_CONTENT_BUTTON.callback_data}",
            ),
            # Handler for exporting the note (any note id)
            CallbackQueryHandler(
                callback=select_option_handler,
                pattern=f"{DELETE_NOTE_BUTTON.callback_data}",
            ),
            # Handler for SAVE CHANGES NOW
            CallbackQueryHandler(
                callback=select_option_handler,
                pattern=f"{SAVE_CHANGES_BUTTON.callback_data}",
            ),
            # Handler for canceling via the command "/cancel"
            CommandHandler(
                command="cancel",
                callback=cancel_fallbacks_by_cmd,
                filters=filters.COMMAND
                & filters.ChatType.PRIVATE
                & filters.UpdateType.MESSAGE,
            ),
            # Handler for canceling via a callback with cancel button
            CallbackQueryHandler(
                callback=cancel_fallbacks_by_button,
                pattern=f"{CANCEL_EDIT_NOTE_CONV_BUTTON.callback_data}",
            ),
        ],
        TITLE: [
            CommandHandler(
                command="cancel",
                callback=cancel_fallbacks_by_cmd,
                filters=filters.COMMAND
                & filters.ChatType.PRIVATE
                & filters.UpdateType.MESSAGE,
            ),
            CallbackQueryHandler(
                callback=cancel_fallbacks_by_button,
                pattern=f"{CANCEL_EDIT_NOTE_CONV_BUTTON.callback_data}",
            ),
            MessageHandler(
                filters=filters.Command(),
                callback=bad_note_title_cmd,
                block=False,
            ),
            MessageHandler(
                filters=filters.TEXT
                & filters.ChatType.PRIVATE
                & filters.UpdateType.MESSAGE,
                callback=get_note_title,
                block=False,
            ),
            MessageHandler(
                filters=filters.ALL,
                callback=bad_note_title_other_type,
                block=False,
            ),
        ],
        CONTENT: [
            CommandHandler(
                command="cancel",
                callback=cancel_fallbacks_by_cmd,
                filters=filters.COMMAND
                & filters.ChatType.PRIVATE
                & filters.UpdateType.MESSAGE,
            ),
            CallbackQueryHandler(
                callback=cancel_fallbacks_by_button,
                pattern=f"{CANCEL_EDIT_NOTE_CONV_BUTTON.callback_data}",
            ),
            MessageHandler(
                filters=filters.Command(),
                callback=bad_note_content_cmd,
                block=False,
            ),
            MessageHandler(
                filters=filters.TEXT
                & filters.ChatType.PRIVATE
                & filters.UpdateType.MESSAGE,
                callback=get_note_content,
                block=False,
            ),
            MessageHandler(
                filters=filters.ALL,
                callback=bad_note_title_other_type,
                block=False,
            ),
        ],
        CONFIRMATION: [
            CommandHandler(
                command="cancel",
                callback=cancel_fallbacks_by_cmd,
                filters=filters.COMMAND
                & filters.ChatType.PRIVATE
                & filters.UpdateType.MESSAGE,
                block=False,
            ),
            MessageHandler(
                filters=filters.Text(["Yes", "/yes"]),
                callback=note_edit_confirmation_yes,
                block=False,
            ),
            MessageHandler(
                filters=filters.Text(["No", "/no"]),
                callback=note_edit_confirmation_no,
                block=False,
            ),
            MessageHandler(
                filters=filters.ALL,
                callback=bad_note_confirmation,
                block=False,
            ),
        ],
    },
    fallbacks=[
        CommandHandler(
            command="cancel",
            callback=cancel_fallbacks_by_cmd,
            filters=filters.COMMAND
            & filters.ChatType.PRIVATE
            & filters.UpdateType.MESSAGE,
            block=False,
        ),
        CallbackQueryHandler(
            callback=cancel_fallbacks_by_button,
            pattern=f"{CANCEL_EDIT_NOTE_CONV_BUTTON.callback_data}",
        ),
    ],
)
