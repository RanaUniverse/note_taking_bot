"""
This module is for making new handler for conversation to make new account
"""

from pydantic import (
    BaseModel,
    EmailStr,
    ValidationError,
)


from telegram import Update

from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from telegram.constants import ParseMode


from my_modules.logger_related import logger


class EmailValidator(BaseModel):
    email: EmailStr


EMAIL, OTP, PASSWORD, PASSWORD_AGAIN, CONFIRMATION = range(5)


OTP_LIST = [
    111111,
    222222,
    333333,
    123123,
    444444,
    555555,
    666666,
    777777,
    888888,
    999999,
    101010,
    121212,
    131313,
    141414,
    151515,
    161616,
    171717,
    181818,
    191919,
]


async def new_account_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    This will start message shows to user on when they
    start the new account making conversation.
    Assume this fun will run when user want to create a new account.
    """
    if update.message is None or update.message.from_user is None:
        logger.warning(
            f"Something in my side cause some problme so conv is ending at now time."
        )
        return ConversationHandler.END

    user = update.message.from_user
    text = (
        f"Hello <b>{user.first_name}</b>"
        f"Thanks for your interest to make new account here.\n\n"
        f"Send your email address to verify and start making new account."
    )
    await context.bot.send_message(user.id, text, ParseMode.HTML)

    return EMAIL


async def get_the_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    This will execute when user will send email, it is for check the email
    address's existance, and as a fake for now it will say it will send a email
    otp to email of the user as till now i have no email service, i make this by
    thinking i have a email service.
    """

    if (
        update.message is None
        or update.message.from_user is None
        or update.message.text is None
    ):
        logger.warning(
            f"Something in my side cause some problme so conv is ending at now time."
        )
        return ConversationHandler.END

    user = update.message.from_user
    user_msg = update.message.text

    first_text = (
        f"Hello {user.full_name} You have send me your email, let's verify this email address,"
        f"\n\n"
        f"<blockquote>{user_msg}</blockquote>"
        f"\n\n"
    )

    try:
        validated_email = EmailValidator(email=user_msg)
        email = validated_email.email
        text = (
            f"{first_text}"
            f"✅ Valid email: \n\n<b>{email}</b>\n\n"
            f"For Now my backend is not set to send you otp to email, "
            f"rather i am making a fake otp to this chat for now."
            f"I will send you otp here in 3 second and del after 5 seconds."
            f"\n\n"
            f"{OTP_LIST}"
        )

        await context.bot.send_message(user.id, text, ParseMode.HTML)
        return OTP

    except ValidationError as e:
        logger.warning(
            f"Invalid email from user {user.full_name} (ID: {user.id}): {user_msg}\n{e}"
        )

        text = (
            f"{first_text}"
            f"❌ This is not a valid email id, so pls resend your email id and send it. "
            f"If you sure this is right email id, pls contact the admin /help."
        )
        await context.bot.send_message(user.id, text, ParseMode.HTML)
        return EMAIL


async def otp_verification(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    This is just a script to check if a otp is valid or not
    """
    if (
        update.message is None
        or update.message.from_user is None
        or update.message.text is None
    ):
        logger.warning(
            f"Something in my side cause some problme so conv is ending at now time."
        )
        return ConversationHandler.END

    user = update.message.from_user
    user_msg = update.message.text

    try:
        user_otp = int(user_msg)

    except ValueError:
        text = "❌ Invalid OTP format! Please enter a 6-digit numeric OTP.\n\n"
        f"(Example: 987654)"
        await context.bot.send_message(user.id, text, ParseMode.HTML)
        return OTP

    if user_otp in OTP_LIST:
        text = (
            "✅ This is a valid OTP.\n\n"
            "Your account has been created just you need to make a login password"
        )
        await context.bot.send_message(user.id, text, ParseMode.HTML)
        return PASSWORD

    else:
        text = "❌ This OTP is invalid. Please type the correct OTP again."
        await context.bot.send_message(user.id, text, ParseMode.HTML)
        return OTP


async def set_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    it will ask for a password from user and then it will
    """
    if (
        update.message is None
        or update.message.from_user is None
        or update.message.text is None
    ):
        logger.warning(
            f"Something in my side cause some problme so conv is ending at now time."
        )
        return ConversationHandler.END

    user = update.message.from_user
    user_msg = update.message.text

    text = (
        f"Your Password is: \n\n"
        f"<tg-spoiler>{user_msg}</tg-spoiler>\n\n"
        f"Please write this password again to confirm."
    )

    await context.bot.send_message(user.id, text, ParseMode.HTML)

    return PASSWORD_AGAIN


async def set_password_again(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    This is the place where i will enter the password again to confirm
    """
    if (
        update.message is None
        or update.message.from_user is None
        or update.message.text is None
    ):
        logger.warning(
            f"Something in my side cause some problme so conv is ending at now time."
        )
        return ConversationHandler.END

    user = update.message.from_user
    user_msg = update.message.text

    login_details = f"EMAIL ID: iamadog@example.com" f"\n\n" f"PASSWORD: my_password"

    text = (
        f"{user_msg}\n\n"
        f"This is a demo text, as till now i have not make thsi how i will do this "
        f"Here i write the password and this got match suppose. "
        f"Now Your account has been created successfully ✅✅✅\n\n"
        f"{login_details}"
    )

    await context.bot.send_message(user.id, text, ParseMode.HTML)
    return ConversationHandler.END


async def close_this_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """This will execute when user want to stop this making for now."""
    if update.message is None or update.message.from_user is None:
        logger.warning(
            f"Something in my side cause some problme so conv is ending at now time."
        )
        return ConversationHandler.END

    user = update.message.from_user
    text = (
        f"Hello <b>{user.full_name}</b>, "
        f"This time you are leaving this converstaion, "
        f"You can start this converstaion again with "
        f"/new, /new_account, /register "
        f"anytime you want to create a new accout here."
    )
    await context.bot.send_message(user.id, text, ParseMode.HTML)

    return ConversationHandler.END


conv_new_account = ConversationHandler(
    entry_points=[
        CommandHandler("new", new_account_start),
        CommandHandler("new_account", new_account_start),
        CommandHandler("register", new_account_start),
    ],
    states={
        EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_the_email)],
        OTP: [MessageHandler(filters.TEXT & ~filters.COMMAND, otp_verification)],
        PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_password)],
        PASSWORD_AGAIN: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, set_password_again)
        ],
    },
    fallbacks=[
        CommandHandler("cancel", close_this_chat),
        CommandHandler("abord_setup", close_this_chat),
        CommandHandler("start_later", close_this_chat),
    ],
)
