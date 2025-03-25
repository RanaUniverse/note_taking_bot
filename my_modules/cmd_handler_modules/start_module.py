from telegram import Update
from telegram import User
from telegram.ext import ContextTypes


async def start_cmd_old(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """When user will send /start this should execute"""

    if update.message is None or update.message.from_user is None:
        print("I used this to prevent the type hint of pyright.")
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
    )
    return text


def get_greeting_message(user: User) -> str:
    return f"Hello {user.first_name}, how can I assist you today?"


def get_leaving_message(user: User) -> str:
    return f"Goodbye {user.first_name}, see you soon!"


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """When user sends /start, this executes"""

    if update.message is None or update.message.from_user is None:
        print("I used this to prevent the type hint of pyright.")
        return

    user = update.message.from_user
    text = get_simple_message(user)
    await context.bot.send_message(user.id, text)
