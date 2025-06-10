"""
Here i will make some funcions which will return some demo
Text which i can reuse in different places.
"""

from telegram import Chat, User

from my_modules import bot_config_settings
from my_modules.database_code.models_table import NotePart


MAX_TITLE_LEN = bot_config_settings.MAX_TITLE_LEN
MAX_CONTENT_LEN = bot_config_settings.MAX_CONTENT_LEN


def start_text_for_private(user: User) -> str:
    """
    When user will send /start in private chate this will trigger
    """

    text = (
        f"👋 Hello, {user.mention_html()}! "
        f"Welcome to <b><u>The Note-Taking Bot</u></b> 📝🤖\n\n"
        f"Use the buttons below to manage your notes, or use commands if needed! 🔒🗂️\n\n"
        f"<b>🔹 Available Commands:</b>\n"
        f"📝 /new_note - Create a new note(use button)\n"
        f"📂 /view_notes - View all your notes\n"
        f"✏️ /edit_note - Edit an existing note\n"
        f"🔍 /search_note - Search notes by title\n"
        f"❌ /delete_note - Delete a note\n"
        f"📤 /export_notes - Export all notes\n"
        f"⚙️ /update_profile - Update your profile\n"
        f"❓ /help - Get help and usage instructions\n\n"
        f"⚠️ <b>Note:</b> If buttons don't work, use the above commands manually."
        f"⚠️ <b>WARNING:</b> The buttons below are still in development. "
        f"Please use the commands above for now. 🚧🔄"
    )

    return text


def start_text_for_group(chat_obj: Chat) -> str:
    """
    When user will send /start in group the text message will come from here
    """

    chat_type = chat_obj.type  # e.g., "group", "supergroup"
    chat_name = chat_obj.title or chat_obj.full_name or "this group"

    text = (
        f"📢 <b>Hello {chat_name}!</b>\n\n"
        f"🧠 This bot is currently <b>not operational in group chats</b> like this one "
        f"({chat_type}).\n\n"
        "🔧 <b>Why?</b>\n"
        "Group note-taking features have not been implemented yet.\n"
        "They're being built and will be included in a future update. 🚧\n\n"
        "💡 In the meantime, you can still use this bot in a private chat.\n"
        "Tap the button below or message me directly to get started.\n\n"
        "🙏 Thanks for your patience!"
    )

    return text


def deeplink_simple_group_start_text(group_id: int | str) -> str:
    """
    This is just a basic deeplink message reply, this time when
    i need to say user based on the deeplink value this is the demo text
    """

    text = (
        f"👋 You came from a group: <code>{group_id}</code>\n\n"
        "Thanks for starting the bot from the group chat! 🙌\n\n"
        "Currently, this bot works only in private messages. "
        "Please continue using it here for now. "
        "Group support will be added in a future update. 🚧\n\n"
        "If you used a deep link like <code>/start</code>, that's totally fine "
        "— just follow the instructions below. 👇"
    )

    return text


def help_cmd_text() -> str:
    """
    When /help will come normal string it will send
    """
    help_text = (
        "🤖 <b>Welcome to the Bot Help Guide</b>\n\n"
        "Hello there! 👋\n"
        "I'm here to assist you with various commands and features.\n\n"
        "<b>📌 Available Commands:</b>\n\n"
        "• <b>/start</b>\n"
        "  └─ Start a new conversation with the bot. Useful if you’re here for the first time!\n\n"
        "• <b>/contact</b>\n"
        "  └─ Need assistance? Use this to get in touch with the administrator directly.\n\n"
        "<b>💡 Tips:</b>\n"
        "• Try typing commands in the chat to explore more features.\n"
        "• You can interact with buttons (if available) for quicker access.\n\n"
        "📢 <i>More commands and features coming soon. Stay connected!</i>\n\n"
        "<b>Thank you for using the bot 💙</b>"
    )
    return help_text


def help_cmd_from_group_text(group_link: str) -> str:
    """
    It will take the group link and just say a normal help message
    just not special just to say only
    """
    text = (
        "⚠️ <b>This bot is not available for use in group chats.</b>\n\n"
        "To access all features and interact with the bot, "
        "please send commands in a <b>private chat</b>.\n\n"
        "💬 For community discussions or support, feel free to "
        "join our official group:\n"
        f"👉 <a href='https://t.me/{group_link}'>Join the Main Group</a>\n\n"
        "Thank you for understanding!"
    )
    return text


def prompt_user_to_register(user: User) -> str:
    """
    When user is not register
    it will say user to register and then user this bot
    """
    text = (
        f"Hi <b>{user.mention_html()}</b>! 👋\n\n"
        f"It looks like you're not registered yet 😢\n"
        f"To get started, please send the /register_me command.\n"
        f"Once you're registered, you can come back and use this bot.\n\n"
        f"If you need help, feel free to reach out using /help. 💬"
    )

    return text


def user_has_no_valid_points(user: User) -> str:
    """
    When user has 0 points, it means it will say user
    to buy new points.
    """
    text_no_point = (
        f"🚫 <b>Oops!</b> You've run out of points 😢🪄\n\n"
        f"But don't worry — you can easily top up! Just use the command:\n"
        f"<blockquote><code>/add_points 20</code></blockquote>\n"
        f"(Here, 20 is an example — choose your own number 🧮)\n\n"
        f"💡 Once you've added some points, you'll be all set to create notes again!"
    )

    return text_no_point


def title_length_exceed_warning_text():
    text = (
        f"⚠️ <b>Title Too Long!</b>\n\n"
        f"Please keep your title within <b>{MAX_TITLE_LEN} characters</b>. 📝\n"
        f"Let's try again — send a shorter, clear title for your note below 👇"
    )
    return text


def content_length_exceed_warning_text():
    text = (
        f"⚠️ <b>Note Content Too Long!</b>\n\n"
        f"Please keep your note within <b>{MAX_CONTENT_LEN} characters</b>. 📏\n"
        f"Let's try again — send a shorter version of your note content below 👇"
    )
    return text


def new_note_title_ask(user: User, user_points: int) -> str:
    """
    Returns the message to show when the user is about to create a new note.
    """
    ask_for_title = (
        f"👋 Hello {user.mention_html()}!\n\n"
        f"You currently have <b>{user_points} Tokens</b> 💰🎉\n"
        f"📝 <i>Creating a note costs</i> <b>1 Token</b> ⚠️\n\n"
        f"If you want to cancel, you can send /cancel anytime. ❌\n\n"
        f"<b>🚀 Step 1:</b> Please send the <u><b>Title of your Note</b></u> below 👇👇👇"
    )

    return ask_for_title


def new_note_content_ask() -> str:
    """
    After user will save the title it will ask for content
    And it is the reply message which says to send for content
    """

    text = (
        f"✅ <b>Awesome!</b> I've saved your note title successfully. 🎯\n\n"
        f"📜 <b>Step 2:</b> Now, please send the <u><b>content of your note</b></u> 📝\n\n"
        f"💡 <i>Tip:</i> You can write as much as you want — I'll save the full message as your note content. ✍️"
    )

    return text


def new_note_save_ask() -> str:
    """
    After user send title and content
    A message will ask if he want to save this note in db or not.
    """
    ask_for_save = (
        f"✅ <b>Great!</b> Your <b>note title</b> has been saved. 🎯\n\n"
        f"✅ <b>Great!</b> Your <b>note content</b> has been saved.\n\n"
        f"⚡ <b>Step 3:</b> Do you want to save this note permanently? "
        f"Please select <b>Yes</b>, <b>No</b>, or <b>Save as Draft</b>.\n\n"
        f"💡 Tip: You can cancel anytime by typing /cancel."
    )

    return ask_for_save


def new_note_making_confirmation_yes(note_obj: NotePart, user_balance: int) -> str:
    """
    After user choose Yes to save Note in the database.
    This will say about the note with little information
    """
    text = (
        f"Your Note Has Been saved Successfully.\n"
        f"Note Title: <u>{note_obj.note_title}\n</u>"
        f"Your Note Id is: <code>{note_obj.note_id}</code>.\n"
        f"Current Point is: {user_balance}\n"
    )
    return text


def new_note_making_confirmation_no(user: User) -> str:
    """
    Informs the user that the note was not saved
    """
    text = (
        f"Hello {user.mention_html()}, your note has not been saved.\n"
        f"If you want to make a new note, please use /new_note."
    )
    return text


def new_note_making_confirmation_as_draft(note_obj: NotePart) -> str:
    """
    When user want to save his note as draft, means note row:
    Is Available:- False
    """
    text = (
        "✅ <b>Note saved as draft.</b> ✍️\n\n"
        f"{"Note Not Available To See"}\n"
        f"{"Note Not Available To See"}\n"
        f"{"Note Not Available To See"}\n\n"
        f"Title: {note_obj.note_title}\n"
        f"Note Title: <u>{note_obj.note_title}\n</u>"
        f"Your Note Id is: <code>{note_obj.note_id}</code>.\n"
        f"Your note has been stored safely but is currently marked as <b>Not Available</b>. "
        f"You can edit or publish it anytime.\n\n"
        f"💡 Tip: Use /publish to make it available or /cancel to discard."
    )

    return text
