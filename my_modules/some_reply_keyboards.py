"""
here will some code of buttons which are in reply keyboards
these keyboard are in the text where we use keyboard

"""

from telegram import KeyboardButton

yes_no_reply_keyboard = [
    [
        KeyboardButton(text="Yes"),
        KeyboardButton(text="No"),
    ],
    [
        KeyboardButton(text="/cancel"),
    ],
]
