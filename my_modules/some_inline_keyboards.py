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
        InlineKeyboardButton(text="📧Add Email ID", callback_data="email"),
        InlineKeyboardButton(text="📱Add Phone No", callback_data="phone"),
    ],
    [
        InlineKeyboardButton(text="🎟Add Referral Code", callback_data="referral"),
    ],
    [
        InlineKeyboardButton(text="❌Terminate Now", callback_data="terminate"),
        InlineKeyboardButton(text="✅Confirm & Save", callback_data="save_now"),
    ],
]
