"""
This python code is for just checking, though this not need, maybe i will use echo just for nothing
"""

import asyncio


from telegram import ReplyParameters
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from my_modules import bot_config_settings

from my_modules.rana_needed_things import make_footer_text
from my_modules.rana_needed_things import create_txt_file_from_string

from my_modules.logger_related import RanaLogger

WILL_TEM_NOTE_DELETE = bot_config_settings.WILL_TEM_NOTE_DELETE


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


async def text_msg_to_txt_file(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """For now i will keep this for checking and make the txt file"""

    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None or msg.text is None:
        return None

    text = f"{msg.text}" + make_footer_text(user=user, use_current_time=True)

    # filename = "user_message.txt"
    filename = f"user_id_{user.id}_time_{int(msg.date.timestamp())}.txt"
    file_path = create_txt_file_from_string(content=text, filename=filename)

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

    new_caption += f"TXT File has been deleted from server."

    await file_send.edit_caption(caption=new_caption, parse_mode=ParseMode.HTML)

    if WILL_TEM_NOTE_DELETE:
        RanaLogger.info(f"Temporary File has been remoed from ssd.")
        file_path.unlink(missing_ok=True)
        return None
