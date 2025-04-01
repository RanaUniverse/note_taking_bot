"""
Here i will keep some commands which i can use in
set_my_commands()
"""

import os
from telegram import Update
from telegram import BotCommand
from telegram.ext import ContextTypes


ADMIN_ID_STR = os.environ.get("ADMIN_ID", None)

if not ADMIN_ID_STR:
    raise ValueError("❌ ADMIN_ID not found in .env file!")

try:
    ADMIN_ID = int(ADMIN_ID_STR)  # Convert to int

except ValueError:
    raise ValueError("❌ ADMIN_ID must be a valid integer!")


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
        command="register",
        description="📝 Register yourself in the bot",
    ),
    BotCommand(
        command="update_commands",
        description="Changes All The commands of this bot",
    ),
    BotCommand(
        command="new_note",
        description="Make a new note and store it.",
    ),
]


async def update_commands_cmd(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
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
    This function retrieves and displays the current bot commands using get_my_commands().
    i can trigger this function by sending /show_commands.
    """

    if update.effective_user is None or update.message is None:
        return

    if update.effective_user.id != ADMIN_ID:

        await update.message.reply_text("⛔ You are not authorized to see commands!")
        return

    commands = await context.bot.get_my_commands()

    print(commands)
    print(type(commands))

    if commands:
        commands_text = "\n".join(
            [f"/{cmd.command} - {cmd.description}" for cmd in commands]
        )
        response = f"📜 *Available Commands:*\n\n{commands_text}"
    else:
        response = "⚠️ No commands have been set for this bot."

    await update.message.reply_text(response)
