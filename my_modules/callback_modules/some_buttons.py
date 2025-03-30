"""
some buttons will be separated in this file
i will kept them for easy editable and easy to separate the logics
"""

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


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
        f"/register"
    )

    if query.data == "update_profile":
        # await query.answer(
        #     text="⚠️ You are going to edit your profile.🚧",
        #     show_alert=True,
        # )
        await query.edit_message_text(
            text= text,
            parse_mode=ParseMode.HTML,
        )
