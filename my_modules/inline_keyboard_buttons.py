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


# === Individual Buttons ===

# Note Related Buttons

NEW_NOTE_BUTTON = InlineKeyboardButton(
    text="✚ New Note",
    callback_data="new_note_making",
)

VIEW_ALL_NOTE_BUTTON = InlineKeyboardButton(
    text="🗒️ View All Notes",
    callback_data="my_all_notes",
)

EXPORT_ALL_NOTE_BUTTON = InlineKeyboardButton(
    text="📤 Export Your Notes",
    callback_data="export_all_notes",
)

FAKE_NOTE_MAKING_BUTTON = InlineKeyboardButton(
    text="🌀 Make A Fake Note",
    callback_data="make_fake_note",
)


# Account Related Buttons


ACCOUNT_DETAILS_BUTTON = InlineKeyboardButton(
    text="📊 View Account Details",
    callback_data="my_account_details",
)

UPGRADE_PRO_BUTTON = InlineKeyboardButton(
    text="💎 Upgrade to Pro Plan",
    callback_data="upgrade_to_pro_user",
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

DELETE_ACCOUNT_BUTTON = InlineKeyboardButton(
    text="❌ Delete Account",
    callback_data="delete_account",
)

# Misc some buttons


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


# Edit Note & its conversation related mainly


EDIT_TITLE_BUTTON = InlineKeyboardButton(
    text="📝 Edit Title",
    callback_data="edit_note_title",
)

EDIT_CONTENT_BUTTON = InlineKeyboardButton(
    text="📄 Edit Content",
    callback_data="edit_note_content",
)

DELETE_NOTE_BUTTON = InlineKeyboardButton(
    text="🗑️ Delete Note",
    callback_data="delete_the_note",
)

SAVE_CHANGES_BUTTON = InlineKeyboardButton(
    text="Save Current Change",
    callback_data="save_current_changes",
)

CANCEL_EDIT_NOTE_CONV_BUTTON = InlineKeyboardButton(
    text="🚫 Cancel Editing",
    callback_data="cancel_edit_note_conv",
)


# Below is some buttons related to notes

DELETE_ALL_NOTE_BUTTON = InlineKeyboardButton(
    text="🗑️ Delete My All Notes",
    callback_data="delete_my_all_notes",
)

# currently this delete button is not in use i am using normal str value.
DELETE_ONE_NOTE_DYNAMIC_BUTTON = InlineKeyboardButton(
    text="Delete This Note",
    callback_data="delete_note_",
)

VIEW_ONE_NOTE_DYNAMIC_BUTTON = InlineKeyboardButton(
    text="View This Note",
    callback_data="view_note_",
)


CANCEL_NOTE_DELETE_BUTTON = InlineKeyboardButton(
    text="Note Deletion Cancel 🚫",
    callback_data="note_delete_cancel",
)

# === Keyboard Layouts Below ===


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
    [SAVE_CHANGES_BUTTON],
    [CANCEL_EDIT_NOTE_CONV_BUTTON],
]


USER_NEW_REGISTER_KEYBOARD = [
    [NEW_NOTE_BUTTON],
    [UPGRADE_PRO_BUTTON],
    [DELETE_ACCOUNT_BUTTON],
]


USER_ALREADY_REGISTER_KEYBOARD = [
    [NEW_NOTE_BUTTON],
    [ACCOUNT_DETAILS_BUTTON],
    [ADD_EMAIL_BUTTON],
    [ADD_PHONE_NO_BUTTON],
    [ADD_REFERREL_BUTTON],
    [UPGRADE_PRO_BUTTON],
    [SETTINGS_BUTTON, HELP_BUTTON],
]


USER_HAS_NO_NOTE_KEYBOARD = [
    [NEW_NOTE_BUTTON],
    [FAKE_NOTE_MAKING_BUTTON],
    [HELP_BUTTON],
]


# Below are some keyboard buttons related to delete note command like this


# when /del_note come it will just a demo keyboard to shows
NOTE_DELETE_KEYBOARD = [
    [VIEW_ALL_NOTE_BUTTON],
    [DELETE_ALL_NOTE_BUTTON],
    [HELP_BUTTON],
]


# Below are somes functions which generate the buttons in a fun as
# i need some dynamic content in the callback data


def generate_buttons_with_note_view(note_id: str) -> list[list[InlineKeyboardButton]]:
    """
    When user is viewing a note, i want these buttons will be
    there present for some simple things.
    """

    buttons = [
        [
            InlineKeyboardButton(
                text="✏️ Edit Note 🟩",
                callback_data=f"edit_note_{note_id}",
            ),
            InlineKeyboardButton(
                text="🗑️ Delete Note 🟥",
                callback_data=f"delete_note_{note_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔗 Share Note 📤",
                callback_data=f"share_note_{note_id}",
            ),
            InlineKeyboardButton(
                text="📋 Duplicate Note 🧬",
                callback_data=f"duplicate_note_{note_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="📄 Export as TXT 🗒️",
                callback_data=f"export_note_txt_{note_id}",
            ),
            InlineKeyboardButton(
                text="📤 Export as PDF 🧾",
                callback_data=f"export_note_pdf_{note_id}",
            ),
        ],
    ]
    return buttons


# Below is one more buttons keyboard which will be there when shows confirmation to del note


def generate_delete_note_confirmation_buttons(
    note_id: str,
) -> list[list[InlineKeyboardButton]]:

    confirmation_buttons = [
        [
            InlineKeyboardButton(
                text="✅ Yes, Delete This Note",
                callback_data=f"note_del_confirm_{note_id}",
            )
        ],
        [CANCEL_NOTE_DELETE_BUTTON],
    ]
    return confirmation_buttons


# Below is a example of how to make the inline buttons

demo_buttons = [
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


if __name__ == "__main__":

    print("Below is The example of how the buttons to use.")
    print(demo_buttons)

    """
    
    from telegram import Message

    msg = Message()

    text = "This is the Text Attaching with the Message Send by Bot"

    await msg.reply_html(
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons),
    )

    """
