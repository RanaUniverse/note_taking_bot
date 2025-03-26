"""
Here i will keep some website's url address so that i can
import easily of this links.
Suppose some google's products related link in one category
social medias links in one category.

"""

from enum import Enum


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
