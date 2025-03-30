"""
/start From User Direct Message
/start From Group Chat


"""

import os

from telegram import Update
from telegram import User
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import ContextTypes

from telegram.constants import ParseMode


from my_modules.some_inline_keyboards import MyInlineKeyboard


BOT_USERNAME = os.environ.get("BOT_USERNAME", None)


if not BOT_USERNAME:
    raise ValueError("❌ BOT_USERNAME not found in .env file!")

# Below 3 Functions i made just to call and take a input i just keep it now, no need in code.


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
    """
    When user sends /start in private chat, this executes
    """

    if update.message is None or update.message.from_user is None:
        print("I used this to prevent the type hint of pyright. in start cmd")
        return

    user = update.message.from_user

    user_mention = f'<a href="tg://user?id={user.id}">{user.full_name}</a>'

    text = (
        f"👋 Hello, {user_mention}! Welcome to <b><u>The Note-Taking Bot</u></b> 📝🤖\n\n"
        f"Use the buttons below to manage your notes, or use commands if needed! 🔒🗂️\n\n"
        f"<b>🔹 Available Commands:</b>\n"
        f"📝 /new_note - Create a new note\n"
        f"📂 /view_notes - View all your notes\n"
        f"✏️ /edit_note - Edit an existing note\n"
        f"🔍 /search_note - Search notes by title\n"
        f"❌ /delete_note - Delete a note\n"
        f"📤 /export_notes - Export all notes\n"
        f"⚙️ /update_profile - Update your profile\n"
        f"❓ /help - Get help and usage instructions\n\n"
        f"⚠️ <b>Note:</b> If buttons don't work, use the above commands manually."
        f"⚠️ <b>WARNING:</b> The buttons below are still in development. Please use the commands above for now. 🚧🔄"
    )

    await context.bot.send_message(
        chat_id=user.id,
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(MyInlineKeyboard.START_MENU.value),
    )
    # For now there is the button not works, for now the buttons
    # will show a alart that it not implimented yet, rather use this command.


async def start_cmd_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    When a edite /start get by groups
    i need to use chat , as user maybe not available when user is hidden admin
    """
    chat = update.effective_chat

    if chat is None:
        print("This should not execute as start in groups.")
        return

    text = (
        "📢 <b>Notice:</b>\n\n"
        "⚠️ This bot currently <b>cannot take notes in groups</b>.\n"
        "🛠️ This feature is <b>is not implimenteds yet available</b>, but it will be added in a future update.\n"
        "🔔 Stay tuned for updates!"
        "Please Press This button To Accss This Bot..."
    )

    url_value = f"https://t.me/{BOT_USERNAME}?start=start"

    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Go to Private Chat",
                    url=url_value,
                ),
            ]
        ]
    )
    await context.bot.send_message(
        chat_id=chat.id,
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=button,
    )
