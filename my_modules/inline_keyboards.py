from enum import Enum
from telegram import InlineKeyboardButton


class MyInlineButtons(Enum):
    """
    Here i will keep some buttons and its values,
    And Then i will use some of the instance value to make some related values.

    I will Keep the .value = tuple(Button Text, Callback Data, Description)
    And i will use the value later when i need from the tuple.

    Later for different type of button i will call the needed Members
    And make some variables of 'list[list[InlineKeyboardButton]]'
    """

    NEW_NOTE = ("➕ New Note", "new_note_making", "Create a new note")
    EDIT_NOTE = ("✏️ Edit Note", "edit_note_prompt", "Edit an existing note")
    VIEW_NOTES = ("📄 View All Notes", "my_notes_view", "View all notes")
    SEARCH_NOTE = ("🔍 Search Note", "search_note_prompt", "Search for a note")
    DELETE_NOTE = ("🗑️ Delete Note", "delete_note_prompt", "Delete a note")
    EXPORT_NOTES = ("📤 Export Notes", "export_notes", "Export all notes")
    SETTINGS = ("⚙️ Settings", "open_settings", "Open settings")
    HELP = ("❓ Help / FAQ", "show_help", "Show help information")
    FEEDBACK = ("💬 Feedback", "send_feedback", "Send feedback")

    ADD_EMAIL = ("📧 Add Email ID", "add_email", "Add your email address")
    ADD_PHONE = ("📱 Add Phone No", "add_phone", "Add your phone number")
    ADD_REFERRAL = ("🎟 Add Referral Code", "add_referral", "Enter a referral code")

    # Account management buttons
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

    def __init__(
        self,
        button_text: str,
        callback_data: str,
        description: str = "Blank Description",
    ):

        self.button_text = button_text
        self.callback_data = callback_data
        self.description = description


start_button = [
    [
        InlineKeyboardButton(
            text=MyInlineButtons.NEW_NOTE.button_text,
            callback_data=MyInlineButtons.NEW_NOTE.callback_data,
        ),
        InlineKeyboardButton(
            text=MyInlineButtons.VIEW_NOTES.button_text,
            callback_data=MyInlineButtons.VIEW_NOTES.callback_data,
        ),
    ],
    [
        InlineKeyboardButton(
            text=MyInlineButtons.EDIT_NOTE.button_text,
            callback_data=MyInlineButtons.EDIT_NOTE.callback_data,
        ),
        InlineKeyboardButton(
            text=MyInlineButtons.SEARCH_NOTE.button_text,
            callback_data=MyInlineButtons.SEARCH_NOTE.callback_data,
        ),
    ],
    [
        InlineKeyboardButton(
            text=MyInlineButtons.DELETE_NOTE.button_text,
            callback_data=MyInlineButtons.DELETE_NOTE.callback_data,
        ),
        InlineKeyboardButton(
            text=MyInlineButtons.EXPORT_NOTES.button_text,
            callback_data=MyInlineButtons.EXPORT_NOTES.callback_data,
        ),
    ],
    [
        InlineKeyboardButton(
            text=MyInlineButtons.SETTINGS.button_text,
            callback_data=MyInlineButtons.SETTINGS.callback_data,
        ),
        InlineKeyboardButton(
            text=MyInlineButtons.HELP.button_text,
            callback_data=MyInlineButtons.HELP.callback_data,
        ),
    ],
    [
        InlineKeyboardButton(
            text=MyInlineButtons.FEEDBACK.button_text,
            callback_data=MyInlineButtons.FEEDBACK.callback_data,
        ),
    ],
]
