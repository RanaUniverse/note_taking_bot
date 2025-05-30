"""
This file will contains some code related to
add some points which is used by user to make note and so on


for now i will make it as demo so that use can by himself add notes.

/add_points :- For now it will send by user and points will be added.

`/add_points 50` :- User need to send like this,

"""

import asyncio
import html
import random

from sqlmodel import Session

from telegram import Update
from telegram.constants import ParseMode, ChatAction
from telegram.ext import ContextTypes


from my_modules.database_code.database_make import engine
from my_modules.database_code.db_functions import (
    user_obj_from_user_id,
    add_point_to_user_obj,
)
from my_modules.logger_related import logger, RanaLogger
from my_modules.some_constants import BotSettingsValue

MAX_POINT = BotSettingsValue.MAX_ADD_POINT.value

ADD_POINT_WAIT = BotSettingsValue.ADD_POINT_WAIT_TIME.value


async def add_points_cmd_old(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Currently This will not work as i dont need to use this logic
    i separate this in below differetn functions.
    When user will send /add_points

    if user dont send any value after the command it will ask him to send right
    """

    if update.message is None or update.message.from_user is None:
        print("I used this to prevent the type hint of pyright. in add_points_cmd")
        return

    user = update.message.from_user

    if context.args is None:
        print("This is unexpected 🍌🍌🍌")
        return

    if len(context.args) == 0:

        text = (
            f"You haven't pass any argument after this command."
            f"You need to send how many points you want to add.\n"
            f"Example: Suppose You want to get 10 points, then send this below to bot.\n"
            f"<blockquote><code>/add_points 10</code></blockquote>"
        )

        await context.bot.send_message(
            chat_id=user.id,
            text=text,
            parse_mode=ParseMode.HTML,
        )

        return None

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
        return None

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
            return None

        await context.bot.send_chat_action(user.id, ChatAction.TYPING)

        # here i will check if the points value is 0 or less than this, means if negative
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
            return None

        if points_to_add > MAX_POINT:
            text = (
                f"⚠️ You are requesting too many points ({points_to_add})!\n"
                f"🔹 The maximum allowed per request is <b>{MAX_POINT}</b> points.\n"
                f"Please enter a smaller value.\n"
                f"Example:\n<blockquote><code>/add_points 20</code></blockquote>\n"
                f"If you want to add many points pls contact admin (/admin)."
            )
            await context.bot.send_message(
                chat_id=user.id,
                text=text,
                parse_mode=ParseMode.HTML,
            )
            return

        # i made at last as i want to open the database and check only when the condition
        # all got satisfied.

        user_row = user_obj_from_user_id(engine, user.id)

        if user_row is None:
            logger.warning(
                f"{user.full_name} is not register but trying to add points."
            )
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

        logger.info(f"{user.full_name} has added {points_to_add} point.")
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


async def add_points_cmd_no_arg(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    When user will only send
    '/add_points'
    it will executes and say user to send this in correct format
    """
    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None:
        RanaLogger.warning(
            "When /add_points will execute with no args it must "
            "have the user and msg"
        )
        return None

    random_point_value = random.randint(1, BotSettingsValue.MAX_ADD_POINT.value)

    text_msg = (
        f"👋 Hello {user.mention_html()}, "
        f"To add point to your account "
        f"Please send the message in correct format:\n\n"
        f"<code>/add_points &lt;number_of_points&gt;</code>\n\n"
        f"To add {random_point_value} Points, please send me 👇🏻👇🏻👇🏻\n"
        f"<code>/add_points {random_point_value}</code> ✅"
    )

    await msg.reply_html(text_msg)


async def add_points_cmd_many_args(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    When user will send /add_points int and more than 1 words
    it will execute for even not passing any value it will call another fun
    the main logic is it will try to add the points to the account of the user
     len(context.args) > 1:
    This is the condition for this.
    """
    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None:
        RanaLogger.warning(
            "When /add_points with args come it must " "have the user and msg"
        )
        return None

    if context.args is None:
        RanaLogger.warning(
            "on /add_points with args athe context.args should present in /add_point with many args"
        )
        return None

    if len(context.args) > 1:

        random_point_value = random.randint(1, BotSettingsValue.MAX_ADD_POINT.value)

        text = (
            f"⚠️ You have entered multiple values!\n"
            f"Please provide only one number. Example:\n"
            f"<code>/add_points &lt;number_of_points&gt;</code>\n\n"
            f"To add {random_point_value} Points, please send me 👇🏻👇🏻👇🏻\n"
            f"<code>/add_points {random_point_value}</code> ✅"
        )

        await msg.reply_html(
            text=text,
        )
        return None


# This is the special main things to add points to user
async def add_points_cmd_one_arg(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    This is the main add point logic function
    /add_points int_value
    This case when will be this will execute when
    len(context.args) == 1
    """

    user = update.effective_user
    msg = update.effective_message
    if user is None or msg is None:
        RanaLogger.warning(
            f"On /add_points int of 1 args the user and msg will be present must"
        )
        return None
    random_point_value = random.randint(1, BotSettingsValue.MAX_ADD_POINT.value)

    # Below lines execute means the real thigns come i need to check the value of the
    # args and then check and try to add the points in the database

    if context.args is None:
        print("on /add_points int_value the context.args should present")
        return None

    arg_value = context.args[0]

    try:
        points_to_add = int(arg_value)
        text_real_int = (
            f"Hello {user.mention_html()}, you have requested "
            f"to add {points_to_add} point in ur account. "
            f"Please wait {ADD_POINT_WAIT} Seconds to verify your account."
        )
        await msg.reply_html(text=text_real_int)
        # i want after this try will successful then the main db logic will come
        await msg.reply_chat_action(action=ChatAction.TYPING)

        await asyncio.sleep(ADD_POINT_WAIT)

    except ValueError:

        text_int_not = (
            f"👋 Hello {user.mention_html()}, you sent 👇🏻\n\n"
            f"<code>{html.escape(arg_value)}</code> — "
            f"but this is not a valid number of points.\n\n"
            f"As a example "
            f"to add {random_point_value} points, please send this command:\n"
            f"<code>/add_points {random_point_value}</code> ✅"
        )

        await msg.reply_html(text=text_int_not)
        return None

    if points_to_add <= 0:
        text = (
            f"⚠️ Invalid points amount!\n"
            f"Please enter a positive number greater than 0.\n"
            f"To add {random_point_value} points, please send this command:\n"
            f"<code>/add_points {random_point_value}</code> ✅"
        )
        await msg.reply_html(text)
        return None

    if points_to_add > MAX_POINT:
        text = (
            f"⚠️ You are requesting too many points ({points_to_add})!\n"
            f"🔹 The maximum allowed per request is <b>{MAX_POINT}</b> points.\n"
            f"Please enter a smaller value.\n"
            f"To add {random_point_value} points, please send this command:\n"
            f"<code>/add_points {random_point_value}</code> ✅\n"
            f"If you want to add many points pls contact admin (/admin or /help)."
        )
        await msg.reply_html(text)
        return None

    # Now first i will find the user obj existance
    # if user not exists it will say user to first register
    # if user exists then it will add the points in the obj and say the information

    user_row = user_obj_from_user_id(engine=engine, user_id=user.id)

    if user_row is None:
        text_no_user = (
            f"Hello {user.mention_html()},"
            f" it seems you are not register in our system "
            f"Please go and register first with /register_me. "
            f"You can also /help"
        )
        await msg.reply_html(text=text_no_user)
        return

    # Now lets add the point to account

    new_user_row = add_point_to_user_obj(engine, user_row, points_to_add)

    # text = f"Your New Point is: "f"{user_row.points}"
    # await msg.reply_html(text)

    # Though upper is working but i am confused on upper code working,
    # why the old user row is working

    text = (
        f"👋 Hello {user.mention_html()},\n"
        f"✅ Your request to add 💰 {points_to_add} Points has been successful!\n\n"
        f"📊 Your New Point Balance is: 🎯 {new_user_row.points}"
    )
    await msg.reply_html(text)
