"""
i will write help cmd code here
"""

from telegram import Update

from telegram.ext import ContextTypes

from my_modules import bot_config_settings
from my_modules import message_templates

from my_modules.logger_related import RanaLogger


GROUP_LINK = bot_config_settings.GROUP_LINK
BOT_INFORMATION_WEBSITE = bot_config_settings.BOT_INFORMATION_WEBSITE


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    When user send help command in private chat
    This will executes and say a normal things later i will extends this.
    """

    user = update.effective_user
    msg = update.effective_message

    if user is None:
        RanaLogger.warning("This user need to be there")
        return

    if msg is None:
        RanaLogger.warning(f"Message need to be there.")
        return

    help_text = message_templates.help_cmd_text()

    await msg.reply_html(text=help_text)


async def help_cmd_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    When user sends /help in a group chat, inform them that the bot is not available
    for group use i need to specefy that it need to use privately and send a demo group link.
    """

    user = update.effective_user

    if user is None:
        RanaLogger.warning("This user needs to be present for group /help.")
        return

    if update.effective_message is None:
        RanaLogger.warning("Message is required for group /help.")
        return

    text = message_templates.help_cmd_from_group_text(group_link=GROUP_LINK)

    await update.effective_message.reply_html(text)
