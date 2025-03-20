"""
Run this in the place of main.py location
"""

import os

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ContextTypes,
    Application,
    CommandHandler,
    # MessageHandler,
    # filters,
)

from telegram.constants import ParseMode

# Below part is for generate a fake things
from faker import Faker

from pydantic import ValidationError
from my_modules.pydantic_validation_logic import UserEmailValidate


fake = Faker()


async def email_storing_wrong(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    For now when user will send something:
    /email some_email_id another email
    This will execute when user send wrong args
    """

    if (
        update.message is None
        or update.message.text is None
        or update.message.from_user is None
    ):
        print("This should not happens")
        return

    if context.args is None:
        print("This should not execute")
        return

    args_count = len(context.args)
    user = update.message.from_user
    user_msg = update.message.text
    print("Somethings happens")
    text = (
        f"Hello {user.full_name}, You have send me {args_count} args,"
        f"you must send exactly one email address that is ur."
        f"\n\n"
        f"But You send me: \n"
        f"{user_msg}"
    )
    await context.bot.send_message(user.id, text, ParseMode.HTML)


async def email_storing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    just a learning way of store user's email id
    ...
    For now when user will send something:
    /email some_email_id
    when this has only one args
    """

    if (
        update.message is None
        or update.message.text is None
        or update.message.from_user is None
        or context.args is None
    ):
        print("This should not happens")
        return

    if len(context.args) != 1:
        print("This also not happens.")
        return

    user = update.message.from_user
    user_email = context.args[0]
    if context.user_data is None:
        print("nothing happens now.")
        return

    # First it will check if i have a email or not already if a email is then return quickly
    existing_email = context.user_data.get("email")
    if existing_email:
        text = f"You have a email already, {existing_email}"
        await context.bot.send_message(user.id, text)
        return

    try:
        email_instance = UserEmailValidate(email=user_email)
        text = (
            f"YOu have send me a valid email id: {email_instance.email} which is ok, "
            "i am storing this in my side, you can get it back by sending "
            "/my_email and i will send you back"
        )
        context.user_data["email"] = user_email
        print("Context.user data is: ", context.user_data)
    except ValidationError as e:
        print(e)
        fake_email = fake.email()
        text = (
            f"You have send me a email id {user_email}, which is not accepted "
            f"so i am making a new email and store this for you.\n\n"
            f"{fake_email}"
        )
        context.user_data["email"] = fake_email
        print("Context.user data is: ", context.user_data)

    except Exception as e:
        print(e)
        print("I dont know what worng here...")
        return

    await context.bot.send_message(user.id, text, ParseMode.HTML)


async def my_email_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    when user will send /my_email it will search for data and send it back
    """
    print("This my email command got from user.")
    if (
        update.message is None
        or update.message.text is None
        or update.message.from_user is None
        or context.args is None
    ):
        print("This should not happens")
        return

    user = update.message.from_user

    if not context.user_data:
        print("context.user data is none so nothing works")

        text = (
            f"Your have not set any email id pls set in /email followed by ur mail id."
        )

        await context.bot.send_message(user.id, text, ParseMode.HTML)
        return

    value = context.user_data.get("email", "Not found")

    text = f"Your Email id which i have is: \n" f"{value}"

    await context.bot.send_message(user.id, text, ParseMode.HTML)


async def del_user_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    This will help me to del the user email dict completely
    """
    if update.message is None or update.message.from_user is None:
        return
    if context.user_data is None:
        print("Nothing special")
        return
    user = update.message.from_user
    text = f"You have clear ur all history"
    context.user_data.clear()
    await context.bot.send_message(user.id, text, ParseMode.HTML)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    load_dotenv()

    BOT_TOKEN = os.environ.get("BOT_TOKEN")

    if BOT_TOKEN is None:
        print(
            ".no .env file or env file has not any bot token. Please make sure the token is there and re run this program."
        )
        return
    print("Bot is running here...")
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(
        CommandHandler(
            command=["email", "e"],
            callback=email_storing,
            block=False,
            has_args=1,
        )
    )
    application.add_handler(
        CommandHandler(
            command=["email", "e"],
            callback=email_storing_wrong,
            block=False,
            has_args=None,
        )
    )

    application.add_handler(
        CommandHandler(
            command=["my_email"],
            callback=my_email_id,
            block=False,
            has_args=None,
        )
    )
    application.add_handler(
        CommandHandler(
            command=["del_my_email", "d", "del"],
            callback=del_user_email,
            block=False,
            has_args=None,
        )
    )

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
