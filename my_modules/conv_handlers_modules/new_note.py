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

import os

from sqlmodel import (
    select,
    Session,
)

from telegram import Update
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from telegram.ext import ContextTypes, filters


from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
)

from my_modules.database_code.database_make import engine
from my_modules.database_code.models_table import UserPart, NotePart

from my_modules.some_reply_keyboards import yes_no_reply_keyboard
from my_modules.logger_related import RanaLogger


# From Below My Code Logic will start Soon.


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


TITLE, CONTENT, CONFIRMATION = range(3)


async def new_note_button_press(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    This fun is a large of copy of the /new_note fun in this converstaion's entry point

    When the button pressed for making new note start this will execute this is
    same as /new_note conversation handler starting

        InlineKeyboardButton("📝 New Note ✅", callback_data="new_note"),
    This upper is one of the button which is pressed for this.

    """

    user = update.effective_user
    if user is None:
        RanaLogger.warning("User should has some value in the next button press")
        return ConversationHandler.END

    msg = update.effective_message
    if msg is None:
        RanaLogger.warning("When button is pressed this should have the msg obj")
        return ConversationHandler.END

    query = update.callback_query

    if query is None or query.data is None:
        RanaLogger.warning("Duplicate Note button pressed but no callback data found.")
        return ConversationHandler.END

    await query.answer(
        text="📋 You are going to make new note, Please Follow The Steps Below 🚧",
        show_alert=True,
    )

    with Session(engine) as session:
        statement = select(UserPart).where(UserPart.user_id == user.id)
        results = session.exec(statement)
        user_row = results.first()

    # This row can be None when user is not register in the database,
    # in this case it will say him to /register, else proceed with check points and
    # allow him to ask for title and then content, at last it will reduce the point and save

    if user_row is None:
        text = (
            f"Hello <b>{user.mention_html()}</b>, You Are Not Registered Yet 😢\n"
            f"Please send /register_me and then come back to use this bot.\n"
            f"Else Contact Customer Support /help."
        )
        await msg.reply_html(
            text=text,
        )
        return ConversationHandler.END

    # This line comes means user row is available.

    user_points = user_row.points

    if user_points <= 0:
        text = (
            f"You Have Finished All Your Points, Now You Cannot "
            f"make new note until you add new points, /add_points followed by int.\n\n"
            f"Example if you want 20 Token, <blockquote><code>/add_points 20</code></blockquote>"
        )

        await msg.reply_html(
            text=text,
        )
        return ConversationHandler.END

    # Below part is for when user has sufficient points and he is going to make
    # new note lets return him to a states for later input from user

    text = (
        f"You are going to make new note by pressing the button... \n\n"
        f"Hello {user.mention_html()}, You have <b>{user_points} Tokens.</b> 🎉\n"
        f"Creating a note will deduct <b>1 Token</b>. ⚠️\n\n"
        f"If you want not to make note now send, /cancel anytime\n\n"
        f"📝 <b>Step 1:</b> Please send me the <b><u>Title of Your Note</u> below.👇👇👇</b>"
    )

    await msg.reply_html(text=text)

    return TITLE


async def new_note_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    This will come from Direct Message & Privately also not any argument
    /new_note or "Make New Note"

    This will return int, as this is entry point which return to one states
    And the states will handle later things.
    """

    user = update.effective_user

    if user is None:
        RanaLogger.warning("for /new_note the user should be present.")
        return ConversationHandler.END

    if update.effective_message is None:
        RanaLogger.warning(f"For this /new_note the update.message is must, why not")
        return ConversationHandler.END

    with Session(engine) as session:
        statement = select(UserPart).where(UserPart.user_id == user.id)
        results = session.exec(statement)
        user_row = results.first()

    # This row can be None when user is not register in the database,
    # in this case it will say him to /register, else proceed with check points and
    # allow him to ask for title and then content, at last it will reduce the point and save

    if user_row is None:
        text = (
            f"Hello <b>{user.mention_html()}</b>, You Are Not Registered Yet 😢\n"
            f"Please send /register_me and then come back to use this bot.\n"
            f"Else Contact Customer Support /help."
        )
        await update.effective_message.reply_html(
            text=text,
        )
        return ConversationHandler.END

    # This line comes means user row is available.

    user_points = user_row.points

    if user_points <= 0:
        text = (
            f"You Have Finished All Your Points, Now You Cannot "
            f"make new note until you add new points, /add_points followed by int.\n\n"
            f"Example if you want 20 Token, <blockquote><code>/add_points 20</code></blockquote>"
        )

        await update.effective_message.reply_html(
            text=text,
        )
        return ConversationHandler.END

    # Below part is for when user has sufficient points and he is going to make
    # new note lets return him to a states for later input from user

    text = (
        f"You are making new row by sending /new_note or 'Make New Note'\n\n"
        f"Hello {user.mention_html()}, You have <b>{user_points} Tokens.</b> 🎉\n"
        f"Creating a note will deduct <b>1 Token</b>. ⚠️\n\n"
        f"If you want not to make note now send, /cancel anytime\n\n"
        f"📝 <b>Step 1:</b> Please send me the <b><u>Title of Your Note</u> below.👇👇👇</b>"
    )

    await update.effective_message.reply_html(text=text)

    return TITLE


async def get_note_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    This will only executes for now bot get a text only response
    only direct message not edited one.
    """
    if update.effective_message is None:
        RanaLogger.warning(f"Note title is text got so this should not happens")
        return ConversationHandler.END

    user_msg = update.effective_message.text
    user_msg_html = update.effective_message.text_html  # type: ignore

    if user_msg is None:
        RanaLogger.warning(f"This should be any value not None ever.")
        return ConversationHandler.END

    if len(user_msg) > MAX_TITLE_LEN:
        text = f"Please send short title in {MAX_TITLE_LEN} character total."
        await update.effective_message.reply_html(text)
        return ConversationHandler.END

    else:

        if context.user_data is None:
            RanaLogger.warning(f"User Data Must be a empty list atleast not none")
            return ConversationHandler.END

        # For now i add this so that it will not save formatting in the title
        # context.user_data["note_title"] = user_msg_html
        context.user_data["note_title"] = user_msg

        text = (
            f"✅ <b>Great!</b> Your note title has been saved. 🎯\n"
            f"📜 <b>Step 2:</b> Now, please send me the <u><b>Content</b> of your note</u>. 📝\n\n"
            f"💡 Tip: You can send a long message, and I'll save it as your note content."
        )

        await update.effective_message.reply_html(text=text, do_quote=True)

        return CONTENT


async def get_note_content(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    This will execute only when the bot receives a valid text message response
    (not an edited message or any non-text input).
    """
    if update.effective_message is None:
        RanaLogger.warning("Note content should be text, this should not happen.")
        return ConversationHandler.END

    user_msg = update.effective_message.text
    user_msg_html = update.effective_message.text_html

    if user_msg is None:
        RanaLogger.warning("Content message should not be None.")
        return ConversationHandler.END

    if len(user_msg) > MAX_CONTENT_LEN:
        text = f"⚠️ Your note content is too long! Please keep it within {MAX_CONTENT_LEN} characters."
        await update.effective_message.reply_html(text)

    if context.user_data is None:
        RanaLogger.warning(
            "User data must not be None, should be at least an empty dictionary."
        )
        return ConversationHandler.END

    context.user_data["note_content"] = user_msg_html

    text = (
        f"✅ <b>Great!</b> Your note content has been saved. 🎯\n"
        f"⚡ <b>Step 3:</b> Do you want to save this note permanently? Select <b>Yes</b> or <b>No</b>.\n\n"
        f"💡 Tip: You can cancel anytime with /cancel."
    )

    await update.effective_message.reply_html(
        text=text,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=yes_no_reply_keyboard,
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder="Press Button Shortcut",
        ),
    )
    return CONFIRMATION


async def note_confirmation_yes(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    I separate this as when user will press /yes on confirmation it will executes
    """
    user = update.effective_user
    if user is None:
        RanaLogger.warning("Here a user should stay")
        return ConversationHandler.END

    with Session(engine) as session:
        statement = select(UserPart).where(UserPart.user_id == user.id)
        results = session.exec(statement)
        user_row = results.first()

    if user_row is None:
        RanaLogger.warning(
            f"This should not happens as in entry point it check if user has register or not, it mans usr is not register."
        )
        return ConversationHandler.END

    if context.user_data is None:
        RanaLogger.warning("This time user_data must be present as can think")
        return ConversationHandler.END

    note_row = NotePart(
        note_title=context.user_data.get("note_title", None),
        note_content=context.user_data.get("note_content", None),
        is_available=True,
    )

    with Session(engine) as session:

        user_row.points -= 1
        note_row.user = user_row

        session.add(note_row)
        session.commit()
        session.refresh(note_row)
        session.refresh(user_row)

    text = (
        f"Your Note Has Been saved Successfully.\n"
        f"Your Note Id is: <code>{note_row.note_id}</code>."
    )

    if update.effective_message is None:
        RanaLogger.warning(f"This must have a message")
        return ConversationHandler.END

    await update.effective_message.reply_html(
        text,
        do_quote=True,
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


async def note_confirmation_no(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    When user dont want to save his data at last it will be by
    "/no", "no"
    """

    user = update.effective_user

    if user is None:
        RanaLogger.warning("Here a user should stay")
        return ConversationHandler.END

    if context.user_data is None:
        RanaLogger.warning("This time user_data must be present as can think")
        return ConversationHandler.END

    context.user_data.clear()

    text = f"Hello {user.name}, Your Note has not been saved. Pls Make new note in /new_note."

    if update.effective_message is None:
        RanaLogger.warning(f"This must have a message")
        return ConversationHandler.END

    await update.effective_message.reply_html(
        text,
        do_quote=True,
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


async def bad_note_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    This will execute when user need title but user send different udpate
    """

    user = update.effective_user

    if update.effective_message is None or user is None:
        RanaLogger.warning("it should has something why title is showing")
        return ConversationHandler.END

    # THis has maybe some logic issue as i only check when command is at beginning.
    if (
        update.effective_message.entities
        and update.effective_message.entities[0].type == "bot_command"
        and update.effective_message.entities[0].offset == 0
    ):
        text = (
            "🛠️ This is a command input! Oh sorry please send "
            f"/cancel to stop this note making..."
        )

    # Checking the type of message and responding accordingly
    elif update.effective_message.photo:
        text = (
            f"📸 <b>Oops! That's a photo!</b>\n\n"
            f"I need a <b>text message</b> to set as the note's title.\n"
            f"Please send only text here. 📝"
        )
    elif update.effective_message.animation:
        text = (
            f"🎞️ <b>Oops! That's an animation (GIF)!</b>\n\n"
            f"I need a simple <b>text message</b> to use as the note title.\n"
            f"Please type and send your title. 📝"
        )
    elif update.effective_message.document:
        text = (
            f"📄 <b>Oops! That's a document!</b>\n\n"
            f"A file can't be used as a note title.\n"
            f"Please type the note title and send it as a message. 📝"
        )
    elif update.effective_message.game:
        text = (
            f"🎮 <b>Oops! That's a game!</b>\n\n"
            f"I can't use a game as a note title.\n"
            f"Please send only text. 📝"
        )
    elif update.effective_message.sticker:
        text = (
            f"🎭 <b>Oops! That's a sticker!</b>\n\n"
            f"I need a text message for the note title, not a sticker.\n"
            f"Please type and send your note title. 📝"
        )
    elif update.effective_message.story:
        text = (
            f"📖 <b>Oops! That's a story!</b>\n\n"
            f"A story can't be used as a note title.\n"
            f"Please send only text. 📝"
        )
    elif update.effective_message.video:
        text = (
            f"🎥 <b>Oops! That's a video!</b>\n\n"
            f"A video can't be used as a note title.\n"
            f"Please send only text to set your note title. 📝"
        )
    elif update.effective_message.voice:
        text = (
            f"🎙️ <b>Oops! That's a voice message!</b>\n\n"
            f"I can't use voice messages for a note title.\n"
            f"Please send only text. 📝"
        )
    elif update.effective_message.video_note:
        text = (
            f"📹 <b>Oops! That's a video note!</b>\n\n"
            f"I need a text message, not a video note.\n"
            f"Please type and send the title. 📝"
        )
    elif update.effective_message.audio:
        text = (
            f"🎵 <b>Oops! That's an audio file!</b>\n\n"
            f"I need a text input, not an audio file.\n"
            f"Please type the note title and send it as a message. 📝"
        )
    elif update.effective_message.poll:
        text = (
            f"📊 <b>Oops! That's a poll!</b>\n\n"
            f"I can't use a poll as a note title.\n"
            f"Please send only text. 📝"
        )
    elif update.effective_message.dice:
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

    await update.effective_message.reply_html(text=text)

    return TITLE


async def bad_note_content(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    This will execute when the user needs to provide note content as text
    but sends an unsupported message type.
    """
    user = update.effective_user

    if update.effective_message is None or user is None:
        RanaLogger.warning("Expected message content, but something is missing!")
        return ConversationHandler.END

    # Check if it's a bot command at the beginning
    if (
        update.effective_message.entities
        and update.effective_message.entities[0].type == "bot_command"
        and update.effective_message.entities[0].offset == 0
    ):
        text = (
            "🛠️ This is a command input! Oh sorry, please send "
            f"/cancel to stop this note-making..."
        )
    elif update.effective_message.photo:
        text = (
            f"📸 <b>Oops! That's a photo!</b>\n\n"
            f"Currently The Photo cannot be saved as note, stay for update."
        )
    elif update.effective_message.animation:
        text = (
            f"🎞️ <b>Oops! That's an animation (GIF)!</b>\n\n"
            f"I need a text message for the note content.\n"
            f"Please type and send your note content. 📝"
        )
    elif update.effective_message.document:
        text = (
            f"📄 <b>Oops! That's a document!</b>\n\n"
            f"A file can't be used as note content.\n"
            f"Please type and send the content as a text message. 📝"
        )
    elif update.effective_message.game:
        text = (
            f"🎮 <b>Oops! That's a game!</b>\n\n"
            f"I can't use a game as note content.\n"
            f"Please send only text. 📝"
        )
    elif update.effective_message.sticker:
        text = (
            f"🎭 <b>Oops! That's a sticker!</b>\n\n"
            f"Stickers can't be used as note content.\n"
            f"Please send text instead. 📝"
        )
    elif update.effective_message.story:
        text = (
            f"📖 <b>Oops! That's a story!</b>\n\n"
            f"A story can't be used as note content.\n"
            f"Please send only text. 📝"
        )
    elif update.effective_message.video:
        text = (
            f"🎥 <b>Oops! That's a video!</b>\n\n"
            f"Videos aren't supported as note content.\n"
            f"Please send text instead. 📝"
        )
    elif update.effective_message.voice:
        text = (
            f"🎙️ <b>Oops! That's a voice message!</b>\n\n"
            f"Voice messages can't be used as note content.\n"
            f"Please type and send your note content as text. 📝"
        )
    elif update.effective_message.video_note:
        text = (
            f"📹 <b>Oops! That's a video note!</b>\n\n"
            f"A video note can't be used as note content.\n"
            f"Please type and send your note content. 📝"
        )
    elif update.effective_message.audio:
        text = (
            f"🎵 <b>Oops! That's an audio file!</b>\n\n"
            f"I need a text input for the note content.\n"
            f"Please type and send it as a message. 📝"
        )
    elif update.effective_message.poll:
        text = (
            f"📊 <b>Oops! That's a poll!</b>\n\n"
            f"A poll can't be used as note content.\n"
            f"Please send only text. 📝"
        )
    elif update.effective_message.dice:
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

    await update.effective_message.reply_html(text=text)
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
        f"Please try again with the buttons 👇🏽"
    )
    await update.effective_message.reply_html(text)
    return CONFIRMATION


async def cancel_fallbacks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    When user want to cancel this process anytime during the conversation

    /cancel & "Cancel My Note Making"
    """
    user = update.effective_user
    if user is None:
        RanaLogger.warning(f"User should exists")
        return ConversationHandler.END

    if update.effective_message is None:
        RanaLogger.warning("on /cancel this should have a Message.")
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

    await update.effective_message.reply_html(text=text)
    return ConversationHandler.END


new_note_conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler(
            command="new_note",
            callback=new_note_cmd,
            filters=filters.ChatType.PRIVATE & filters.UpdateType.MESSAGE,
            block=False,
        ),
        # This below going to same fun, though it should looks wired
        MessageHandler(
            filters=filters.Text(["Make New Note"]),
            callback=new_note_cmd,
            block=False,
        ),
        CallbackQueryHandler(
            callback=new_note_button_press,
            pattern="new_note",
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
