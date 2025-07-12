"""
I make this module which work is just for handle the response back to user

/ai user_quesion_here
This upper format is there which will call the gemini api and it will work
directly by my code below.
"""

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes


from my_modules.logger_related import RanaLogger
from gemini_api_modules.gemini_api import answer_question_from_ai


async def ai_response_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    When user send /ai command in private chat
    This will executes and say a normal things later i will extends this.
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

    user_question = (
        f"{' '.join(context.args)}"  # type: ignore
        f"\n"
        f"Please Wait i am sending you answer..."
    )

    await msg.reply_html(text=user_question)
    await msg.reply_chat_action(ChatAction.TYPING)

    user_answer = answer_question_from_ai(user_question)
    if user_answer:
        await msg.reply_html(user_answer)
