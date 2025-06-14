"""
This file will contains some code related to
add some points which is used by user to make note and so on


for now i will make it as demo so that use can by himself add notes.

/add_points :- For now it will send by user and points will be added.

`/add_points 50` :- User need to send like this,

"""

import asyncio
import random

from sqlmodel import Session

from telegram import Update
from telegram.constants import ParseMode, ChatAction
from telegram.ext import ContextTypes


from my_modules import bot_config_settings
from my_modules import message_templates

from my_modules.database_code.database_make import engine
from my_modules.database_code.db_functions import (
    user_obj_from_user_id,
    add_point_to_user_obj,
)
from my_modules.logger_related import logger, RanaLogger


MAX_ADD_POINT = bot_config_settings.MAX_ADD_POINT

ADD_POINT_WAIT_TIME = bot_config_settings.ADD_POINT_WAIT_TIME


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

        if points_to_add > MAX_ADD_POINT:
            text = (
                f"⚠️ You are requesting too many points ({points_to_add})!\n"
                f"🔹 The maximum allowed per request is <b>{MAX_ADD_POINT}</b> points.\n"
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
            return None

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

    random_point_value = random.randint(1, MAX_ADD_POINT)

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

        random_point_value = random.randint(1, MAX_ADD_POINT)

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
    random_point_value = random.randint(1, MAX_ADD_POINT)

    # Below lines execute means the real thigns come i need to check the value of the
    # args and then check and try to add the points in the database

    if context.args is None:
        RanaLogger.warning("on /add_points int_value the context.args should present")
        return None

    arg_value = context.args[0]

    try:
        points_to_add = int(arg_value)
        text_real_int = (
            f"👋 Hello {user.mention_html()},\n\n"
            f"🧾 You’ve requested to add <b>{points_to_add}</b> point(s) "
            "to your account.\n"
            f"⏳ Please wait <b>{ADD_POINT_WAIT_TIME}</b> seconds while "
            "we verify your account.\n\n"
            f"✅ We appreciate your patience!"
        )

        await msg.reply_html(text=text_real_int)
        # i want after this try will successful then the main db logic will come
        await msg.reply_chat_action(action=ChatAction.TYPING)

        await asyncio.sleep(ADD_POINT_WAIT_TIME)

    except ValueError:

        text_int_not = message_templates.invalid_int_value_in_add_points(
            user_obj=user,
            arg_value=arg_value,
            random_point_value=random_point_value,
        )

        await msg.reply_html(text=text_int_not)
        return None

    if points_to_add <= 0:
        text = (
            f"⚠️ <b>Invalid points amount!</b>\n\n"
            f"🚫 Please enter a <b>positive number greater than 0</b>.\n"
            f"💡 To try again, you can use this command:\n"
            f"<code>/add_points {random_point_value}</code> ✅"
        )

        await msg.reply_html(text)
        return None

    if points_to_add > MAX_ADD_POINT:
        text = (
            f"⚠️ <b>Too many points requested!</b>\n\n"
            f"❗ You asked for <b>{points_to_add}</b> points.\n"
            f"🔹 But the maximum allowed per request is <b>{MAX_ADD_POINT}</b> points.\n\n"
            f"💡 Please try a smaller number.\n"
            f"For example, use:\n"
            f"<code>/add_points {random_point_value}</code> ✅\n\n"
            f"📞 Want to add more points? Contact the admin with <code>/admin</code> "
            "or <code>/help</code>."
        )

        await msg.reply_html(text)
        return None

    # Now first i will find the user obj existance
    # if user not exists it will say user to first register
    # if user exists then it will add the points in the obj and say the information

    user_row = user_obj_from_user_id(engine=engine, user_id=user.id)

    if user_row is None:
        text_no_user = message_templates.prompt_user_to_register(user=user)
        await msg.reply_html(text=text_no_user)
        return

    # Now lets add the point to account
    # i use try except here because i didn't use try except in the function.

    try:
        new_user_row = add_point_to_user_obj(engine, user_row, points_to_add)

        text = (
            f"👋 Hello {user.mention_html()},\n"
            f"✅ Your request to add 💰 {points_to_add} Points has been successful!\n\n"
            f"📊 Your New Point Balance is: 🎯 {new_user_row.points}"
        )

    except Exception as e:
        RanaLogger.warning("Some Error happens here." "\n" f"{e}")
        text = f"Here is some problem in our Side. Please Report to Admin."

    await msg.reply_html(text)
