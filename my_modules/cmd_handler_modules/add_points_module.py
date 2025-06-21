"""
This file will contains some code related to
add some points which is used by user to make note and so on


for now i will make it as demo so that use can by himself add notes.

/add_points :- For now it will send by user and points will be added.

`/add_points 50` :- User need to send like this,

"""

import asyncio
import random


from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes


from my_modules import bot_config_settings
from my_modules import message_templates

from my_modules.database_code.database_make import engine
from my_modules.database_code import db_functions
from my_modules.logger_related import RanaLogger


ADD_POINT_WAIT_TIME = bot_config_settings.ADD_POINT_WAIT_TIME
MAX_ADD_POINT = bot_config_settings.MAX_ADD_POINT


async def add_points_cmd_no_arg(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    When user will only send
    '/add_points'
    it will executes and say user to send this in correct format
    on how many point user want to add to his account
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
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
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


async def add_points_cmd_one_arg(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
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
            f"🧾 You've requested to add <b>{points_to_add}</b> point(s) to your account.\n"
            f"⏳ Please wait <b>{ADD_POINT_WAIT_TIME}</b> seconds "
            f"while we verify your request.\n\n"
            f"🚫 Kindly avoid sending any messages to the bot during "
            f"this time to ensure smooth processing.\n\n"
            f"✅ Thank you for your patience!"
        )

        await msg.reply_html(text=text_real_int)
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

    user_row = db_functions.user_obj_from_user_id(engine=engine, user_id=user.id)

    if user_row is None:
        text_no_user = message_templates.prompt_user_to_register(user=user)
        await msg.reply_html(text=text_no_user)
        return

    # Now lets add the point to account
    # i use try except here because i didn't use try except in the function.

    try:
        new_user_row = db_functions.add_point_to_user_obj(
            engine, user_row, points_to_add
        )

        text = (
            f"👋 Hello {user.mention_html()},\n"
            f"✅ Your request to add 💰 {points_to_add} Points has been successful!\n\n"
            f"📊 Your New Point Balance is: 🎯 {new_user_row.points}"
        )

    except Exception as e:
        RanaLogger.warning(
            "Some Error happens here, when points is adding to the user account column."
            "\n"
            f"{e}"
        )
        text = f"Here is some problem in our Side. Please Report to Admin."

    await msg.reply_html(text)
