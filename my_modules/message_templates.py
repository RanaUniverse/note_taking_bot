"""
Here i will make some funcions which will return some demo
Text which i can reuse in different places.
"""

from enum import Enum
import html
import random


from telegram import Chat, Message, User


from my_modules import bot_config_settings
from my_modules.database_code.models_table import NotePart, UserPart

BOT_INFORMATION_WEBSITE = bot_config_settings.BOT_INFORMATION_WEBSITE


MAX_ADD_POINT = bot_config_settings.MAX_ADD_POINT
MAX_CONTENT_LEN = bot_config_settings.MAX_CONTENT_LEN
MAX_TITLE_LEN = bot_config_settings.MAX_TITLE_LEN

IST_TIMEZONE = bot_config_settings.IST_TIMEZONE


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
        f"✏️ /edit_note - Edit an existing note\n"
        f"❌ /delete_note - Delete a note\n"
        f"❓ /help - Get help and usage instructions\n\n"
        f"🚀 <b>New AI Feature:</b>\n"
        f"Ask any question to our smart AI assistant!\n"
        f"💡 Just type like this:\n"
        f"Ask Me Question with /ai like this i send: ⏭⏭⏭"
        f"'<code>/ai What is Artificial Intelligence?</code>' Like This ask."
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
        "<b>Thank you for using the bot 💙</b>\n"
        f"Please Visit The Website to know more about how to use this bot.\n"
        f"{BOT_INFORMATION_WEBSITE}"
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
        f"Hey there, <b>{user.mention_html()}</b>! 🎉👋\n\n"
        f"Oh no! 😢 It looks like you're not registered yet.\n"
        f"Don't worry — it's super easy to fix! 🚀\n\n"
        f"👉 Just send the /register_me command to get started.\n"
        f"Once you're all set, you can come back and start using this awesome bot! 🤖✨\n\n"
        f"Need a hand? 🛠️ No problem! Just type /help and I’ve got you covered. 💬😊"
    )

    return text


def user_has_no_valid_points(user: User) -> str:
    """
    When user has 0 points, it means it will say user
    to buy new points.
    """
    suggested_int_value = random.randint(0, MAX_ADD_POINT)

    text_no_point = (
        f"🚫 <b>Oops!</b> You've run out of points 😢🪄\n\n"
        f"But don't worry — you can easily top up! Just use the command:\n"
        f"<blockquote><code>/add_points {suggested_int_value}</code></blockquote>\n"
        f"(This is just a suggestion — you can choose any number you like 🧮)\n\n"
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
    safe_note_title = html.escape(f"{note_obj.note_title}")
    text = (
        "✅ <b>Your note has been saved successfully!</b>\n\n"
        f"📝 <b>Note Title</b>: <u>{safe_note_title}</u>\n"
        f"🆔 <b>Note ID</b>: <code>{html.escape(note_obj.note_id)}</code>\n"
        f"💰 <b>Available Points</b>: {user_balance}\n"
    )
    return text


def new_note_making_confirmation_no(user: User) -> str:
    """
    Informs the user that the note was not saved
    """
    text = (
        f"❌ Hello {user.mention_html()}, your note was <b>not saved</b>.\n\n"
        f"📝 If you'd like to create a new one, please use /new_note."
    )
    return text


def new_note_making_confirmation_as_draft(note_obj: NotePart) -> str:
    """
    When user want to save his note as draft, means note row:
    Is Available:- False
    """
    text = (
        "✅ <b>Note saved as draft.</b> ✍️\n\n"
        f"Note Not Available To See\n"
        f"Title: {note_obj.note_title}\n"
        f"Note Title: <u>{note_obj.note_title}\n</u>"
        f"Your Note Id is: <code>{note_obj.note_id}</code>.\n"
        f"Your note has been stored safely but is currently marked as <b>Not Available</b>. "
        f"You can edit or publish it anytime.\n\n"
        f"💡 Tip: Use /publish to make it available or /cancel to discard."
    )

    return text


def user_register_success_text(tg_user_obj: User, db_user_row: UserPart) -> str:
    """
    When user register to database got success this text will show
    """

    text_success = (
        f"🎉 Welcome, <b>{tg_user_obj.mention_html()}</b>! 🎉\n\n"
        f"✅ You are now successfully registered!\n"
        f"🪙 You have received <b>{db_user_row.points} Welcome Tokens</b>.\n\n"
        f"📋 You can add more details later using:\n"
        f"   🔹 Buttons below (coming soon!) ⬇️\n"
        f"   🔹 Or use manual commands ⌨️\n\n"
        f"🚀 Let's get started!"
    )
    return text_success


def user_already_register_text(
    tg_user_obj: User,
    db_user_row: UserPart,
    msg_obj: Message,
) -> str:
    """
    When user is already present in database it will execute and
    say the text reply to user back.
    """

    time_formatting = f"Date:%Y-%m-%d, Time:%H-%M-%S"

    old_register_time = db_user_row.account_creation_time
    now = msg_obj.date.astimezone(IST_TIMEZONE).replace(tzinfo=None)
    delta = now - old_register_time

    text_user_exists = (
        f"⚠️ Hello <b>{tg_user_obj.mention_html()}, you're already registered!</b>\n\n"
        f"<b>🗓️ Account created:</b> {old_register_time.strftime(time_formatting)}"
        f" ({delta} ago)\n"
        f"<b>📝 Notes created:</b> {db_user_row.note_count}\n"
        f"<b>💰 Token balance:</b> {db_user_row.points}\n"
        f"<b>🔗 Referral Code:</b> "
        f"{db_user_row.referral_code if db_user_row.referral_code else 'No Refer'}\n"
        f"<b>📧 Email ID:</b> "
        f"{db_user_row.email_id if db_user_row.email_id else 'No Email'}\n"
    )

    return text_user_exists


def user_register_unknown_error() -> str:
    """
    When insert a row gives a unknown error
    Nor insert the data properly nor also integrity error
    i need to just say user a custome text to try how?
    """

    text_error = (
        "A database error occurred during your registration attempt. "
        "Kindly reattempt the registration process. Should the issue persist, "
        "please utilize the /help command to contact an administrator.\n"
        "Please contact admin with proper screenshot or mail us."
    )

    return text_error


def invalid_int_value_in_add_points(
    user_obj: User,
    arg_value: str,
    random_point_value: int,
) -> str:
    """
    When use will send wrong value which cannot be make in int
    This error message will be send to user.
    """
    text_int_not = (
        f"👋 Hello {user_obj.mention_html()}, it looks like you sent:\n\n"
        f"<code>{html.escape(arg_value)}</code>\n\n"
        f"Unfortunately, that's not a valid number of points. ❌\n\n"
        f"For example, to add {random_point_value} points, please use the command:\n"
        f"<code>/add_points {random_point_value}</code> ✅"
    )

    return text_int_not


class WhatMessageAction(Enum):
    VIEW = "👁️ view"
    EDIT = "✏️ edit"
    DELETE = "🗑️ delete"
    SHARE = "📤 share"
    EXPORT = "📦 Export"


def access_denied_messages(user: User, what_action: WhatMessageAction) -> str:
    """
    This is say the text based on
    View
    Edit
    Delete
    Share
    """

    text_old = (  # type: ignore
        f"🚫 <b>Access Denied</b>\n\n"
        f"Dear {user.mention_html()}, you are not the owner of this note and therefore "
        f"cannot {what_action.value} it. 😢\n\n"
        f"If you believe this is an error or need assistance, "
        f"please contact support via /help."
    )

    text = (
        f"🚫 <b>Access Denied</b>\n\n"
        f"Hi <b>{user.full_name}</b>, it seems this note isn't yours.\n\n"
        f"Only the person who created it can <b>{what_action.value}</b> it.\n\n"
        f"If you think this is a mistake — for example, if you’re logged in from a different device "
        f"or had created it earlier — feel free to contact support.\n\n"
        f"🛠 Use /help or message an admin directly.\n\n"
        f"💡 You can also create a new note anytime with /new_note."
    )

    return text


# Below is some constants variables for some text generation.

NOTE_NO_FOUND_TEXT = (
    f"🚫 <b>Note Not Accessible</b>\n\n"
    f"😢 This note is no longer available.\n"
    f"It might have been <b>deleted</b> or "
    f"there was an <b>unexpected issue</b>.\n\n"
    f"📌 Try checking your other notes using /my_notes.\n"
    f"Or You can contact Admins For This issue."
)


SUCCESS_NOTE_DELETE_TEXT = (
    "✅ <b>Note Deleted Successfully!</b>\n\n"
    "🗑️ Your note has been permanently removed from the database.\n"
    "Please remember, this action cannot be undone.\n\n"
    "If you deleted it by mistake, unfortunately, it's gone for good. 😢"
)

FAIL_NOTE_DELETE_TEXT = (
    "⚠️ <b>Deletion Failed</b>\n\n"
    "Something went wrong while trying to delete your note.\n"
    "Please try again later or use <b>/help</b> to contact support. 🛠️ "
    "Please Send Proper Screenshots."
)


def generate_no_note_found_with_note_id(wrong_note: str) -> str:
    """
    When User need to be replied with the bad note id also
    That the note is not accessable i need to use this function.
    As i am using html thats why i need to make the input safe of html
    """

    safe_note_id = html.escape(wrong_note)

    text = (
        f"🚫 The Note ID You provided (<code>{safe_note_id}</code>) "
        f"seems to be invalid.\n\n"
        f"{NOTE_NO_FOUND_TEXT}"
    )

    return text


def user_complete_details_text(tg_user_obj: User, user_row: UserPart) -> str:
    """
    When Bot will say some information about the user completely this demo
    Templates of the text can be say to user back.
    """

    created_at = user_row.account_creation_time.strftime("%d %b %Y, %I:%M %p")
    full_name = tg_user_obj.mention_html()

    account_text = (
        f"👤 <b>Account Details</b>\n\n"
        f"📛 <b>Name:</b> {full_name or 'N/A'}\n"
        f"🔗 <b>Username:</b> @{user_row.username or 'N/A'}\n"
        f"🆔 <b>User ID:</b> <code>{user_row.user_id}</code>\n\n"
        f"📝 <b>Total Notes:</b> {user_row.note_count}\n"
        f"💎 <b>Points:</b> {user_row.points}\n"
        f"🕰️ <b>Joined On:</b> {created_at}\n"
    )

    if user_row.email_id:
        account_text += f"📧 <b>Email:</b> {user_row.email_id}\n"
    if user_row.phone_no:
        account_text += f"📱 <b>Phone:</b> {user_row.phone_no}\n"
    if user_row.referral_code:
        account_text += (
            f"🎁 <b>Referral Code:</b> " "<code>{user_row.referral_code}</code>\n"
        )

    return account_text


def generate_delete_confirmation_with_note_info_text(note_row: NotePart) -> str:
    title = f"{note_row.note_title or 'Untitled Note'}"

    created_info = (
        f"{note_row.created_time.strftime('%d %b %Y, %I:%M %p')}"
        if note_row.created_time
        else "Unknown"
    )

    edited_info = (
        f"✏️ <b>Last Edited:</b> <code>{note_row.edited_time.strftime('%d %b %Y, %I:%M %p')}</code>\n"
        if note_row.edited_time
        else ""
    )

    text = (
        f"⚠️ <b>Delete Confirmation</b>\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"<b>📝 Title:</b> <code>{html.escape(title)}</code>\n"
        f"<b>📅 Created On:</b> <code>{created_info}</code>\n"
        f"{edited_info}"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"🚫 <i>This action is <b>permanent</b> and cannot be undone!</i>\n"
        f"Are you absolutely sure you want to <b>delete</b> this note?\n\n"
        f"👇 Please confirm your choice:"
    )
    return text
