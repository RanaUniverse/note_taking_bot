"""
This python code is for just checking, though this not need, maybe i will use echo just for nothing
"""

import asyncio


from telegram import ReplyParameters
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatAction

from my_modules import bot_config_settings

from my_modules.logger_related import RanaLogger

from my_modules.rana_needed_things import make_footer_text
from my_modules.rana_needed_things import create_txt_file_from_string
from gemini_api_modules.gemini_api import answer_question_from_ai

# from my_modules.logger_related import RanaLogger

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
        # RanaLogger.info(f"Temporary File has been remoed from ssd.")
        file_path.unlink(missing_ok=True)
        return None


async def text_msg_come_from_private(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    When a text message will come what to do it will decide
    For now i want it will ask the gemini ai to send the question's answer.
    """

    user = update.effective_user
    msg = update.effective_message

    if user is None:
        RanaLogger.warning("This user need to be there")
        return None

    if msg is None:
        RanaLogger.warning(f"Message need to be there.")
        return None

    if not msg.text:
        return None

    user_question = msg.text
    first_reply_text = (
        f"👋 Hello {user.mention_html()},\n\n"
        f"⏳ Please wait while I process your question using our AI model 🤖..."
    )
    await msg.reply_html(text=first_reply_text)

    await msg.reply_chat_action(ChatAction.TYPING)

    try:
        user_answer = answer_question_from_ai(user_question)
        if user_answer:
            await msg.reply_html(user_answer)
        else:
            await msg.reply_html("⚠️ Sorry, I couldn't get an answer from the AI.")

    except Exception as e:
        RanaLogger.error(f"AI processing failed: {e}")
        await msg.reply_html("❌ Something went wrong while processing your question.")
