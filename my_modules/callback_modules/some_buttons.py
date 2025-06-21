"""
some buttons will be separated in this file
i will kept them for easy editable and easy to separate the logics
"""

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


from my_modules import inline_keyboard_buttons
from my_modules import message_templates

from my_modules.database_code import db_functions
from my_modules.database_code.database_make import engine
from my_modules.logger_related import RanaLogger


ACCOUNT_DETAILS_BUTTON = inline_keyboard_buttons.ACCOUNT_DETAILS_BUTTON


async def update_profile_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    When the button having this callback_data =update_profile
    i will make this separate just for easy development.
    """

    query = update.callback_query

    if query is None:
        return

    text = (
        f"You Need To Register here to use this bot, To register please send, \n"
        f"/register_me"
    )

    if query.data == "update_profile":
        # await query.answer(
        #     text="⚠️ You are going to edit your profile.🚧",
        #     show_alert=True,
        # )
        await query.edit_message_text(
            text=text,
            parse_mode=ParseMode.HTML,
        )


async def new_note_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = update.effective_message
    if msg is None:
        RanaLogger.warning("Button pressed but msg is none for new note making.")
        return None

    query = update.callback_query
    if query is None or query.data is None:
        RanaLogger.warning("Button pressed on new note confirm , but not query :cry")
        return None

    await query.answer()

    action, _ = query.data.split("_", 1)

    # Default messages for each action
    if action == "view":
        reply = "👀 Viewing note feature in development."
    elif action == "export":
        reply = "📤 Export feature in development."
    elif action == "delete":
        reply = "🗑️ Delete feature in development."
    elif action == "share":
        reply = "🔗 Share feature in development."
    else:
        reply = "⚠️ Unknown action."

    reply_text = reply + "\n" + "Please wait for next update"

    await msg.reply_html(text=reply_text, do_quote=True)


async def account_details_of_user_button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    When user want to know his account details by pressing a button
    This function will executes and it will result to shows some information to him

        ACCOUNT_DETAILS_BUTTON = InlineKeyboardButton(
            text="📊 View Account Details",
            callback_data="my_account_details",
        )
    """

    user = update.effective_user
    msg = update.effective_message
    if msg is None or user is None:
        RanaLogger.warning(
            f"user msg should be present when account details button pressed"
        )
        return None

    query = update.callback_query
    if query is None:
        RanaLogger.warning(
            f"Query should be present of press button of 'my_account_details'"
        )
        return None

    await query.answer(text="Let's See your Details.")

    user_row = db_functions.user_obj_from_user_id(engine, user.id)

    if user_row is None:
        no_register_text = message_templates.prompt_user_to_register(user)
        await msg.reply_html(text=no_register_text)
        return None
    user_info_text = message_templates.user_complete_details_text(
        tg_user_obj=user,
        user_row=user_row,
    )
    await msg.reply_html(text=user_info_text)
