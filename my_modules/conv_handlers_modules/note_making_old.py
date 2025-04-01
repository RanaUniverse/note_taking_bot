"""
Here i will make the codes which will help to setup new note
edit note,
delte note and so on
"""

from telegram import ReplyKeyboardMarkup
from telegram import Update

from telegram.constants import ParseMode

from telegram.ext import filters
from telegram.ext import ContextTypes

from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    MessageHandler,
)


from sqlmodel import Session, select

from my_modules.database_code.models_table import UserPart, NotePart
from my_modules.database_code.database_make import engine


from my_modules.some_reply_keyboards import yes_no_reply_keyboard


TITLE, CONTENT, CONFIRMATION = range(3)


async def new_note_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    First it will check the point's value in the his row of user
    This will start a conversation asking for title and then description
    and then it will save this note and return the successful or not message


    Then it will check how many points he has, as one point = 1 note,
    if he has not more point it will ask to go back and add new point
    point can be get from '/add_points 100' like this and when he will
    have good point it will ask for title, and then description,
    and it will save this note in the notepart table,

    """

    # First it will check if user is in database if not say him to go and register
    # and then come back here ot make new note
    if update.message is None or update.message.from_user is None:
        print("I used this to prevent the type hint of pyright. in newnotecmd")
        return ConversationHandler.END

    user = update.message.from_user
    user_mention = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'

    with Session(engine) as session:
        statement = select(UserPart).where(UserPart.user_id == user.id)
        results = session.exec(statement)
        user_row = results.first()

    if user_row is None:
        # it means user has not register so it need to go back and register
        text = (
            f"Hello {user_mention} 😢😢😢\n"
            "⚠️ You are not registered! Please use /register_me to create an account first."
            "Then you will able to make new notes and use this Bot "
        )
        await context.bot.send_message(
            chat_id=user.id,
            text=text,
            parse_mode=ParseMode.HTML,
        )
        return ConversationHandler.END

    # below i will check his points to allow him or not making the notes
    his_points = user_row.points

    if his_points <= 0:
        text = (
            "❌ You don't have enough points to create a note. "
            f"Creating a note will deduct <b>1 point</b> from your balance. ⚠️\n\n"
            "Pls send /add_points followed by a value (<code>/add_points 10</code>) "
            "to add some points here."
        )
        await context.bot.send_message(
            chat_id=user.id,
            text=text,
            parse_mode=ParseMode.HTML,
        )
        return ConversationHandler.END

    # Below will execute when user has valid >=1 points then it will execute

    text = (
        f"Hello {user_mention}, You have <b>{his_points}</b> Points. 🎉\n"
        f"Creating a note will deduct <b>1 point</b> from your Points({his_points}). ⚠️\n\n"
        f"If you want not to make note now send, /cancel\n\n"
        f"📝 <b>Step 1:</b> Please send me the <b><u>Title of Your Note</u> below.👇👇👇</b>"
    )

    await context.bot.send_message(
        chat_id=user.id,
        text=text,
        parse_mode=ParseMode.HTML,
    )

    return TITLE


async def get_note_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    This will get the note title and it will keep save it in the running time
    until it got saved in the datbase.
    """
    if (
        update.message is None
        or update.message.from_user is None
        or context.user_data is None
    ):
        print("/get_note_title thsi should not executes")
        return ConversationHandler.END

    user = update.message.from_user
    context.user_data["note_title"] = update.message.text_html
    # i used .text_html as i want to store the formatting also.

    text = (
        f"✅ <b>Great!</b> Your note title has been saved. 🎯\n"
        f"📜 <b>Step 2:</b> Now, please send me the <b>Content</b> of your note. 📝\n\n"
        f"💡 Tip: You can send a long message, and I'll save it as your note content."
    )

    await context.bot.send_message(
        chat_id=user.id,
        text=text,
        parse_mode=ParseMode.HTML,
    )

    return CONTENT


async def bad_update_in_title(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    This will execute when bot need title text but user send somethign else
    """

    # if update.message is None or update.message.from_user is None:
    #     print("a user should have here also when he send not text in title")
    #     return ConversationHandler.END

    # user = update.message.from_user
    user = update.effective_user

    if user is None:
        print(f"This is unexpected in the bad update when title need.")
        return ConversationHandler.END

    text = f"You Need to send a Text in the Title Part. Pls send Text"
    await context.bot.send_message(user.id, text)
    return TITLE


async def get_note_content(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    this will take the description of the note / content of the note
    which will be saved


    # Here user can send another text and i need to save this next text in the content.

    """
    if (
        update.message is None
        or update.message.from_user is None
        or context.user_data is None
    ):
        print("I used this to prevent the type hint of pyright. get note content")
        return ConversationHandler.END

    user = update.message.from_user

    context.user_data["note_content"] = update.message.text

    text = (
        "📌 <b>Note Received!</b>\n\n"
        "I have saved your Note Title and Content. Now, if you want to "
        "<b>save This Note permanently</b>, please send `Yes` or `No` or /cancel"
    )

    await context.bot.send_message(
        chat_id=user.id,
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=ReplyKeyboardMarkup(
            yes_no_reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="yes not button here.",
        ),
    )

    print(context.user_data)

    return CONFIRMATION


async def bad_update_in_content(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    This function is triggered when the bot expects note content,
    but the user sends something else (e.g., a photo, sticker, voice message).
    """

    user = update.effective_user

    if user is None:
        print("This should not execute")
        return ConversationHandler.END

    print("Something bad in content part.")

    text = "⚠️ Please send a valid text message for the note content. Images, stickers, or other media are not allowed for Now."
    await context.bot.send_message(user.id, text)

    return CONTENT


async def cancel_note_making(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    the note making has been stopped
    """
    if update.message is None or update.message.from_user is None:
        print("I used this to prevent the type hint of pyright.")
        return ConversationHandler.END

    user = update.message.from_user
    user_mention = f'<a href="tg://user?id={user.id}">{user.full_name}</a>'

    text = (
        f"Hello {user_mention} \n"
        f"You have stopped the note making process. Thanks Meet you later."
    )

    await context.bot.send_message(
        chat_id=update.message.from_user.id,
        text=text,
        parse_mode=ParseMode.HTML,
    )
    return ConversationHandler.END


async def save_note(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    When user want to save his note 'Yes'
    """
    if update.message is None or update.message.from_user is None:
        print("save note yes should not be none")
        return ConversationHandler.END

    print("Note is going to save")

    user = update.message.from_user

    with Session(engine) as session:
        statement = select(UserPart).where(UserPart.user_id == user.id)
        results = session.exec(statement)
        user_row = results.first()

    if user_row is None:
        text = (
            f"This should not happens as in start time of the note making it "
            f"already checked if the user is register or not, maybe in the "
            f"time of conversation it got delete."
        )
        await context.bot.send_message(user.id, text)
        return ConversationHandler.END

    # NOw it means userrow has a value so now i will use to save this note
    if context.user_data is None:
        print(f"User should have some context.data as it is come")
        return ConversationHandler.END

    note_row = NotePart(
        note_title=context.user_data.get("note_title", None),
        note_content=context.user_data.get("note_content", None),
        is_available=True,
    )
    # i need to open with session again and use this insert

    with Session(engine) as session:

        note_row.user = user_row
        user_row.points -= 1

        session.add(note_row)
        session.add(user_row)
        session.commit()
        session.refresh(note_row)
        session.refresh(user_row)

    text = (
        f"Hello {user.first_name}, Your new Note has been Saved Successfully. "
        f"Your Private Note ID: <tg-spoiler><code>{note_row.note_id}</code></tg-spoiler>, "
        f"Please keep it hidden to get your note back."
    )

    from telegram import ReplyKeyboardRemove

    await context.bot.send_message(
        chat_id=user.id,
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=ReplyKeyboardRemove(),
    )


async def discard_note(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """thsi will execute when note will not saved but it will send the note back to user now"""


conv_new_note = ConversationHandler(
    entry_points=[
        CommandHandler(
            command=["new_note", "make_note"],
            callback=new_note_cmd,
            block=False,
        ),
        MessageHandler(
            filters=filters.Text(["NEW NOTE"]),
            callback=new_note_cmd,
            block=False,
        ),
    ],
    states={
        TITLE: [
            CommandHandler(
                command="cancel",
                callback=cancel_note_making,
                filters=filters.COMMAND & filters.UpdateType.MESSAGE,
            ),
            MessageHandler(
                filters=filters.TEXT & filters.UpdateType.MESSAGE,
                callback=get_note_title,
                block=False,
            ),
            MessageHandler(
                filters=filters.ALL,
                callback=bad_update_in_title,
                block=False,
            ),
        ],
        CONTENT: [
            CommandHandler(
                command="cancel",
                callback=cancel_note_making,
                filters=filters.COMMAND & filters.UpdateType.MESSAGE,
            ),
            MessageHandler(
                filters=filters.TEXT & filters.UpdateType.MESSAGE,
                callback=get_note_content,
                block=False,
            ),
            MessageHandler(
                filters=filters.ALL,
                callback=bad_update_in_content,
                block=False,
            ),
        ],
        CONFIRMATION: [
            CommandHandler(
                command="cancel",
                callback=cancel_note_making,
                filters=filters.COMMAND & filters.UpdateType.MESSAGE,
            ),
            MessageHandler(
                filters=filters.Text(["Yes"]) & filters.UpdateType.MESSAGE,
                callback=save_note,  # Function to save the note
                block=False,
            ),
            MessageHandler(
                filters=filters.Text(["No"]) & filters.UpdateType.MESSAGE,
                callback=discard_note,  # Function to discard the note
                block=False,
            ),
        ],
    },
    fallbacks=[
        CommandHandler(
            command="cancel",
            callback=cancel_note_making,
            filters=filters.COMMAND & filters.UpdateType.MESSAGE,
        ),
        CommandHandler("cancel", cancel_note_making),
        CommandHandler("abord_setup", cancel_note_making),
        CommandHandler("start_later", cancel_note_making),
    ],
    allow_reentry=True,
)
