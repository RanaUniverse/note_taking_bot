"""
No Use Of This Module ❌❌❌

This code is good, and it is easy as a fun will run
in a interval, this is just for testing
"""

import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""
    await update.message.reply_text("Hi! Use /set <seconds> to set a timer")


async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""
    job = context.job
    await context.bot.send_message(
        job.chat_id, text=f"Beep! {job.data} seconds are over!"
    )


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""
    chat_id = update.effective_message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = float(context.args[0])
        if due < 0:
            await update.effective_message.reply_text(
                "Sorry we can not go back to future!"
            )
            return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(
            alarm, due, chat_id=chat_id, name=str(chat_id), data=due
        )

        text = "Timer successfully set!"
        if job_removed:
            text += " Old one was removed."
        await update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /set <seconds>")

    except Exception as e:
        print("Soemthign wrong", e)


async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = (
        "Timer successfully cancelled!" if job_removed else "You have no active timer."
    )
    await update.message.reply_text(text)


import datetime

IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))


async def callback_alarm(context: ContextTypes.DEFAULT_TYPE):
    now_time = datetime.datetime.now(IST)
    text = f"Current Time is: {now_time}"

    await context.bot.send_message(
        chat_id=context.job.user_id,
        text=text,
    )


async def callback_timer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # chat_id = update.message.chat_id
    if update.message is None or update.message:
        return
    user = update.message.from_user
    text = "Setting a timer for continuous beep!"

    await context.bot.send_message(
        chat_id=user.id,
        text=text,
    )

    # context.job_queue.run_once(callback_alarm, 1, data=name, chat_id=chat_id)

    context.job_queue.run_repeating(
        callback_alarm,
        interval=3,
        first=0,
        user_id=user.id,
    )


def main() -> None:
    """Run bot."""
    # Create the Application and pass it your bot's token.
    load_dotenv()
    BOT_TOKEN = os.environ.get("BOT_TOKEN")

    if BOT_TOKEN is None:
        print(
            ".no .env file or env file has not any bot token. Please make sure the token is there and rerun this program."
        )
        return
    application = Application.builder().token(BOT_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler(["start"], start))
    application.add_handler(CommandHandler("set", set_timer))
    application.add_handler(CommandHandler("unset", unset))
    application.add_handler(CommandHandler("help", callback_timer))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
