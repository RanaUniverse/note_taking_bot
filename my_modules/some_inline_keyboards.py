"""
Here will some buttons representing the keyboards
which i can import and use later
"""

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


keyboard_account_register = [
    [
        InlineKeyboardButton(
            text="📧Add Email ID",
            callback_data="email",
        ),
        InlineKeyboardButton(
            text="📱Add Phone No",
            callback_data="phone",
        ),
    ],
    [
        InlineKeyboardButton(
            text="🎟Add Referral Code",
            callback_data="referral",
        ),
    ],
    [
        InlineKeyboardButton(
            text="❌Terminate Now",
            callback_data="terminate",
        ),
        InlineKeyboardButton(
            text="✅Confirm & Save",
            callback_data="save_now",
        ),
    ],
]


keyboard_start_menu = [
    [
        InlineKeyboardButton(
            text="📝 New Note",
            callback_data="new_note",
        ),
        InlineKeyboardButton(
            text="✏️ Edit Old Note",
            callback_data="edit_note",
        ),
    ],
    [
        InlineKeyboardButton(
            text="❌ Delete Note",
            callback_data="delete_note",
        ),
        InlineKeyboardButton(
            text="🔍 Search Notes",
            callback_data="search_note",
        ),
    ],
    [
        InlineKeyboardButton(
            text="⚙️ Edit My Details",
            callback_data="edit_details",
        ),
        InlineKeyboardButton(
            text="📂 View All Notes",
            callback_data="view_notes",
        ),
    ],
    [
        InlineKeyboardButton(
            text="📤 Export Notes",
            callback_data="export_notes",
        ),
        InlineKeyboardButton(
            text="❓ Help Section",
            callback_data="help_section",
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


from enum import Enum


class MyInlineKeyboard(Enum):

    OPTIONS = keyboard_options
    ALPHABET = keyboard_options_aplhabet
    ACCOUNT_REGISTER = keyboard_account_register
    START_MENU = keyboard_start_menu
