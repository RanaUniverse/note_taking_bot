"""
Here i will keep some commands which i can use in
set_my_commands()
Now is in Development
"""

from pathlib import Path


from telegram import Update
from telegram import BotCommand
from telegram.ext import ContextTypes

from my_modules import bot_config_settings
from my_modules.logger_related import RanaLogger


ADMIN_ID = bot_config_settings.ADMIN_ID_1
LOG_FILE_NAME = bot_config_settings.LOG_FILE_NAME
DATABASE_FILE_NAME = bot_config_settings.DATABASE_FILE_NAME

cmds_list: list[BotCommand] = [
    BotCommand(
        command="start",
        description="🚀 Just Start This Bot",
    ),
    BotCommand(
        command="help",
        description="❓ Get help about available commands",
    ),
    BotCommand(
        command="settings",
        description="⚙️ Adjust your bot settings",
    ),
    BotCommand(
        command="register_me",
        description="📝 Register yourself in the bot",
    ),
    BotCommand(
        command="update_commands",
        description="🔄 Changes all the commands of this bot",
    ),
    BotCommand(
        command="new_note",
        description="🆕 Make a new note and store it",
    ),
    BotCommand(
        command="edit_note",
        description="✏️ Edit a note you created",
    ),
    BotCommand(
        command="fake_note",
        description="📝 Create a fake note for testing",
    ),
    BotCommand(
        command="my_notes",
        description="📒 Show all your saved notes",
    ),
    BotCommand(
        command="delete_note",
        description="❌ Delete a specific note",
    ),
    BotCommand(
        command="delete_me",
        description="🗑 Remove your registration and all your notes",
    ),
    BotCommand(
        command="add_points",
        description="💰 Add points to your account for new notes",
    ),
    BotCommand(
        command="my_account_details",
        description="See Your Account Informations",
    ),
]


async def update_commands_cmd(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Fully Experimental Not Use ❌
    This will have Telegram.Message update

    This is useful for when i want to add the commands for the bot
    for now i dont use database i just come to edit this code and then
    user will send /update_commands it will check if it send from admin,
    if yes it will update the commands.
    """

    # First it will check if this came from admins or not
    # if not then return, else update the commands using set_my_commands()
    if update.effective_user is None or update.message is None:
        return

    if update.effective_user.id == ADMIN_ID:

        msg_obj = await update.message.reply_text("⏳ Updating bot Commands...")

        try:
            cmd_status = await context.bot.set_my_commands(cmds_list)

        except Exception as e:
            cmd_status = None
            print(f"{e}")

        if not cmd_status:
            await msg_obj.edit_text("⛔ Somethign wrong here. Maybe too long cmds")

        else:
            await msg_obj.edit_text("✅ Commands have been updated successfully!")

    elif update.effective_user.id != ADMIN_ID:

        await update.message.reply_text("⛔ You are not authorized to update commands!")


async def show_bot_commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    For now only admins can see the information of all the commands.
    This function retrieves and displays the current bot commands using get_my_commands().
    i can trigger this function by sending /show_commands.
    """

    if update.effective_user is None or update.message is None:
        return

    if update.effective_user.id != ADMIN_ID:

        await update.message.reply_text(
            "⛔ You are not authorized to see All Commands!"
        )
        return

    commands = await context.bot.get_my_commands()

    if commands:
        commands_text = "\n".join(
            [f"/{cmd.command} - {cmd.description}" for cmd in commands]
        )
        response = f"📜 *Available Commands:*\n\n{commands_text}"
    else:
        response = "⚠️ No commands have been set for this bot."

    await update.message.reply_text(response)


async def rana_checking(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    This is for checking purpose only
    /rana
    """

    if update.message is None:
        print("just to warning remove of the below pylance")
        return

    text = f"Please send me a texts"

    await update.message.reply_text(text=text, do_quote=True)


async def get_logger_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    This is for my use when i want to get the logger file in tg directly
    This i have some extra plan to add some others featurs to get some text or
    Something like slicing features, but i dont plan till now.
    """
    msg = update.effective_message
    user = update.effective_user

    if msg is None or user is None:
        RanaLogger.info(
            "When request for logger file the msg and user need to present."
        )
        return None

    if user.id != ADMIN_ID:
        text = "❌ You are not authorized to access the log file."
        await msg.reply_html(text)
        return None

    file_path = Path() / LOG_FILE_NAME

    if not file_path.exists():
        await msg.reply_html("⚠️ Logger file does not exist.")
        return

    timestamp = msg.date.strftime("%Y%m%d_%H%M%S")
    filename = f"LoggerFile_{timestamp}_{LOG_FILE_NAME}"

    await msg.reply_document(
        document=file_path,
        filename=filename,
        caption=(
            "📝 Logger file as requested.\n"
            f"Below is when you requested for the database file.\n"
            f"Time: {timestamp}"
        ),
    )


async def get_database_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    This is for my use when I want to get the database file in TG directly.
    """
    msg = update.effective_message
    user = update.effective_user

    if msg is None or user is None:
        RanaLogger.info(
            "When request for database file the msg and user need to present."
        )
        return None

    if user.id != ADMIN_ID:
        text = "❌ You are not authorized to access the database file."
        await msg.reply_html(text)
        return None

    file_path = Path() / DATABASE_FILE_NAME

    if not file_path.exists():
        await msg.reply_html("⚠️ Database file does not exist.")
        return

    timestamp = msg.date.strftime("%Y%m%d_%H%M%S")

    filename = f"Database_File_{timestamp}_{DATABASE_FILE_NAME}"

    await msg.reply_document(
        document=file_path,
        filename=filename,
        caption=(
            f"🗃️ Database file as requested.\n\n\n"
            f"Below is when you requested for the database file.\n"
            f"Time: {timestamp}"
        ),
    )
