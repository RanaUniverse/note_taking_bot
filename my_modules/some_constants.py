"""
Here i will keep some website's url address so that i can
import easily of this links.
Suppose some google's products related link in one category
social medias links in one category.

I will use this from where i will import others constants which will come
from the config or env files.

"""

import datetime
from enum import Enum
import os
import sys

from dotenv import load_dotenv

load_dotenv()


class GoogleProductsUrl(Enum):
    GOOGLE = "https://www.google.com"
    GMAIL = "https://mail.google.com"
    DRIVE = "https://drive.google.com"


class SocialMediaUrl(Enum):
    FACEBOOK = "https://www.facebook.com"
    TWITTER = "https://www.twitter.com"
    LINKEDIN = "https://www.linkedin.com"


class ImageLinks(Enum):
    RU_IMAGE = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSEjeabRvIoe4fpLe5qBTHzNQw1sfrOafBVos1KwWM9IJOT41hX0mxrocF6&s=10"

    RU_IMAGE_2 = "https://scontent.fccu13-4.fna.fbcdn.net/v/t39.30808-6/482980943_661157046599546_8694658622174943763_n.jpg?_nc_cat=100&ccb=1-7&_nc_sid=833d8c&_nc_ohc=Ue-dhnbbSIEQ7kNvgELCCFX&_nc_oc=AdmviZKvpalxkqyxZnqxKyTdXPGapi1QoCCd96HO92Pba-YzO_A927z6As0O4Oo_WZhJnNhq3E9FI2TcIis09eAp&_nc_zt=23&_nc_ht=scontent.fccu13-4.fna&_nc_gid=w2Ixq3rnvE8un1h8QF_xKw&oh=00_AYFaj-PfTmvLBV35bAHxIGMkLzQyApVMC3O8FxkAhM9J1Q&oe=67E35DB1"


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


class PrivateValue(Enum):
    BOT_TOKEN = BOT_TOKEN
    BOT_USERNAME = BOT_USERNAME


class BotSettingsValue(Enum):
    """
    Here some values like settings will be there.
    """

    DEFAULT_REGISTER_TOKEN = 3000
    MAX_TITLE_LEN = 100
    MAX_CONTENT_LEN = 4000

    MAX_ADD_POINT = 1001
    ADD_POINT_WAIT_TIME = 3
    MAX_FAKE_NOTE = 1001

    FOLDER_NOTE_TEM_NAME = "000_user_msg"

    NOTES_PER_PAGE = 10
    OFFSET_VALUE = 0

    ADMIN_ID_1 = 1895194333

    GROUP_LINK = "RanaUniverse"
    LOG_FILE_NAME = "RanaUniverse_Log_File.log"


IST_TIMEZONE = datetime.timezone(datetime.timedelta(hours=5, minutes=30))


if __name__ == "__main__":

    my_name = "Rana Universe"
    print(my_name)
