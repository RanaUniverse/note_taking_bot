"""
some buttons will be separated in this file
i will kept them for easy editable and easy to separate the logics
"""

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


from my_modules import inline_keyboard_buttons
from my_modules import message_templates
from my_modules import bot_config_settings

from my_modules.database_code import db_functions
from my_modules.database_code.database_make import engine
from my_modules.logger_related import RanaLogger


ACCOUNT_DETAILS_BUTTON = inline_keyboard_buttons.ACCOUNT_DETAILS_BUTTON
UPGRADE_ACCOUNT_PRO_WEBSITE = bot_config_settings.UPGRADE_ACCOUNT_PRO_WEBSITE
FEEDBACK_EMAIL_ID = bot_config_settings.FEEDBACK_EMAIL_ID


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


async def upgrade_to_pro_member_button_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    When user will press the upgrade to pro button this will handle this function

        UPGRADE_PRO_BUTTON = InlineKeyboardButton(
            text="💎 Upgrade to Pro Plan",
            callback_data="upgrade_to_pro_user",
        )
    """
    user = update.effective_user
    msg = update.effective_message

    if msg is None or user is None:
        RanaLogger.warning(f"user msg should be present when account upgrade to Pro")
        return None

    query = update.callback_query
    if query is None:
        RanaLogger.warning(
            f"Query should be present of press button of 'upgrade_to_pro_user'"
        )
        return None

    await query.answer(text="🚧 Pro Features Coming Soon!", show_alert=True)

    reply_text = (
        f"💎 <b>Upgrade to Pro Plan</b>\n\n"
        f"Hey {user.mention_html()}! Ready to unlock more power? 🚀\n\n"
        f"✅ <b>Pro Benefits Include:</b>\n"
        f"• More note storage 📦\n"
        f"• Priority support 🛠️\n"
        f"• Special Pro-only features ✨\n\n"
        f"🌐 Visit our website to learn more:\n"
        f"<a href='{UPGRADE_ACCOUNT_PRO_WEBSITE}'>🔗 Upgrade to Pro</a>\n\n"
        f"📞 Or contact the admin anytime if you’d like early access."
    )

    await msg.reply_html(text=reply_text)


async def settings_button_pressed_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    wehn the settings button is presed this will executes for now this is
    just a demo just kept as a things to keep
        SETTINGS_BUTTON = InlineKeyboardButton(
        text="⚙️ Settings",
        callback_data="open_settings",
    )

    """

    user = update.effective_user
    msg = update.effective_message

    if msg is None or user is None:
        RanaLogger.warning(f"user msg should be present when account upgrade to Pro")
        return None

    query = update.callback_query
    if query is None:
        RanaLogger.warning(
            f"Query should be present of press button of 'upgrade_to_pro_user'"
        )
        return None

    await query.answer(
        text="⚙️ Settings are not available yet. "
        "Please stay tuned for the next update! 🔄",
        show_alert=True,
    )


async def feedback_button_pressed_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    This handler is triggered when the Feedback button is pressed.
    Currently, direct feedback through chat is not supported.
    Users are advised to use /help or send feedback via email.

        FEEDBACK_BUTTON = InlineKeyboardButton(
            text="💬 Feedback",
            callback_data="send_feedback",
        )
    """
    user = update.effective_user
    msg = update.effective_message

    if msg is None or user is None:
        RanaLogger.warning("User or message missing when pressing Feedback button")
        return None

    query = update.callback_query
    if query is None:
        RanaLogger.warning("Query missing for Feedback button press")
        return None
    await query.answer()
    text = (
        "💬 Feedback feature is not available directly in chat for now.\n\n"
        "👉 If you need help, use the /help command.\n"
        "📧 Or send your feedback to: " + FEEDBACK_EMAIL_ID
    )
    await msg.reply_html(text=text)
