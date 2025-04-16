"""
Here i will keep the logic and code which will help me
to edit a note's title content and something
First i will do this in a command /edit_note

"""

import html
import os


from telegram import Update
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import ContextTypes
from telegram.ext import (
    CallbackQueryHandler,
    # i need to use this in reality
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from my_modules.database_code import db_functions
from my_modules.database_code.database_make import engine

from my_modules.logger_related import RanaLogger

SELECT_OPTION, TITLE, CONTENT, CONFIRMATION = range(4)


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


async def edit_note_cmd_no_args(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    When user will only send /edit_note without anything else
    this function will execute it will give user the choice to choose
    a old note, or say make a note and return for sure
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

    # if len(context.args) == 0:
    # i dont need to check this args len as it will always 0 as in i pass

    buttons = [
        [
            InlineKeyboardButton(
                text="Find From All Notes To Edit ✅",
                callback_data="my_all_notes",
            ),
            InlineKeyboardButton(
                text="New Note Make Now ✅",
                callback_data="new_note",
            ),
        ],
        [
            InlineKeyboardButton(
                text="Need Help",
                callback_data="customer_care",
            ),
            InlineKeyboardButton(
                text="Cancel Now ✅",
                callback_data="cancel_conv",
            ),
        ],
    ]

    text = (
        f"You get if from single fun as you dont pass any args. "
        f"Hello {user.mention_html()}, you have not pass the note id, so i dont know which "
        f" note you are going to edit. "
        f"So please select a note below and then found the note id of "
        f"After you get the note id please send me the note id as "
        f"<code>/edit_note &lt;note_id&gt;</code>"
        f"Conversation has ended."
    )
    await msg.reply_html(
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons),
    )
    # After this fun execute it want for note id,
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
        f"Hello {user.mention_html()}, you've passed too many values after <code>/edit_note</code>. "
        f"This command expects <b>exactly one</b> argument — the <u>note ID</u> you want to edit.\n\n"
        f"✅ Example usage:\n"
        f"<code>/edit_note NOTE123</code>\n\n"
        f"Please try again with just the note ID."
    )

    await msg.reply_html(text=text)
    return ConversationHandler.END


async def edit_note_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    This is my current best logic i will check the one args value and see
    if this is note id and so on and the conversation will start from here.
    as from handler it will only executes one args.

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

    else:
        note_id = context.args[0]
        note_row = db_functions.note_obj_from_note_id(
            engine=engine,
            note_id=note_id,
        )

        if note_row is None:
            text = (
                f"Note ID: <u>{html.escape(note_id)}</u>\n\n"
                f"This is not a valid note id Please provideo correct note id, else find "
                f"correct note id in /my_notes section."
            )
            await msg.reply_html(text=text)
            return ConversationHandler.END

        # Below is execute when note_row is present
        owner_id = note_row.user_id

        if user.id != owner_id:
            text = (
                f"🚫 <b>Access Denied</b>\n\n"
                f"Dear {user.mention_html()}, you are not the owner of this note and therefore "
                f"cannot edit it. 😢\n\n"
                f"If you believe this is an error or need assistance, "
                f"please contact support via /help."
            )
            await msg.reply_html(text=text)
            return ConversationHandler.END

        # Below part is the greatest part which is my main logic to do the note edit
        # i am thinking to keep the note's id to be in the dict so that i can know which note
        # i need to edit and what to do with this.
        else:
            content_preview = f"{note_row.note_content}"[:100]
            text = (
                f"Hello {user.mention_html()}, You own this note 🙋\n\n"
                f"<u>TITLE</u>: {note_row.note_title} \n\n"
                f"<u>CONTENT</u>: {content_preview}... \n\n"
                f"Please SElect the correct button to edit the note. "
                f"Also send /cancel anytime to exit this note making"
            )
            button = [
                [
                    InlineKeyboardButton(
                        text="Edit Title",
                        callback_data="edit_title",
                    ),
                    InlineKeyboardButton(
                        text="Edit Content",
                        callback_data="edit_content",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Export Current Note",
                        callback_data=f"export_note_{note_id}",
                    ),
                    InlineKeyboardButton(
                        text="Delete This Note ✅",
                        callback_data=f"delete_note_{note_id}",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Change Ownership",
                        callback_data=f"owner_change_{note_id}",
                    ),
                    InlineKeyboardButton(
                        text="Cancel Editing",
                        callback_data="cancel_button",
                    ),
                ],
            ]

            if context.user_data is None:
                RanaLogger.warning(f"User Data Must be a empty list atleast not none")
                return ConversationHandler.END

            context.user_data["note_id_of_edited_note"] = note_id

            await msg.reply_html(
                text=text,
                reply_markup=InlineKeyboardMarkup(button),
            )
            return SELECT_OPTION


async def cancel_fallbacks_by_cmd(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    When user want to cancel this process anytime during the conversation

    /cancel & "Cancel My Note Making"
    """
    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None:
        RanaLogger.warning(
            "in conversation of edit note the msg and user is must need "
        )
        return ConversationHandler.END

    if context.user_data is None:
        RanaLogger.warning(f"Context .user data at least is a empty dict,")
        return ConversationHandler.END

    RanaLogger.warning(f"📝 User ({user.name}) Data Removed: {context.user_data}")

    context.user_data.clear()

    text = (
        f"You have just cancel teh note editing process by ur wish. "
        f"If you want to edit again pls come in /edit_note again."
    )

    await msg.reply_html(text=text)
    return ConversationHandler.END


async def cancel_fallbacks_by_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    when a button has say to cancel the note editing process
    """
    query = update.callback_query
    msg = update.effective_message

    if query is None or query.data is None:
        RanaLogger.warning(f"When cancel edit note button is pressed it should exists")
        return ConversationHandler.END

    if msg is None:
        RanaLogger.warning(f"The message should be present ")
        return ConversationHandler.END

    if context.user_data is None:
        RanaLogger.warning(f"Context .user data at least is a empty dict,")
        return ConversationHandler.END

    if query.data != "cancel":
        RanaLogger.warning(f"Button data is must need 'cancel'")
        await msg.reply_html(
            f"Some Query's Data has some issue but this edit "
            f"Note conversation has just ended."
        )
        return ConversationHandler.END

    if query.data == "cancel":
        await query.answer("You have pressed cancel button")
        context.user_data.clear()
        text = (
            f"You have pressed the cancel note making button "
            f"so this note editing has been stopped, you can "
            f"start again in /edit_note"
        )
        await msg.reply_html(text)
        return ConversationHandler.END

    # Below is saying to return to end explicitely
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
            callback=edit_note_cmd,
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
        MessageHandler(
            filters=filters.Text(["Edit My Note", "edit note"])
            & filters.ChatType.PRIVATE
            & filters.UpdateType.MESSAGE,
            callback=edit_note_cmd,
            block=False,
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
                pattern=r"^cancel$",
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
