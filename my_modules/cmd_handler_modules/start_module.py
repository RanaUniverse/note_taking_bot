"""
/start From User Direct Message
/start From Group Chat


"""

import os

from telegram import Update
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

from telegram.constants import ParseMode

from telegram.ext import ContextTypes


from my_modules.some_inline_keyboards import MyInlineKeyboard
from my_modules.logger_related import RanaLogger


BOT_USERNAME = os.environ.get("BOT_USERNAME", None)

if not BOT_USERNAME:
    raise ValueError("❌ BOT_USERNAME not found in .env file!")


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    When user sends /start in private chat, this executes
    """

    if update.message is None or update.message.from_user is None:
        print("I used this to prevent the type hint of pyright. in start cmd")
        return

    user = update.message.from_user

    text = (
        f"👋 Hello, {user.mention_html()}! Welcome to <b><u>The Note-Taking Bot</u></b> 📝🤖\n\n"
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
        f"⚠️ <b>WARNING:</b> The buttons below are still in development. "
        f"Please use the commands above for now. 🚧🔄"
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
    When a /start get by groups
    i need to use chat , as user maybe not available when user is hidden admin
    """
    chat = update.effective_chat

    if chat is None:
        print("This should not execute as start in groups.")
        return

    text = (
        "📢 <b>Notice:</b>\n\n"
        "⚠️ This bot currently <b>cannot take notes in groups</b>.\n"
        "🛠️ This feature is <b>is not implimenteds yet not available</b>, "
        f"but it will be added in a future update.\n"
        "🔔 Stay tuned for updates!"
        "Please Press This button To Accss This Bot..."
    )

    url_value = f"https://t.me/{BOT_USERNAME}?start=group_start"

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


async def start_cmd_from_group_to_private(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    This will execute when /start has a deep link which comes
    from the group /start button to private chat this is very
    just for a differentiate how to use this
    """

    if context.args is None:
        RanaLogger.warning("When deep link is used the value should has somethign")
        return None

    if update.message is None or update.message.from_user is None:
        print("I used this to prevent the type hint of pyright. in start cmd")
        return

    user = update.message.from_user

    if context.args[0] == "group_start":
        print("something happens")
        text = (
            "You have started this bot from a group chat, "
            f"Currently please just use this bot in private and "
            f"later use this bot until we will update this in a official update.\n"
            f"Please see the below message."
        )

        await context.bot.send_message(
            chat_id=user.id,
            text=text,
            parse_mode=ParseMode.HTML,
        )

        await start_cmd(update=update, context=context)

    else:
        print("another button")
