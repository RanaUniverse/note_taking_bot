"""
In This file i will keep some constants which is like
Some Settings Values

"""

import datetime
import os
import sys


BOT_TOKEN = os.environ.get("BOT_TOKEN")
if BOT_TOKEN is None:
    print(
        ".no .env file or env file has not any bot token. "
        "Please make sure the token is there and re run this program."
    )
    sys.exit(1)
    # i did exit so that in below in bot token it will always a str not none


BOT_USERNAME = os.environ.get("BOT_USERNAME", None)
if not BOT_USERNAME:
    raise ValueError("❌ BOT_USERNAME not found in .env file!")


DEFAULT_REGISTER_TOKEN = 3000

MAX_TITLE_LEN: int = 500
MAX_CONTENT_LEN: int = 4000

MAX_ADD_POINT = 1001
ADD_POINT_WAIT_TIME = 3
MAX_FAKE_NOTE = 1001


NOTES_PER_PAGE = 10
OFFSET_VALUE = 0

ADMIN_ID_1 = 1895194333

FOLDER_NOTE_TEM_NAME = "000_user_msg"

GROUP_LINK = "RanaUniverse"
LOG_FILE_NAME = "RanaUniverse_Log_File.log"


IST_TIMEZONE = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
