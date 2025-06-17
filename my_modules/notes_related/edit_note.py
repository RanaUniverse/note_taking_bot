"""
This will a edit note features, where user can
Edit his own note.

"""

import html


from telegram import Update
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
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
from inline_keyboard_buttons import (
    CANCEL_EDIT_NOTE_CONV_BUTTON,
    EDIT_TITLE_BUTTON,
    EDIT_CONTENT_BUTTON,
)

from my_modules import message_templates
from message_templates import WhatMessageAction

from my_modules.database_code import db_functions
from my_modules.database_code.database_make import engine

from my_modules.logger_related import RanaLogger


SELECT_OPTION, TITLE, CONTENT, CONFIRMATION = range(4)


MAX_TITLE_LEN = bot_config_settings.MAX_TITLE_LEN
MAX_CONTENT_LEN = bot_config_settings.MAX_CONTENT_LEN


async def edit_note_cmd_no_args(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """
    When user will only send /edit_note without anything else
    this function will execute it will say him to how to use this.
    """

    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None:
        RanaLogger.warning(f"/edit_note it should has user and msg obj")
        return ConversationHandler.END

    # if len(context.args) == 0:
    # i dont need to check this args len as it will always 0
    # as in i pass in the CommandHandler when refer to this functions
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
    like this many args it will execute
    """

    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None:
        RanaLogger.warning("edit_note_cmd_many_args missing user or msg")
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
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    `/edit_note NOTE_ID`
    This upper is the format of response this function will execute.
    Only 1 argument value this fun will take to start.

    """
    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None:
        RanaLogger.warning(f"/edit_note it should has user and msg obj")
        return ConversationHandler.END

    if context.args is None:
        RanaLogger.warning(
            "On send /edit_note the context.args should has some value of list"
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

    reply_text = (
        f"Hello {user.mention_html()}, you own this note 🙋\n\n"
        f"<u>TITLE</u>: {note_row.note_title}\n\n"
        f"<u>CONTENT</u>: {content_preview}\n\n"
        f"Please select one of the buttons below to edit your note.\n"
        f"You can also send /cancel or press the 'Cancel Now' button to exit editing."
    )

    button = inline_keyboard_buttons.EDIT_NOTE_CONV_KEYBOARD

    if context.user_data is None:
        RanaLogger.warning(
            f"User Data Must be a empty list atleast not none when editing note"
        )
        return ConversationHandler.END

    context.user_data["note_id_of_edited_note"] = note_id
    context.user_data["reply_text"] = reply_text

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
            "context.user data when starting the note editing"
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
        CANCEL_EDIT_NOTE_CONV_BUTTON = InlineKeyboardButton(
            text="Cancel Now",
            callback_data="cancel_edit_note_conv",
        )
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
        RanaLogger.warning(f"The message should be present ")
        return ConversationHandler.END

    if query.data != "cancel_edit_note_conv":
        RanaLogger.warning(f"Button data is must need 'cancel_edit_note_conv'")
        await msg.reply_html(
            f"Some Query's Data has some issue but this edit "
            f"Note conversation has just ended."
        )
        return ConversationHandler.END

    # it means the query data is matched

    await query.answer("You have pressed cancel button")

    if context.user_data is None:
        RanaLogger.warning(
            f"Context .user data at least is a empty "
            "dict, also i passed the note_id in the "
            "context.user data when starting the note editing"
        )
        return ConversationHandler.END

    RanaLogger.info(
        f"📝 User ({user.name}) Stopped His Note Making. "
        f"Data Removed: {context.user_data}"
    )

    new_text = (
        f"❌ You’ve canceled the note editing process By Pressing the Cancel Button.\n\n"
        f"No worries — your session has been stopped. "
        f"Your current editing data has been safely cleared 🧹"
        f"You can always start editing again with the command:\n"
        f"<code>/edit_note &lt;NOTE_ID&gt;</code> 📝"
    )

    # i want to update the message where the button is attached so i did this.
    # i need to make it good design.

    # When a old Message's Button is pressed below will give Default value in .get
    old_text = context.user_data.get("reply_text", "OLD Message Removed.")

    context.user_data.clear()

    updated_text = old_text + "..." + "\n\n\n" + "..." + new_text
    await query.edit_message_text(text=updated_text, parse_mode=ParseMode.HTML)

    return ConversationHandler.END


async def get_note_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    When user will send text it will execute and try to save this in the dictionary first
    Then if it is wrong it will say to send him again
    """

    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None:
        RanaLogger.warning(
            "when i got text msg for note it should be present the user and msg"
        )
        return ConversationHandler.END

    user_text = f"{msg.text}"

    if len(user_text) > MAX_TITLE_LEN:
        text = (
            f"The New Note Title exceed {MAX_TITLE_LEN} characters. "
            f"So i cannot take this note title, please resend me note title in the limit of "
            f"{MAX_TITLE_LEN}."
        )
        await msg.reply_html(text)
        return TITLE

    else:
        if context.user_data is None:
            RanaLogger.warning(f"User Data Must be a empty list atleast not none")
            return ConversationHandler.END

        context.user_data["edit_note_title"] = user_text

        text = f"You have send me a correct title, " f"now please select what you want."

        button = [
            [
                InlineKeyboardButton(
                    text="Edit Title Done Already 🍌🍌🍌",
                    callback_data="edit_title",
                ),
                InlineKeyboardButton(
                    text="Edit Content",
                    callback_data="edit_content",
                ),
            ],
        ]

        await msg.reply_html(text=text, reply_markup=InlineKeyboardMarkup(button))

        return SELECT_OPTION


async def get_note_content(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    This time user got a new message to save it as the note content
    """

    msg = update.effective_message
    user = update.effective_user

    if user is None or msg is None:
        RanaLogger.warning(
            "when i got text msg for note it should be present the user and msg"
        )
        return ConversationHandler.END

    user_msg = msg.text
    user_msg_html = msg.text_html

    if user_msg is None:
        RanaLogger.warning("Content message should not be None.")
        return ConversationHandler.END

    if len(user_msg) > MAX_CONTENT_LEN:
        text = (
            f"⚠️ Your note content is too long! Please keep it within {MAX_CONTENT_LEN} characters."
            f"Please resend your note's content properly in {MAX_TITLE_LEN} characters"
        )

        await msg.reply_html(text)
        return ConversationHandler.END

    else:

        if context.user_data is None:
            RanaLogger.warning(
                "User data must not be None, should be at least an empty dictionary."
            )
            return ConversationHandler.END

        context.user_data["note_content"] = user_msg_html

        return CONFIRMATION


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
            f"Thsi should not happens as thsi is maybe handle "
            f"by the first filters.Text() in the handler"
        )

    # Checking the type of message and responding accordingly
    elif msg.photo:
        text = (
            f"📸 <b>Oops! That's a photo!</b>\n\n"
            f"I need a <b>text message</b> to set as the note's title.\n"
            f"Please send only text here. 📝"
        )
    elif msg.animation:
        text = (
            f"🎞️ <b>Oops! That's an animation (GIF)!</b>\n\n"
            f"I need a simple <b>text message</b> to use as the note title.\n"
            f"Please type and send your title. 📝"
        )
    elif msg.document:
        text = (
            f"📄 <b>Oops! That's a document!</b>\n\n"
            f"A file can't be used as a note title.\n"
            f"Please type the note title and send it as a message. 📝"
        )
    elif msg.game:
        text = (
            f"🎮 <b>Oops! That's a game!</b>\n\n"
            f"I can't use a game as a note title.\n"
            f"Please send only text. 📝"
        )
    elif msg.sticker:
        text = (
            f"🎭 <b>Oops! That's a sticker!</b>\n\n"
            f"I need a text message for the note title, not a sticker.\n"
            f"Please type and send your note title. 📝"
        )
    elif msg.story:
        text = (
            f"📖 <b>Oops! That's a story!</b>\n\n"
            f"A story can't be used as a note title.\n"
            f"Please send only text. 📝"
        )
    elif msg.video:
        text = (
            f"🎥 <b>Oops! That's a video!</b>\n\n"
            f"A video can't be used as a note title.\n"
            f"Please send only text to set your note title. 📝"
        )
    elif msg.voice:
        text = (
            f"🎙️ <b>Oops! That's a voice message!</b>\n\n"
            f"I can't use voice messages for a note title.\n"
            f"Please send only text. 📝"
        )
    elif msg.video_note:
        text = (
            f"📹 <b>Oops! That's a video note!</b>\n\n"
            f"I need a text message, not a video note.\n"
            f"Please type and send the title. 📝"
        )
    elif msg.audio:
        text = (
            f"🎵 <b>Oops! That's an audio file!</b>\n\n"
            f"I need a text input, not an audio file.\n"
            f"Please type the note title and send it as a message. 📝"
        )
    elif msg.poll:
        text = (
            f"📊 <b>Oops! That's a poll!</b>\n\n"
            f"I can't use a poll as a note title.\n"
            f"Please send only text. 📝"
        )
    elif msg.dice:
        text = (
            f"🎲 <b>Oops! That's a dice roll!</b>\n\n"
            f"A dice roll can't be used as a note title.\n"
            f"Please send only text. 📝"
        )
    else:
        text = (
            f"❌ <b>Oops! Unsupported format!</b>\n\n"
            f"I need a simple text message as your note title.\n"
            f"Please type and send the title again. 📝"
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

    # Check if it's a bot command at the beginning
    if (
        msg.entities
        and msg.entities[0].type == "bot_command"
        and msg.entities[0].offset == 0
    ):
        text = (
            "🛠️ This is a command input! Oh sorry, please send "
            f"/cancel to stop this note-making..."
        )
    elif msg.photo:
        text = (
            f"📸 <b>Oops! That's a photo!</b>\n\n"
            f"Currently The Photo cannot be saved as note, stay for update."
        )
    elif msg.animation:
        text = (
            f"🎞️ <b>Oops! That's an animation (GIF)!</b>\n\n"
            f"I need a text message for the note content.\n"
            f"Please type and send your note content. 📝"
        )
    elif msg.document:
        text = (
            f"📄 <b>Oops! That's a document!</b>\n\n"
            f"A file can't be used as note content.\n"
            f"Please type and send the content as a text message. 📝"
        )
    elif msg.game:
        text = (
            f"🎮 <b>Oops! That's a game!</b>\n\n"
            f"I can't use a game as note content.\n"
            f"Please send only text. 📝"
        )
    elif msg.sticker:
        text = (
            f"🎭 <b>Oops! That's a sticker!</b>\n\n"
            f"Stickers can't be used as note content.\n"
            f"Please send text instead. 📝"
        )
    elif msg.story:
        text = (
            f"📖 <b>Oops! That's a story!</b>\n\n"
            f"A story can't be used as note content.\n"
            f"Please send only text. 📝"
        )
    elif msg.video:
        text = (
            f"🎥 <b>Oops! That's a video!</b>\n\n"
            f"Videos aren't supported as note content.\n"
            f"Please send text instead. 📝"
        )
    elif msg.voice:
        text = (
            f"🎙️ <b>Oops! That's a voice message!</b>\n\n"
            f"Voice messages can't be used as note content.\n"
            f"Please type and send your note content as text. 📝"
        )
    elif msg.video_note:
        text = (
            f"📹 <b>Oops! That's a video note!</b>\n\n"
            f"A video note can't be used as note content.\n"
            f"Please type and send your note content. 📝"
        )
    elif msg.audio:
        text = (
            f"🎵 <b>Oops! That's an audio file!</b>\n\n"
            f"I need a text input for the note content.\n"
            f"Please type and send it as a message. 📝"
        )
    elif msg.poll:
        text = (
            f"📊 <b>Oops! That's a poll!</b>\n\n"
            f"A poll can't be used as note content.\n"
            f"Please send only text. 📝"
        )
    elif msg.dice:
        text = (
            f"🎲 <b>Oops! That's a dice roll!</b>\n\n"
            f"A dice roll can't be used as note content.\n"
            f"Please send only text. 📝"
        )
    else:
        text = (
            f"❌ <b>Oops! Unsupported format!</b>\n\n"
            f"I need a simple text message as your note content.\n"
            f"Please type and send the content again. 📝"
        )

    await msg.reply_html(text=text)
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
    await query.answer()  # acknowledge the callback
    option = query.data

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

    if option == "edit_title":
        await query.edit_message_text(
            text="✏️ Please send the new title:",
            reply_markup=InlineKeyboardMarkup(button),
        )
        return TITLE
    elif option == "edit_content":
        await query.edit_message_text(
            text="📝 Please send the new content:",
            reply_markup=InlineKeyboardMarkup(button),
        )
        return CONTENT
    elif option == "delete_note":
        await query.edit_message_text(
            text="🗑️ Confirm deletion of the note, please type 'YES' to proceed or 'NO' to cancel:"
        )
        return CONFIRMATION
    elif option == "export_note":
        await query.edit_message_text(text="📤 Preparing your note for export...")
        # Handle export logic here; you might then end the conversation or redirect the flow.
        return ConversationHandler.END
    elif option == "cancel_conv":
        await query.edit_message_text(text="❌ Note editing canceled.")
        return ConversationHandler.END
    else:
        await query.edit_message_text(text="❓ Unrecognized option. Please try again.")
        return SELECT_OPTION


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
                pattern=r"^edit_title$",
            ),
            # Handler for editing the content
            CallbackQueryHandler(
                callback=select_option_handler,
                pattern=r"^edit_content$",
            ),
            # Handler for exporting the note (any note id)
            CallbackQueryHandler(
                callback=select_option_handler,
                pattern=r"^export_note_.*$",
            ),
            # Handler for deleting the note (any note id)
            CallbackQueryHandler(
                callback=select_option_handler,
                pattern=r"^delete_note_.*$",
            ),
            # Handler for changing ownership (any note id)
            CallbackQueryHandler(
                callback=select_option_handler,
                pattern=r"^owner_change_.*$",
            ),
            # Handler for canceling via the inline button
            CallbackQueryHandler(
                callback=cancel_fallbacks_by_button,
                pattern=r"^cancel_button$",
            ),
            # Handler for canceling via the command "/cancel"
            CommandHandler(
                command="cancel",
                callback=cancel_fallbacks_by_cmd,
                filters=filters.COMMAND
                & filters.ChatType.PRIVATE
                & filters.UpdateType.MESSAGE,
            ),
            # Handler for canceling via a callback with exact data "cancel"
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
                pattern="cancel",
                callback=cancel_fallbacks_by_button,
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
        # MessageHandler(
        #     filters=filters.Text(["Cancel My Note Making"]),
        #     callback=cancel_fallbacks,
        #     block=False,
        # ),
    ],
)
