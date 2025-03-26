"""
this code will help to register a new user to the database
so that they can use this bot from next time.

I will use SqlModel here...

"""

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from telegram import Update
from telegram import InlineKeyboardMarkup

from telegram.ext import ContextTypes
from telegram.constants import ParseMode


from my_modules.database_code.database_make import engine
from my_modules.database_code.models_table import UserPart

from my_modules.some_inline_keyboards import MyInlineKeyboard


from my_modules.some_constants import IST


from my_modules.logger_related import logger


async def new_acc_register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    command=["register_me", "new_account", "register"],

    When user want to make his account he need to press this and bot will
    check his old details and then it will enter him in the datbase
    """

    if update.message is None or update.message.from_user is None:
        print("I used this to prevent the type hint of pyright.")
        return

    user = update.message.from_user
    user_mention = f'<a href="tg://user?id={user.id}">{user.full_name}</a>'

    # Below part code will try to save the user details in the user table. with try except also
    # i will make the user row instance and then in try except i will
    user_row = UserPart(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        account_creation_time=update.message.date.astimezone(IST),
    )

    try:
        with Session(engine) as session:
            session.add(user_row)
            session.commit()
            session.refresh(user_row)

        first_name = user_row.first_name or ""
        last_name = user_row.last_name or ""
        full_name = first_name + last_name
        user_id = user_row.user_id
        username = f"@{user_row.username}" if user_row.username else "Not Available"
        note_count = user_row.note_count if user_row.note_count else "0"
        email_id = user_row.email_id if user_row.email_id else "❌❌❌"
        phone_no = user_row.phone_no if user_row.phone_no else "❌❌❌"

        text = (
            f"Hello {user_mention}, You Have successfully registered now on our side.\n"
            f"Your Current Information is:\n\n"
            f"<b>Name</b>:- {full_name}\n"
            f"<b>Username</b>:- {username}\n"
            f"<b>UserId</b>:- <code>{user_id}</code>\n"
            f"<b>Note Count</b>:- {note_count}\n"
            f"<b>Email Id</b>:- {email_id}\n"
            f"<b>Phone Number</b>:- {phone_no}\n"
            f"Please Press The Buttons Below to add some more information.👇👇👇"
        )
        await context.bot.send_message(
            chat_id=user.id,
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(MyInlineKeyboard.ACCOUNT_REGISTER.value),
        )

    except IntegrityError as e:
        logger.info(e)
        # It will check if the user is in the database or not, if in database
        # then it will say him his details, otherwise, say to contact customer care
        with Session(engine) as session:
            statement = select(UserPart).where(UserPart.user_id == user.id)
            results = session.exec(statement)
            user_row = results.first()

        if user_row is None:
            logger.warning(f"This should not happens")
            return

        text = (
            f"Hello {user_mention}, You are already register in our side, you dont "
            f"need to register here again, you can simply use this bot."
            f"\n\n"
            f"{user_row}"
        )
        await context.bot.send_message(
            chat_id=user.id,
            text=text,
            parse_mode=ParseMode.HTML,
        )

    except Exception as e:
        logger.info(e)
        print("Something wrong happens")
        text = f"Hello Somethings Unexpected happesn"
        await context.bot.send_message(user.id, text)

        # it will try to say him to contact admin, as still now i dont get any concept
        # why this can happens.
