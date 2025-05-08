"""
This python code is for just checking, though this not need, maybe i will use echo just for nothing
"""

import asyncio
import datetime

from pathlib import Path

from telegram import ReplyParameters
from telegram import Update
from telegram import User
from telegram.ext import ContextTypes
from telegram.constants import ParseMode


async def echo_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """This is just send same message to user with the"""

    if (
        update.message is None
        or update.message.from_user is None
        or update.message.text is None
    ):
        print("I used this to prevent the type hint of pyright. for any text msg")
        return

    user = update.message.from_user
    user_text = update.message.text

    print(user_text)

    text_100 = f"{user_text.upper()[0:100]} ..."
    text = (
        f"Hello {user.first_name} You have send me the text of {len(user_text)} character, whose first max 100 character is below: \n\n"
        f"<blockquote>{text_100}</blockquote>"
    )

    await context.bot.send_message(user.id, text, ParseMode.HTML)


def make_footer_text(user: User, now_time: datetime.datetime) -> str:
    """
    i though to make a footer where it will give me
    user some informaiton and the time
    """

    username = f"@{user.username}" if user.username else "Not Available ❌"

    breaking_str = f"\n\n\n\n\n" f"----------" f"\n"

    user_info = (
        f"Full Name: {user.full_name}\n"
        f"UserID: {user.id}\n"
        f"Username: {username}\n"
    )
    time_str = (
        f"\n\n\n\n\n"
        f"----------"
        f"\n"
        f"Response Time: \n{now_time}"
        f"\n\n\n\n\n"
        f"----------"
        f"\n"
    )
    output_txt = breaking_str + user_info + time_str

    return output_txt


async def text_msg_to_txt_file(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """For now i will keep this for checking and make the txt file"""

    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None:
        return

    utc_time = msg.date.replace(tzinfo=None)
    current_ind_time = utc_time + datetime.timedelta(hours=5, minutes=30)

    text = f"{msg.text}" + make_footer_text(user=user, now_time=current_ind_time)

    # filename = "user_message.txt"
    filename = f"user_id_{user.id}_time_{int(msg.date.timestamp())}.txt"

    file_dir = Path.cwd() / "000_user_msg"

    file_path = file_dir / filename

    file_dir.mkdir(parents=True, exist_ok=True)

    file_path.write_text(text)

    old_caption = "📄 <b>Document Sent By The Echo Function</b>"

    file_send = await context.bot.send_document(
        chat_id=user.id,
        document=file_path,
        caption=old_caption,
        parse_mode=ParseMode.HTML,
        reply_parameters=ReplyParameters(msg.id),
    )

    if file_send.document is None:
        print("This docs should be present this is just for checking")
        return None

    new_caption = (
        "📄 <b>Document Details</b> 🍌\n"
        f"File Name: {file_send.document.file_name}\n"
        f"File ID: <code>{file_send.document.file_id}</code>\n"
    )

    await asyncio.sleep(1)

    # i want it will first delete the file and then only send the updated caption
    # so that it will also sure nothign wrong happens here
    file_path.unlink(missing_ok=True)

    await file_send.edit_caption(caption=new_caption, parse_mode=ParseMode.HTML)
