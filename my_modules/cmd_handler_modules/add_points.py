"""
This file will contains some code related to
add some points which is used by user to make note and so on


for now i will make it as demo so that use can by himself add notes.

/add_points :- For now it will send by user and points will be added.

`/add_points 50` :- User need to send like this,

"""

import asyncio


from telegram import Update

from telegram.ext import ContextTypes

from telegram.constants import ParseMode, ChatAction


from sqlmodel import Session, select

from my_modules.logger_related import logger

from my_modules.database_code.models_table import UserPart
from my_modules.database_code.database_make import engine


async def add_points_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    When user will send /add_points

    if user dont send any value after the command it will ask him to send right
    """
    print("this has get by suer")

    if update.message is None or update.message.from_user is None:
        print("I used this to prevent the type hint of pyright.")
        return

    user = update.message.from_user

    if context.args is None:
        print("This is unexpected 🍌🍌🍌")
        return

    if len(context.args) == 0:

        text = (
            f"You haven't pass any argument after this command."
            f"You need to send how many points you want to add.\n"
            f"Example: Suppose You want to get 10 points, then send this below to bot."
            f"<blockquote><code>/add_points 10</code></blockquote>"
        )

        await context.bot.send_message(
            chat_id=user.id,
            text=text,
            parse_mode=ParseMode.HTML,
        )

        return

    if len(context.args) > 1:
        text = (
            f"⚠️ You have entered multiple values!\n"
            f"Please provide only one number. Example:\n"
            f"<blockquote><code>/add_points 10</code></blockquote>"
        )

        await context.bot.send_message(
            chat_id=user.id,
            text=text,
            parse_mode=ParseMode.HTML,
        )
        return

    if len(context.args) == 1:
        try:
            points_to_add = int(context.args[0])
            text = (
                f"You have requested to add <b>{points_to_add}</b> points! 🎉\n"
                f"⏳ Please wait <b>3 seconds</b> for confirmation..."
            )

            await context.bot.send_message(
                chat_id=user.id,
                text=text,
                parse_mode=ParseMode.HTML,
            )

        except ValueError:
            text = (
                f"⚠️ Invalid input!\n"
                f"Please send a valid number. Example:\n"
                f"<blockquote><code>/add_points 10</code></blockquote>"
            )
            await context.bot.send_message(
                chat_id=user.id,
                text=text,
                parse_mode=ParseMode.HTML,
            )
            return

        await context.bot.send_chat_action(user.id, ChatAction.TYPING)

        ## here i will check if the points value is 0 or less than this, means if negative
        # it will exit this fun by sayuing to provide a positive goo value

        if points_to_add <= 0:
            text = (
                f"⚠️ Invalid points amount!\n"
                f"Please enter a positive number greater than 0.\n"
                f"Example:\n<blockquote><code>/add_points 10</code></blockquote>"
            )
            await context.bot.send_message(
                chat_id=user.id,
                text=text,
                parse_mode=ParseMode.HTML,
            )
            return

        if points_to_add > 30:
            text = (
                f"⚠️ You are requesting too many points ({points_to_add})!\n"
                f"🔹 The maximum allowed per request is <b>30</b> points.\n"
                f"Please enter a smaller value.\n"
                f"Example:\n<blockquote><code>/add_points 20</code></blockquote>\n"
                f"If you want to add many points pls contact admin."
            )
            await context.bot.send_message(
                chat_id=user.id,
                text=text,
                parse_mode=ParseMode.HTML,
            )
            return

        # i made at last as i want to open the database and check only when the condition
        # all got satisfied.

        with Session(engine) as session:
            statement = select(UserPart).where(UserPart.user_id == user.id)
            results = session.exec(statement)
            user_row = results.first()

        if user_row is None:
            logger.warning(f"{user.full_name} is not register.")
            text = (
                f"Sorry, {user.full_name} 😢\n"
                "You are not register in the database first go to Bot and send"
                f"/register or /register_me then come back."
            )
            await context.bot.send_message(
                chat_id=user.id,
                text=text,
                parse_mode=ParseMode.HTML,
            )
            return

        with Session(engine) as session:

            user_row.points += points_to_add
            session.add(user_row)
            session.commit()
            session.refresh(user_row)

        print(user_row)

        await asyncio.sleep(1)

        text = (
            f"✅ {points_to_add} Points have been successfully added! 🎉\n"
            f"🏆 Your Current Points is: <b>{user_row.points}</b>"
        )
        await context.bot.send_message(
            chat_id=user.id,
            text=text,
            parse_mode=ParseMode.HTML,
        )
