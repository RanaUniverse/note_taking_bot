from enum import Enum
from my_modules.some_inline_keyboards import keyboard_start_menu
from telegram import InlineKeyboardButton


class StartMenuButton(Enum):
    """
    Here i will keep the some normal buttons attached with mainly
    /start
    I will Keep the .value = tuple(Button Text, Callback Data, Description)
    And i will use the value later when i need from the tuple...

    """

    NEW_NOTE = ("➕ New Note", "new_note_making", "Create a new note")
    VIEW_NOTES = ("📄 View All Notes", "my_all_notes", "View all notes")
    EDIT_NOTE = ("✏️ Edit Note", "edit_note_prompt", "Edit an existing note")
    SEARCH_NOTE = ("🔍 Search Note", "search_note_prompt", "Search for a note")
    DELETE_NOTE = ("🗑️ Delete Note", "delete_note_prompt", "Delete a note")
    EXPORT_NOTES = ("📤 Export Notes", "export_notes", "Export all notes")
    SETTINGS = ("⚙️ Settings", "open_settings", "Open settings")
    HELP = ("❓ Help / FAQ", "show_help", "Show help information")
    FEEDBACK = ("💬 Feedback", "send_feedback", "Send feedback")

    def __init__(
        self,
        button_text: str,
        callback_data: str,
        description: str = "Blank Description",
    ):

        self.button_text = button_text
        self.callback_data = callback_data
        self.description = description


print(keyboard_start_menu)


button_rows = [
    [StartMenuButton.NEW_NOTE, StartMenuButton.VIEW_NOTES],
    [StartMenuButton.EDIT_NOTE, StartMenuButton.SEARCH_NOTE],
    [StartMenuButton.DELETE_NOTE, StartMenuButton.EXPORT_NOTES],
    [StartMenuButton.SETTINGS, StartMenuButton.HELP],
    [StartMenuButton.FEEDBACK],
]


def generate_start_menu_keyboard():
    """It will use iteratino to make the variable"""
    keyboard = [
        [
            InlineKeyboardButton(
                text=button.button_text, callback_data=button.callback_data
            )
            for button in row
        ]
        for row in button_rows
    ]
    return keyboard


print(generate_start_menu_keyboard())
