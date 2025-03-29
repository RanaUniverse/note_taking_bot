from telegram import Update
from telegram import User
from telegram import InlineKeyboardMarkup
from telegram.ext import ContextTypes

from telegram.constants import ParseMode


from my_modules.some_inline_keyboards import MyInlineKeyboard


async def start_cmd_old(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """When user will send /start this should execute"""

    if update.message is None or update.message.from_user is None:
        print("I used this to prevent the type hint of pyright. in start cmd old")
        return

    user = update.message.from_user
    text = f"Thanks {user.first_name.upper()} For starting this bot"
    await context.bot.send_message(user.id, text)


def get_simple_message(user: User) -> str:
    text = (
        f"Thanks {user.first_name}, welcome to <b>The Note Taking Bot</b>.\n"
        f"I can help you to store Notes, in my side, and you can get the notes "
        f"back later any time.\n\n"
        f"/info :-Knows about your full informations \n"
        f"/my_notes :-Shows All My Notes \n"
        f"/search_my_notes :- Search My Notes in Title \n"
        f"/new_account or /register_me :- To make new account."
    )
    return text


def get_greeting_message(user: User) -> str:
    return f"Hello {user.first_name}, how can I assist you today?"


def get_leaving_message(user: User) -> str:
    return f"Goodbye {user.first_name}, see you soon!"


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """When user sends /start, this executes"""

    if update.message is None or update.message.from_user is None:
        print("I used this to prevent the type hint of pyright. in start cmd")
        return

    user = update.message.from_user

    user_mention = f'<a href="tg://user?id={user.id}">{user.full_name}</a>'

    text = (
        f"👋 Thanks, {user_mention}! Welcome to <b><u>The Note-Taking Bot</u></b> 📝🤖\n\n"
        f"I can help you store your notes securely and retrieve them anytime! 🔒🗂️\n\n"
        f"<b>Here below are some useful commands to check:</b>\n"
        f"🍌 /register or /register_me :- Register Yourself First\n"
        f"📝 /new_note - Create a new note\n"
        f"✏️ /edit_note - Edit an existing note\n"
        f"❌ /delete_note - Delete a note\n"
        f"🔍 /search_note - Search notes by title\n"
        f"ℹ️ /my_info - View your information\n"
        f"⚠️ <b>WARNING:</b> The buttons below are still in development. Please use the commands above for now. 🚧🔄"
    )

    await context.bot.send_message(
        chat_id=user.id,
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(MyInlineKeyboard.START_MENU.value),
    )
