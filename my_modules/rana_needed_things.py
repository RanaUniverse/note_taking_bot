"""
I have kept some useful things here, which i don't
Understand where i will use those things.
Here i will keep some reusable code for now i dont think
where i can replace those things, this is just for now here
"""

import datetime
from pathlib import Path


from telegram import User


from my_modules import bot_config_settings


TEM_FOLDER_NOTE_STORE = bot_config_settings.TEM_FOLDER_NOTE_STORE


def get_current_indian_time() -> datetime.datetime:
    """
    When this fun will execute it will say current indian time
    """

    now_time_gmt = datetime.datetime.now(tz=datetime.timezone.utc)
    now_time_ind = now_time_gmt + datetime.timedelta(hours=5, minutes=30)
    return now_time_ind


def make_footer_text(
    user: User,
    use_current_time: bool = True,
) -> str:
    """
    This will make a Demo Footer Text Saying The current time and
    some user informations.
    """

    username = f"@{user.username}" if user.username else "Not Available ❌"

    user_info = (
        f"Full Name       : {user.full_name}\n"
        f"User ID         : {user.id}\n"
        f"Username        : {username}\n"
    )

    if use_current_time:
        ist_time = get_current_indian_time()
        time_info = f"{ist_time.strftime('%Y-%m-%d %H:%M:%S')} IST"
    else:
        time_info = "No Time Information ❌❌❌"

    time_str = f"\n----------\n" f"Note Export Time:\n" f"{time_info}\n" "----------"

    breaking_str = f"\n\n\n\n\n" f"----------" f"\n"

    output_txt = breaking_str + user_info + time_str

    return output_txt


def create_txt_file_from_string(
    content: str,
    filename: str,
    file_dir: Path | None = None,
) -> Path:
    """
    Creates a .txt file with the given content and filename in the specified folder.
    """
    if file_dir is None:
        file_dir = Path.cwd() / TEM_FOLDER_NOTE_STORE
        file_dir.mkdir(parents=True, exist_ok=True)

    else:
        file_dir.mkdir(parents=True, exist_ok=True)

    if not filename.endswith(".txt"):
        filename += ".txt"

    file_path = file_dir / filename
    file_path.write_text(content)

    return file_path
