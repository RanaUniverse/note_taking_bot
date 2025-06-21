"""
The Buttons which comes in the
Text Typing Keyboard's Place Which works like sending the
predefined text to user back.

So For this i want to make some buttons & keyboards
Which i can use goodly by import from these below.
"""

from telegram import KeyboardButton

YES_NO_REPLY_KEYBOARD = [
    [
        KeyboardButton(text="Yes"),
        KeyboardButton(text="No"),
    ],
    [
        KeyboardButton(text="/cancel"),
    ],
    # [
    #     KeyboardButton(text="Save As Draft"),
    # ],
]
