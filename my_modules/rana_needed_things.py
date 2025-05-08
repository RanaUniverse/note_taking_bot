"""
Here i will keep some reusable code for now i dont think
where i can replace those things, this is just for now here
"""

import datetime

from telegram import Message, User


def make_footer_text(
    user: User,
    msg: Message | None = None,
) -> str:
    """
    i though to make a footer where it will give me
    user some informaiton and the time
    """

    username = f"@{user.username}" if user.username else "Not Available ❌"

    breaking_str = f"\n\n\n\n\n" f"----------" f"\n"

    user_info = (
        f"Full Name: {user.full_name}\n"
        f"UserID: {user.id}\n"
        f"Username: {username}\n"
    )
    if msg is None:
        time_str = (
            f"\n\n\n\n\n"
            f"----------"
            f"\n"
            f"Response Time: \n"
            f"No Time Information ❌❌❌"
            f"\n\n\n\n\n"
            f"----------"
            f"\n"
        )

    else:
        utc_time = msg.date.replace(tzinfo=None)

        current_ind_time = utc_time + datetime.timedelta(hours=5, minutes=30)
        time_str = (
            f"\n\n\n\n\n"
            f"----------"
            f"\n"
            f"Response Time: \n{current_ind_time}"
            f"\n\n\n\n\n"
            f"----------"
            f"\n"
        )
    output_txt = breaking_str + user_info + time_str

    return output_txt
