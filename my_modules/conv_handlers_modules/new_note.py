"""
This module is a conversation handler where user can start making new note
it will ask for note title and content, and it will save those in the database

** Ideas for making new note **

1st: How this can start thie note making idea,
    1. When user will send /new_note command
    2. button having the callback_data = "new_note_making"
    3. /make_a_random_note :- This is for user make random note in his acccount


2nd: After 1,2 it will return to a state's obj which is found for Note's Title,
    Here i also need to keep the fallsback's /cancel and filters.ALL need to keep
    kept which return to the same state. And also Title need to be fixed length.


3rd: After This Title, it will also ask for Content of the note, also same logic applied as 2nd.

4th: Confirmation, It will have buttons which will show if user want to save the note or not/
    Then it will also have a wrong input checking logic also need to established.

"""

from telegram import Update
from telegram import InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from telegram.ext import ContextTypes, filters


from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
)

from my_modules import bot_config_settings
from my_modules import message_templates

from my_modules.database_code.database_make import engine
from my_modules.database_code.models_table import NotePart
from my_modules.database_code import db_functions

from my_modules.logger_related import RanaLogger

from my_modules.some_inline_keyboards import generate_view_note_buttons

from my_modules.some_reply_keyboards import yes_no_reply_keyboard


# From Below My Code Logic will start Soon.


MAX_TITLE_LEN = bot_config_settings.MAX_TITLE_LEN
MAX_CONTENT_LEN = bot_config_settings.MAX_CONTENT_LEN


TITLE, CONTENT, CONFIRMATION = range(3)


async def new_note_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Command: `/new_note`
    Text: "Make New Note"
    When This will come it will start the conversation
    So that it will ask for title & progressing.
    This will come from Direct Message & Privately also not any argument.
    """

    user = update.effective_user
    msg = update.effective_message

    if user is None:
        RanaLogger.warning("for /new_note the user should be present.")
        return ConversationHandler.END

    if msg is None:
        RanaLogger.warning(f"For this /new_note the update.message is must, why not")
        return ConversationHandler.END

    user_row = db_functions.user_obj_from_user_id(engine, user.id)

    if user_row is None:
        no_register_text = message_templates.prompt_user_to_register(user)
        await msg.reply_html(text=no_register_text)
        return ConversationHandler.END

    # This line comes to executes means user row is available.

    user_points = user_row.points

    if user_points <= 0:
        text_no_point = message_templates.user_has_no_valid_points(user)
        await msg.reply_html(text=text_no_point)
        return ConversationHandler.END

    # Below part is for when user has sufficient points and he is going to make
    # new note lets return him to a states for later input from user

    text = message_templates.new_note_title_ask(user, user_points)
    await msg.reply_html(text=text)

    return TITLE


async def new_note_button_press(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """
    When User Want to make new note by pressing the button.
        InlineKeyboardButton("📝 New Note ✅", callback_data="new_note_making"),
    """

    user = update.effective_user
    msg = update.effective_message

    if user is None:
        RanaLogger.warning("User should has some value in the next button press")
        return ConversationHandler.END

    if msg is None:
        RanaLogger.warning("When button is pressed this should have the msg obj")
        return ConversationHandler.END

    query = update.callback_query
    if query is None or query.data is None:
        RanaLogger.warning("Note button pressed but no callback data found.")
        return ConversationHandler.END

    await query.answer(
        text="📋 Please Follow The Steps Below To Make New Note 🚧",
        show_alert=True,
    )

    user_row = db_functions.user_obj_from_user_id(engine, user.id)

    if user_row is None:
        no_register_text = message_templates.prompt_user_to_register(user)
        await msg.reply_html(text=no_register_text)
        return ConversationHandler.END

    # This line comes to execute means user row is available.

    user_points = user_row.points

    if user_points <= 0:
        text_no_point = message_templates.user_has_no_valid_points(user)
        await msg.reply_html(text=text_no_point)
        return ConversationHandler.END

    # Below part is for when user has sufficient points and he is going to make
    # new note lets return him to a states for later input from user

    text = message_templates.new_note_title_ask(user, user_points)
    await msg.reply_html(text=text)

    return TITLE


async def get_note_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    The Only Way, when a user send text to save as note's title,
    This will executes and it will take the note' title in a cache to use later.
    """
    msg = update.effective_message

    if msg is None:
        RanaLogger.warning(f"Note title is text got so msg must present")
        return ConversationHandler.END

    user_msg = msg.text

    # i am saving the title without formatting so that it will not shows bad in buttons

    # user_msg_html = msg.text_html

    if user_msg is None:
        RanaLogger.warning(f"User New Note's Title must has some value not None.")
        return ConversationHandler.END

    if len(user_msg) > MAX_TITLE_LEN:
        title_exceed = message_templates.title_length_exceed_warning_text()

        await msg.reply_html(text=title_exceed)
        return TITLE

    else:

        if context.user_data is None:
            RanaLogger.warning(
                f"User Data Must be a empty list atleast not None, when getting the Title"
            )
            return ConversationHandler.END

        # For now i add this so that it will not save formatting in the title
        # context.user_data["note_title"] = user_msg_html

        context.user_data["note_title"] = user_msg

        ask_for_content = message_templates.new_note_content_ask()

        await msg.reply_html(text=ask_for_content, do_quote=True)

        return CONTENT


async def get_note_content(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    This will execute only when the bot receives a valid text message response
    (not an edited message or any non-text input).
    """
    msg = update.effective_message

    if msg is None:
        RanaLogger.warning(
            "In New Note Making, the Note Content getting the msg must present"
        )
        return ConversationHandler.END

    user_msg = msg.text
    user_msg_html = msg.text_html

    if user_msg is None:
        RanaLogger.warning("Content message should not be None.")
        return ConversationHandler.END

    if len(user_msg) > MAX_CONTENT_LEN:
        exceed_content = message_templates.content_length_exceed_warning_text()

        await msg.reply_html(text=exceed_content)
        return CONTENT

    if context.user_data is None:
        RanaLogger.warning(
            "User data must not be None, should be at least an "
            "empty dictionary at time of content getting."
        )
        return ConversationHandler.END

    context.user_data["note_content"] = user_msg_html

    ask_for_note_save = message_templates.new_note_save_ask()

    in_keyboard_button = ReplyKeyboardMarkup(
        keyboard=yes_no_reply_keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Press Any Button Quickly",
    )

    await msg.reply_html(text=ask_for_note_save, reply_markup=in_keyboard_button)
    return CONFIRMATION


async def note_confirmation_yes(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """
    I separate this as when user will press /yes on confirmation it will executes.
    """
    user = update.effective_user
    msg = update.effective_message

    if user is None:
        RanaLogger.warning(
            "Here a user should stay when sending yes confirmation on note saving."
        )
        return ConversationHandler.END

    if msg is None:
        RanaLogger.warning(f"This must have a message")
        return ConversationHandler.END

    user_row = db_functions.user_obj_from_user_id(engine, user.id)

    if user_row is None:
        RanaLogger.warning(
            f"This should not happens as in entry point it check if "
            f"user has register or not, it mans user is not register in time of note saving."
        )
        return ConversationHandler.END

    if context.user_data is None:
        RanaLogger.warning(
            "at note save confirmation yes, user_data " "must be present as can think"
        )
        return ConversationHandler.END

    note_row = NotePart(
        note_title=context.user_data.get("note_title", None),
        note_content=context.user_data.get("note_content", None),
        is_available=True,
    )

    db_functions.add_one_note_and_update_the_user(engine, user_row, note_row)

    # As the upper fun re value the variable, so this is just automatically
    note_maked_text = message_templates.new_note_making_confirmation_yes(
        note_obj=note_row,
        user_balance=user_row.points,
    )

    buttons_successfull_note = generate_view_note_buttons(note_row.note_id)

    await msg.reply_html(
        text=note_maked_text,
        do_quote=True,
        reply_markup=InlineKeyboardMarkup(buttons_successfull_note),
    )
    return ConversationHandler.END


async def note_confirmation_no(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """
    When user dont want to save his data at last it will be by
    "/no", "no"
    """

    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None:
        RanaLogger.warning(
            "User or msg must present when user choose no in new note save"
        )
        return ConversationHandler.END

    if context.user_data is None:
        RanaLogger.warning("This time user_data must be present as can think")
        return ConversationHandler.END

    context.user_data.clear()

    note_not_save = message_templates.new_note_making_confirmation_no(user=user)

    await msg.reply_html(
        text=note_not_save,
        do_quote=True,
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


async def note_confirmation_as_draft(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """
    When user will want to save his note by marking
    Is Available: No
    This will just save the note like this,
    so That user will not avle to see note Right Now.
    """
    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None:
        RanaLogger.warning(
            "User or msg must present when user choose note as not available."
        )
        return ConversationHandler.END

    if context.user_data is None:
        RanaLogger.warning(
            "at note save confirmation yes, user_data " "must be present as can think"
        )
        return ConversationHandler.END

    user_row = db_functions.user_obj_from_user_id(engine, user.id)

    if user_row is None:
        RanaLogger.warning(
            f"This should not happens as in entry point it check if "
            f"user has register or not, it mans user is not"
            " register in time of note saving draft."
        )
        return ConversationHandler.END

    note_row = NotePart(
        note_title=context.user_data.get("note_title", None),
        note_content=context.user_data.get("note_content", None),
        is_available=False,
    )

    db_functions.add_one_note_and_update_the_user(engine, user_row, note_row)

    note_maked_text = message_templates.new_note_making_confirmation_as_draft(
        note_obj=note_row,
    )

    buttons_successfull_note = generate_view_note_buttons(note_row.note_id)

    await msg.reply_html(
        text=note_maked_text,
        do_quote=True,
        reply_markup=InlineKeyboardMarkup(buttons_successfull_note),
    )
    return ConversationHandler.END


async def bad_note_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    This will execute when user need title but user send different
    type of response.
    """

    user = update.effective_user
    msg = update.effective_message

    if msg is None or user is None:
        RanaLogger.warning("it should has something why title is showing")
        return ConversationHandler.END

    # THis has maybe some logic issue as i only check when command is at beginning.
    if (
        msg.entities
        and msg.entities[0].type == "bot_command"
        and msg.entities[0].offset == 0
    ):
        text = (
            "🛠️ This is a command input! Oh sorry please send "
            f"/cancel to stop this note making..."
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


async def bad_note_content(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    This will execute when the user needs to provide note content as text
    but sends an unsupported message type.
    """
    user = update.effective_user
    msg = update.effective_message

    if msg is None or user is None:
        RanaLogger.warning("Expected message content, but something is missing!")
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


async def cancel_fallbacks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    When user want to cancel this process anytime during the conversation

    /cancel & "Cancel My Note Making"
    """
    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None:
        RanaLogger.warning(f"User should exists when /cancel got in conversation")
        return ConversationHandler.END

    if context.user_data is None:
        RanaLogger.warning(f"Context .user data at least is a empty dict,")
        return ConversationHandler.END

    RanaLogger.warning(f"📝 User ({user.name}) Data Removed: {context.user_data}")

    context.user_data.clear()

    text = (
        f"🚫 <b>Note creation process has been canceled.</b>\n\n"
        f"If you want to start again, send /new_note."
    )

    await msg.reply_html(text=text)
    return ConversationHandler.END


new_note_conv = ConversationHandler(
    entry_points=[
        # when this will come it will start making the conversation.
        CommandHandler(
            command="new_note",
            callback=new_note_cmd,
            filters=filters.ChatType.PRIVATE & filters.UpdateType.MESSAGE,
            block=False,
        ),
        # This below going to same fun, though it should looks wired
        MessageHandler(
            filters=filters.Text(["Make New Note Now"]),
            callback=new_note_cmd,
            block=False,
        ),
        # because also pressing the button which data to make new note conversation
        CallbackQueryHandler(
            callback=new_note_button_press,
            pattern="new_note_making",
            block=False,
        ),
    ],
    states={
        TITLE: [
            CommandHandler(
                command="cancel",
                callback=cancel_fallbacks,
                filters=filters.COMMAND
                & filters.ChatType.PRIVATE
                & filters.UpdateType.MESSAGE,
            ),
            MessageHandler(
                filters=filters.Command(),
                callback=bad_note_title,
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
                callback=bad_note_title,
                block=False,
            ),
        ],
        CONTENT: [
            CommandHandler(
                command="cancel",
                callback=cancel_fallbacks,
                filters=filters.COMMAND
                & filters.ChatType.PRIVATE
                & filters.UpdateType.MESSAGE,
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
                callback=bad_note_content,
                block=False,
            ),
        ],
        CONFIRMATION: [
            CommandHandler(
                command="cancel",
                callback=cancel_fallbacks,
                filters=filters.COMMAND
                & filters.ChatType.PRIVATE
                & filters.UpdateType.MESSAGE,
                block=False,
            ),
            MessageHandler(
                filters=filters.Text(["Yes", "/yes"]),
                callback=note_confirmation_yes,
                block=False,
            ),
            MessageHandler(
                filters=filters.Text(["No", "/no"]),
                callback=note_confirmation_no,
                block=False,
            ),
            MessageHandler(
                filters=filters.Text(["Save As Draft", "/draft_note"]),
                callback=note_confirmation_as_draft,
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
            callback=cancel_fallbacks,
            filters=filters.COMMAND
            & filters.ChatType.PRIVATE
            & filters.UpdateType.MESSAGE,
            block=False,
        ),
        MessageHandler(
            filters=filters.Text(["Cancel My Note Making"]),
            callback=cancel_fallbacks,
            block=False,
        ),
    ],
    allow_reentry=True,
)
