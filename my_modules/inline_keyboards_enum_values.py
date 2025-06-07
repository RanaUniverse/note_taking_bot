"""
In this module i will keep some code which will same as
some inline keyboards.
This value will be the callback data.
"""

from enum import Enum
from telegram import InlineKeyboardButton


class ThreeValues:
    """
    This is for just a 3 values tuple from where i can get
    the value i want to use in the enum instances.
    I will use this class as init only.
    """

    def __init__(
        self,
        button_text: str,
        callback_data: str,
        description: str = "No description provided",
    ):
        self.button_text = button_text
        self.callback_data = callback_data
        self.description = description

    def to_inline_button(self) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=self.button_text,
            callback_data=self.callback_data,
        )


# 👤 Buttons For user accoutn
class AccountButtons(ThreeValues, Enum):

    ADD_EMAIL = ("📧 Add Email ID", "add_email", "Add your email address")
    ADD_PHONE = ("📱 Add Phone No", "add_phone", "Add your phone number")
    ADD_REFERRAL = ("🎟 Add Referral Code", "add_referral", "Enter a referral code")
    ADD_TOKEN = ("Add Token ⭐", "add_tokens", "Add Some token later")
    ACTIVATE_ACCOUNT = (
        "✅ Activate My Account",
        "activate_account",
        "Activate your account",
    )
    EDIT_ACCOUNT = ("⚙️ Edit My Account", "edit_account", "Edit your account settings")
    DELETE_ACCOUNT = (
        "❌ Delete Account",
        "delete_account",
        "Delete your account permanently",
    )
    CHANGE_PASSWORD = (
        "🔒 Change Password",
        "change_password",
        "Update your account password",
    )
    VIEW_ACCOUNT_DETAILS = (
        "📊 View Account Details",
        "view_account",
        "See your account information",
    )
    ACCOUNT_HISTORY = (
        "📜 View Account History",
        "account_history",
        "See your activity history",
    )
    LOGOUT = ("🚪 Logout", "logout", "Logout from your account")
    UPGRADE_PRO = (
        "💎 Upgrade to Pro Plan",
        "upgrade_pro",
        "Upgrade your account to the Pro Plan",
    )


# ⚙️ Some Extra Buttons need
class MiscButtons(ThreeValues, Enum):

    SETTINGS = ("⚙️ Settings", "open_settings", "Open settings")
    HELP = ("❓ Help / FAQ", "show_help", "Show help information")
    FEEDBACK = ("💬 Feedback", "send_feedback", "Send feedback")


# 📝 Note Making and so on related to Notes
class NoteButtons(ThreeValues, Enum):

    NEW_NOTE = ("✚ New Note", "new_note_making", "Create a new note")
    EDIT_NOTE = ("✏️ Edit Note", "edit_note_prompt", "Edit an existing note")
    VIEW_NOTES = ("📄 View All Notes", "my_all_notes", "View all notes")
    SEARCH_NOTE = ("🔍 Search Note", "search_note_prompt", "Search for a note")
    DELETE_NOTE = ("🗑️ Delete Note", "delete_note_prompt", "Delete a note")
    EXPORT_NOTES = ("📤 Export Notes", "export_notes", "Export all notes")


start_cmd_button = [
    [
        InlineKeyboardButton(
            text=NoteButtons.NEW_NOTE.button_text,
            callback_data=NoteButtons.NEW_NOTE.callback_data,
        ),
        InlineKeyboardButton(
            text=NoteButtons.VIEW_NOTES.button_text,
            callback_data=NoteButtons.VIEW_NOTES.callback_data,
        ),
    ],
    [
        InlineKeyboardButton(
            text=NoteButtons.EDIT_NOTE.button_text,
            callback_data=NoteButtons.EDIT_NOTE.callback_data,
        ),
        InlineKeyboardButton(
            text=NoteButtons.SEARCH_NOTE.button_text,
            callback_data=NoteButtons.SEARCH_NOTE.callback_data,
        ),
    ],
    [
        InlineKeyboardButton(
            text=NoteButtons.DELETE_NOTE.button_text,
            callback_data=NoteButtons.DELETE_NOTE.callback_data,
        ),
        InlineKeyboardButton(
            text=NoteButtons.EXPORT_NOTES.button_text,
            callback_data=NoteButtons.EXPORT_NOTES.callback_data,
        ),
    ],
    [
        InlineKeyboardButton(
            text=AccountButtons.UPGRADE_PRO.button_text,
            callback_data=AccountButtons.UPGRADE_PRO.callback_data,
        )
    ],
    [
        InlineKeyboardButton(
            text=AccountButtons.VIEW_ACCOUNT_DETAILS.button_text,
            callback_data=AccountButtons.VIEW_ACCOUNT_DETAILS.callback_data,
        ),
        InlineKeyboardButton(
            text=AccountButtons.EDIT_ACCOUNT.button_text,
            callback_data=AccountButtons.EDIT_ACCOUNT.callback_data,
        ),
    ],
    [
        InlineKeyboardButton(
            text=MiscButtons.SETTINGS.button_text,
            callback_data=MiscButtons.SETTINGS.callback_data,
        ),
        InlineKeyboardButton(
            text=MiscButtons.HELP.button_text,
            callback_data=MiscButtons.HELP.callback_data,
        ),
    ],
]


def main():
    print("Rana Universe")

    a = MiscButtons.SETTINGS.description
    print(a)


if __name__ == "__main__":
    main()
