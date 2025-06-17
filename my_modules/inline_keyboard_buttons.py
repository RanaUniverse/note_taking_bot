"""
Buttons Having Callback Data
Here i will keep some Buttons Defind with some Callback Data
Then i will use this buttons values in the others ReplyKeyboardMarkup
And i will need to use this module goodly to generate the buttons.
"""

from telegram import (
    InlineKeyboardButton,
    # InlineKeyboardMarkup,
)


NEW_NOTE_BUTTON = InlineKeyboardButton(
    text="✚ New Note",
    callback_data="new_note_making",
)

VIEW_ALL_NOTE_BUTTON = InlineKeyboardButton(
    text="🗒️ View All Notes",
    callback_data="my_all_notes",
)


ACCOUNT_DETAILS_BUTTON = InlineKeyboardButton(
    text="📊 View Account Details",
    callback_data="account_details",
)


UPGRADE_PRO_BUTTON = InlineKeyboardButton(
    text="💎 Upgrade to Pro Plan",
    callback_data="upgrade_pro",
)

EXPORT_ALL_NOTE_BUTTON = InlineKeyboardButton(
    text="Export Your Notes",
    callback_data="export_all_notes",
)

ADD_EMAIL_BUTTON = InlineKeyboardButton(
    text="📧 Add Email ID",
    callback_data="add_email",
)

ADD_PHONE_NO_BUTTON = InlineKeyboardButton(
    text="📱 Add Phone No",
    callback_data="add_phone_no",
)

ADD_REFERREL_BUTTON = InlineKeyboardButton(
    text="🎟 Add Referral Code",
    callback_data="add_referral",
)

SETTINGS_BUTTON = InlineKeyboardButton(
    text="⚙️ Settings",
    callback_data="open_settings",
)

FEEDBACK_BUTTON = InlineKeyboardButton(
    text="💬 Feedback",
    callback_data="send_feedback",
)

HELP_BUTTON = InlineKeyboardButton(
    text="Need Help ?",
    callback_data="need_help",
)

CANCEL_EDIT_NOTE_CONV_BUTTON = InlineKeyboardButton(
    text="❌ Cancel Edit Note Now",
    callback_data="cancel_edit_note_conv",
)


EDIT_TITLE_BUTTON = InlineKeyboardButton(
    text="Edit The Title",
    callback_data="edit_note_title",
)

EDIT_CONTENT_BUTTON = InlineKeyboardButton(
    text="Edit Main Content",
    callback_data="edit_note_content",
)

DELETE_NOTE_BUTTON = InlineKeyboardButton(
    text="Delete This Note",
    callback_data="delete_the_note",
)


# Below are some Varialbe for constant keyboards

START_SIMPLE_KEYBOARD = [
    [NEW_NOTE_BUTTON, VIEW_ALL_NOTE_BUTTON],
    [ACCOUNT_DETAILS_BUTTON],
    [UPGRADE_PRO_BUTTON],
    [SETTINGS_BUTTON, FEEDBACK_BUTTON],
]


EDIT_NOTE_KEYBOARD = [
    [VIEW_ALL_NOTE_BUTTON],
    [NEW_NOTE_BUTTON],
    [HELP_BUTTON],
    [CANCEL_EDIT_NOTE_CONV_BUTTON],
]


EDIT_NOTE_CONV_KEYBOARD = [
    [EDIT_TITLE_BUTTON],
    [EDIT_CONTENT_BUTTON],
    [DELETE_NOTE_BUTTON],
    [CANCEL_EDIT_NOTE_CONV_BUTTON],
]

if __name__ == "__main__":

    print("Below is The example of how the buttons to use.")

    buttons = [
        [
            InlineKeyboardButton(
                text="Find From All Notes To Edit ✅",
                callback_data="my_all_notes",
            ),
            InlineKeyboardButton(
                text="New Note Make Now ✅",
                callback_data="new_note",
            ),
        ],
        [
            InlineKeyboardButton(
                text="Need Help",
                callback_data="customer_care",
            ),
            InlineKeyboardButton(
                text="Cancel Now ✅",
                callback_data="cancel_conv",
            ),
        ],
    ]

    """
    
    from telegram import Message

    msg = Message()

    text = "This is the Text Attaching with the Message Send by Bot"

    await msg.reply_html(
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons),
    )

    """
