"""
Here i will keep some database related logics and code and
i will import those thigns in my main.py to work with
"""

import datetime
from uuid import uuid4

from my_modules import bot_config_settings

from sqlmodel import (
    Field,
    # Session,
    SQLModel,
    # create_engine,
    Relationship,
)

GMT_TIMEZONE = bot_config_settings.GMT_TIMEZONE
IST_TIMEZONE = bot_config_settings.IST_TIMEZONE


class UserPart(SQLModel, table=True):
    __tablename__: str = "user_data"  # type: ignore

    id_: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, unique=True, index=True)
    username: str | None = Field(default=None, index=True)
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    note_count: int = Field(default=0)
    points: int = Field(default=0)
    account_creation_time: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(IST_TIMEZONE),
    )
    referral_code: str | None = Field(default=None)
    email_id: str | None = Field(default=None)
    phone_no: str | None = Field(default=None)

    notes: list["NotePart"] = Relationship(back_populates="user")


class NotePart(SQLModel, table=True):
    __tablename__: str = "note_data"  # type: ignore

    id_: int | None = Field(default=None, primary_key=True)
    note_id: str = Field(default_factory=lambda: uuid4().hex.upper(), index=True)
    # Use a lambda function for unique id i will for each note.
    note_title: str | None = Field(default=None)
    note_content: str | None = Field(default=None)
    user_id: int | None = Field(default=None, foreign_key="user_data.user_id")
    # i kept None, for some checking when user delete his note, i used to find easily
    created_time: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(IST_TIMEZONE),
    )
    edited_time: datetime.datetime | None = Field(default=None)
    is_available: bool = Field(default=True)

    user: UserPart = Relationship(back_populates="notes")


def main():

    import random
    from faker import Faker

    fake = Faker()
    new_user = UserPart(
        user_id=random.randrange(0, 100000001, 5),
        username=fake.name().replace(" ", ""),
        email_id=fake.free_email(),
    )
    print(new_user)


if __name__ == "__main__":
    main()
