"""
Here will some buttons representing the keyboards
which i can import and use later
"""

from enum import Enum

from telegram import InlineKeyboardButton


keyboard_options = [
    [
        InlineKeyboardButton(text="Option 1", callback_data="1"),
        InlineKeyboardButton(text="Option 2", callback_data="2"),
    ],
    [
        InlineKeyboardButton(text="Option 3", callback_data="3"),
        InlineKeyboardButton(text="Option 4", callback_data="4"),
        InlineKeyboardButton(text="Option 5", callback_data="5"),
    ],
]

keyboard_options_aplhabet = [
    [
        InlineKeyboardButton(text="Button A", callback_data="A1"),
        InlineKeyboardButton(text="Button B", callback_data="B2"),
        InlineKeyboardButton(text="Button C", callback_data="C3"),
    ],
    [
        InlineKeyboardButton(text="Button D", callback_data="D4"),
        InlineKeyboardButton(text="Button E", callback_data="E5"),
    ],
]


# Below will use with the /start get by user. This need to call with appropriat callback
# but till now i dont make it.
# For Now dont change the button and its callback query data
# ✅ ❌ first which are made and second which i need to made yet

from telegram import InlineKeyboardButton

keyboard_start_menu = [
    [
        InlineKeyboardButton(
            text="➕ New Note",
            callback_data="new_note_making",
        ),
        InlineKeyboardButton(
            text="📄 View All Notes",
            callback_data="my_notes_view",
        ),
    ],
    [
        InlineKeyboardButton(
            text="✏️ Edit Note",
            callback_data="edit_note_prompt",
        ),
        InlineKeyboardButton(
            text="🔍 Search Note",
            callback_data="search_note_prompt",
        ),
    ],
    [
        InlineKeyboardButton(
            text="🗑️ Delete Note",
            callback_data="delete_note_prompt",
        ),
        InlineKeyboardButton(
            text="📤 Export Notes",
            callback_data="export_notes",
        ),
    ],
    [
        InlineKeyboardButton(
            text="⚙️ Settings",
            callback_data="open_settings",
        ),
        InlineKeyboardButton(
            text="❓ Help / FAQ",
            callback_data="show_help",
        ),
    ],
    [
        InlineKeyboardButton(
            text="💬 Feedback",
            callback_data="send_feedback",
        ),
    ],
]


keyboard_account_new_register = [
    [
        InlineKeyboardButton(
            text="📧Add Email ID",
            callback_data="add_email",
        ),
        InlineKeyboardButton(
            text="📱Add Phone No",
            callback_data="add_phone",
        ),
    ],
    [
        InlineKeyboardButton(
            text="🎟Add Referral Code",
            callback_data="add_referral",
        ),
        InlineKeyboardButton(
            text="My Account Details",
            callback_data="account_details",
        ),
    ],
    [
        InlineKeyboardButton(
            text="❌Terminate Now",
            callback_data="register_terminate",
        ),
        InlineKeyboardButton(
            text="✅Confirm & Save",
            callback_data="register_save_now",
        ),
    ],
]


keyboard_user_info = [
    [
        InlineKeyboardButton(
            text="✅ Activate My Account",
            callback_data="activate_account",
        ),
        InlineKeyboardButton(
            text="⚙️ Edit My Account",
            callback_data="edit_account",
        ),
    ],
    [
        InlineKeyboardButton(
            text="❌ Delete Account",
            callback_data="delete_account",
        ),
        InlineKeyboardButton(
            text="🔒 Change Password",
            callback_data="change_password",
        ),
    ],
    [
        InlineKeyboardButton(
            text="📊 View Account Details",
            callback_data="view_account",
        ),
        InlineKeyboardButton(
            text="📜 View Account History",
            callback_data="account_history",
        ),
    ],
    [
        InlineKeyboardButton(
            text="🚪 Logout",
            callback_data="logout",
        ),
    ],
]


keyboard_account_already_register = [
    [
        InlineKeyboardButton(
            text="Add Some Token",
            callback_data="add_some_token",
        ),
        InlineKeyboardButton(
            text="✏️ Edit My Profile",
            callback_data="edit_profile",
        ),
    ],
    [
        InlineKeyboardButton(
            text="🗑️ Delete My Account",
            callback_data="delete_account",
        ),
        InlineKeyboardButton(
            text="💎 Upgrade to Pro Plan",
            callback_data="upgrade_pro",
        ),
    ],
    [
        InlineKeyboardButton(
            text="📂 View My Data",
            callback_data="view_my_data",
        ),
        InlineKeyboardButton(
            text="🔄 Sync & Backup",
            callback_data="sync_backup",
        ),
    ],
]


class MyInlineKeyboard(Enum):

    START_MENU = keyboard_start_menu
    OPTIONS = keyboard_options
    ALPHABET = keyboard_options_aplhabet
    ACCOUNT_REGISTER = keyboard_account_new_register
    ACCOUNT_NEW_REGISTER = keyboard_account_new_register
    ACCOUNT_ALREADY_REGISTER = keyboard_account_already_register
