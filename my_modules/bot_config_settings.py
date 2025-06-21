"""
In This file i will keep some constants which is like
Some Settings Values

"""

import datetime
from enum import Enum
import os
import sys


from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN_GET = os.environ.get("BOT_TOKEN")
if BOT_TOKEN_GET is None:
    print(
        ".no .env file or env file has not any bot token. "
        "Please make sure the token is there and re run this program."
    )
    sys.exit(1)
    # i did exit so that in below in bot token it will always a str not none


BOT_USERNAME_GET = os.environ.get("BOT_USERNAME", None)
if not BOT_USERNAME_GET:
    raise ValueError("❌ BOT_USERNAME not found in .env file!")


BOT_TOKEN = f"{BOT_TOKEN_GET}"
BOT_USERNAME = f"{BOT_USERNAME_GET}"


DEFAULT_REGISTER_TOKEN = 3000

MAX_TITLE_LEN: int = 500
MAX_CONTENT_LEN: int = 4000

MAX_ADD_POINT = 1001
MAX_FAKE_NOTE_COUNT = 9999


NOTES_PER_PAGE = 10
OFFSET_VALUE = 0

NOTE_PREVIEW_CHAR_LIMIT = 100

ADMIN_ID_1 = 1895194333

TEM_FOLDER_NOTE_STORE = "000_user_msg"
WILL_TEM_NOTE_DELETE: bool = True

GROUP_LINK = "RanaUniverse"
LOG_FILE_NAME = "RanaUniverse_Log_File.log"
DATABASE_FILE_NAME = "DATABASE.db"


# This below is the link of about the bot and how to use this
BOT_INFORMATION_WEBSITE = "https://telegra.ph/How-To-Use-Note-Taking-Bot-06-20"
UPGRADE_ACCOUNT_PRO_WEBSITE = "https://telegra.ph/Pro-Members-Features-06-21"

ADD_POINT_WAIT_TIME = 3
REGISTER_ACCOUNT_WAIT_TIME = 3


# Below are some Regular Important Needy Constants


GMT_TIMEZONE = datetime.timezone(datetime.timedelta(hours=0, minutes=0))
IST_TIMEZONE = datetime.timezone(datetime.timedelta(hours=5, minutes=30))


# This below values is working for me, so before run the script
# Make sure to check the values and use it properly
class MessageEffectEmojies(Enum):
    """
    This class content will have some content which help
    to send the user some message with some animations so that it will looks good...
    Some Values are as:
    LIKE = 👍
    DISLIKE = 👎
    HEART = ❤️
    FLAME = 🔥
    TADA = 🎉
    POO = 💩
    """

    LIKE = "5107584321108051014"
    DISLIKE = "5104858069142078462"
    HEART = "5159385139981059251"
    FLAME = "5104841245755180586"
    TADA = "5046509860389126442"
    POO = "5046589136895476101"
