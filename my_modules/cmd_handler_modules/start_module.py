"""
No Use Of This Module ❌❌❌

/start From User Direct Message
/start From Group Chat


"""

import asyncio

from telegram import Update
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

from telegram.constants import ChatAction, ParseMode

from telegram.ext import ContextTypes

from my_modules import bot_config_settings
from my_modules import message_templates
from my_modules import inline_keyboard_buttons

from my_modules.logger_related import RanaLogger


BOT_USERNAME = bot_config_settings.BOT_USERNAME


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    When user sends /start in private chat, this executes
    """

    msg = update.effective_message
    user = update.effective_user

    if msg is None or user is None:
        RanaLogger.warning(f"when /start come in private msg & user must present.")
        return None

    reply_text = message_templates.start_text_for_private(user=user)

    start_button = inline_keyboard_buttons.START_SIMPLE_KEYBOARD
    await context.bot.send_message(
        chat_id=user.id,
        text=reply_text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(start_button),
    )


async def start_cmd_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    When a /start come in any group.
    i need to use chat, as user maybe not available when user is hidden admin
    using the chat object (not user) since the sender could be anonymous.

    """
    chat = update.effective_chat

    if chat is None:
        RanaLogger.warning("/start in group it should has the chat obj")
        return None

    reply_text = message_templates.start_text_for_group(chat_obj=chat)

    url_value = f"https://t.me/{BOT_USERNAME}?start=group_start_{chat.id}"

    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Go to Private Chat",
                    url=url_value,
                ),
            ]
        ]
    )
    await context.bot.send_message(
        chat_id=chat.id,
        text=reply_text,
        parse_mode=ParseMode.HTML,
        reply_markup=button,
    )


async def start_cmd_from_group_to_private(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    This is a Normal Deep Link Which say user to go to private chat...
    This will execute when /start has a deep link which comes
    from the group /start button to private chat this is very
    just for a differentiate how to use this
    """

    if context.args is None:
        RanaLogger.warning("When deep link is used the value should has somethign")
        return None

    msg = update.effective_message
    user = update.effective_user
    if msg is None or user is None:
        RanaLogger.warning(f"On start deeplink the msg and user should present.")
        return None

    if context.args[0].startswith("group_start_"):

        RanaLogger.info(f"{user.full_name} now came to private chat from any group.")
        group_id = context.args[0].removeprefix("group_start_")

        reply_text = message_templates.deeplink_simple_group_start_text(
            group_id=group_id
        )

        await context.bot.send_message(
            chat_id=user.id,
            text=reply_text,
            parse_mode=ParseMode.HTML,
        )
        await context.bot.send_chat_action(user.id, ChatAction.TYPING)
        await asyncio.sleep(3)

        # Now it will send the actual /start form the private like same
        await start_cmd(update=update, context=context)

    else:
        RanaLogger.info(f"{user.full_name} send a new type of /start deeplink")
        text = (
            "⚠️ Unknown deep link\n\n"
            "It looks like you tried to use a special link, but "
            "this feature isn't available yet.\n"
            "Please wait for a future update, or simply type /start "
            "to begin using the bot. 😊"
        )

        await context.bot.send_message(
            chat_id=user.id,
            text=text,
            parse_mode=ParseMode.HTML,
        )
