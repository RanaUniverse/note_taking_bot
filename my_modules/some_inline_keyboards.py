"""
Here will some buttons representing the keyboards
which i can import and use later
"""

from enum import Enum

from telegram import InlineKeyboardButton
from my_modules.inline_keyboards_enum_values import AccountButtons


demo_keyboard_options = [
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

demo_keyboard_options_aplhabet = [
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


keyboard_start_menu = [
    [
        InlineKeyboardButton(
            text="➕ New Note",
            callback_data="new_note_making",
        ),
        InlineKeyboardButton(
            text="📄 View All Notes",
            callback_data="my_all_notes",
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
            text=AccountButtons.ADD_EMAIL.button_text,
            callback_data=AccountButtons.ADD_EMAIL.callback_data,
        ),
        InlineKeyboardButton(
            text=AccountButtons.ADD_PHONE.button_text,
            callback_data=AccountButtons.ADD_PHONE.callback_data,
        ),
    ],
    [
        InlineKeyboardButton(
            text=AccountButtons.DELETE_ACCOUNT.button_text,
            callback_data=AccountButtons.DELETE_ACCOUNT.callback_data,
        ),
        InlineKeyboardButton(
            text=AccountButtons.UPGRADE_PRO.button_text,
            callback_data=AccountButtons.UPGRADE_PRO.callback_data,
        ),
    ],
]


keyboard_account_already_register = [
    [
        InlineKeyboardButton(
            text=AccountButtons.ADD_EMAIL.button_text,
            callback_data=AccountButtons.ADD_EMAIL.callback_data,
        ),
        InlineKeyboardButton(
            text=AccountButtons.ADD_PHONE.button_text,
            callback_data=AccountButtons.ADD_PHONE.callback_data,
        ),
    ],
    [
        InlineKeyboardButton(
            text=AccountButtons.ADD_TOKEN.button_text,
            callback_data=AccountButtons.ADD_TOKEN.callback_data,
        ),
        InlineKeyboardButton(
            text=AccountButtons.EDIT_ACCOUNT.button_text,
            callback_data=AccountButtons.EDIT_ACCOUNT.callback_data,
        ),
    ],
    [
        InlineKeyboardButton(
            text=AccountButtons.DELETE_ACCOUNT.button_text,
            callback_data=AccountButtons.DELETE_ACCOUNT.callback_data,
        ),
        InlineKeyboardButton(
            text=AccountButtons.UPGRADE_PRO.button_text,
            callback_data=AccountButtons.UPGRADE_PRO.callback_data,
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


# from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def new_note_make_successfull_buttons(note_id: str) -> list[list[InlineKeyboardButton]]:
    """When new note has been saved this buttons will shows there"""
    buttons = [
        [
            InlineKeyboardButton("View Note", callback_data=f"view_{note_id}"),
            InlineKeyboardButton("Export This", callback_data=f"export_{note_id}"),
        ],
        [
            InlineKeyboardButton("Delete Note", callback_data=f"delete_{note_id}"),
            InlineKeyboardButton("Share Note", callback_data=f"share_{note_id}"),
        ],
    ]
    return buttons


class MyInlineKeyboard(Enum):

    START_MENU = keyboard_start_menu
    OPTIONS = demo_keyboard_options
    ALPHABET = demo_keyboard_options_aplhabet
    ACCOUNT_NEW_REGISTER = keyboard_account_new_register
    ACCOUNT_ALREADY_REGISTER = keyboard_account_already_register
