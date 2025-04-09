"""
this module will contains the code for delete a note
i not think fully should i will delete the notes or i will keep those and mark as delete

"""

from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from telegram.constants import ChatAction

from telegram.ext import ContextTypes

from my_modules.logger_related import RanaLogger

from my_modules.database_code.database_make import engine

# from my_modules.database_code.models_table import NotePart
from my_modules.database_code import db_functions


async def delete_note_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    When user will send /delete_note without any args it will execute
    and it will say user to pass the correct note id and how to use.
    """

    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None:
        RanaLogger.warning(
            "User and MSG should be present when user send "
            "/delete_note without any args"
        )
        return None

    print(context.args)

    if not context.args:
        keyboard = [
            [
                InlineKeyboardButton("View All Notes", callback_data="view_notes"),
                InlineKeyboardButton("Help", callback_data="help"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await msg.reply_text(
            "Please provide the ID of the note you wish to delete. "
            "Or You can go and search in ur note and then view and then delete.",
            reply_markup=reply_markup,
        )
    else:
        RanaLogger.warning("This should not execute as i will use args value to 0")


async def delete_note_one_args(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    When user will send /delete_note without any args it will execute
    and it will say user to pass the correct note id and how to use.
    """

    user = update.effective_user
    msg = update.effective_message

    if user is None or msg is None:
        RanaLogger.warning(
            "User and MSG should be present when user send "
            "/delete_note with one any args"
        )
        return None

    await msg.reply_chat_action(action=ChatAction.TYPING)

    if not context.args:
        # This part should not execute as this is must have 1 args
        text = (
            "Please provide the ID of the note you wish to delete.\n"
            "Usage: /delete_note <note_id>"
        )
        await msg.reply_html(text=text)
        return None

    note_id = context.args[0]
    RanaLogger.warning(f"{user.full_name} want to delete the note id of: {note_id}")

    note_row = db_functions.note_obj_from_note_id(
        engine=engine,
        note_id=note_id,
    )

    if note_row is None:
        text = (
            f"YOu Have Send me note id as <code>{note_id}</code>.\n\n"
            f"This Id is not valid, Please Provide Correct Note Id, You can find old chat "
            f"Or You can go to export ur data, else search note, and finally contact admin."
            f" /help and describe this"
        )
        await msg.reply_html(text=text)
        return

    # Below Means Note row is present
    owner_id = note_row.user_id

    if user.id != owner_id:
        text = f"You are not the owner, you can't remove this note,"
        await msg.reply_html(text)
        return

    deletion_confirmation = db_functions.delete_note_obj(
        engine=engine,
        note_id=note_id,
        user_id=owner_id,
    )

    if deletion_confirmation:
        text = f"This Note has been deleted forever 🥹"
        await msg.reply_html(text)
        return

    else:
        print(f"I wish This should not happens.")
        RanaLogger.warning(f"I wish This should not happens.")
        text = f"Note Deleted got failed for any reason pls /help"
        await msg.reply_html(text)
        return
