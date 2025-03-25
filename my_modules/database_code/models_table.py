"""
Here i will keep some database related logics and code and
i will import those thigns in my main.py to work with
"""

import datetime
from uuid import uuid4

from sqlmodel import (
    Field,
    # Session,
    SQLModel,
    # create_engine,
    Relationship,
)

IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
GMT = datetime.timezone(datetime.timedelta(hours=0, minutes=0))


class UserPart(SQLModel, table=True):
    __tablename__: str = "user_data"  # type: ignore

    id_: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, unique=True)
    username: str | None = Field(default=None, index=True)
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    note_count: int = Field(default=0)
    points: int | None = Field(default=None)
    account_creation_time: datetime.datetime | None = Field(
        default_factory=lambda: datetime.datetime.now(IST),
    )
    referral_code: str | None = Field(default=None)
    email_id: str | None = Field(default=None)
    phone_no: str | None = Field(default=None)

    notes: list["NotePart"] = Relationship(back_populates="user")


class NotePart(SQLModel, table=True):
    __tablename__: str = "note_data"  # type: ignore

    id_: int | None = Field(default=None, primary_key=True)
    note_id: str = Field(
        default_factory=lambda: uuid4().hex.upper(),
    )
    # Use a lambda function for unique id i will for each note.
    note_title: str | None = Field(default=None)
    note_content: str | None = Field(default=None)
    user_id: int | None = Field(default=None, foreign_key="user_data.id_")
    # i kept None, for some checking when user delete his note, i used to find easily
    created_time: datetime.datetime | None = Field(
        default_factory=lambda: datetime.datetime.now(IST),
    )
    edited_time: datetime.datetime | None = Field(default=None)
    availability: bool | None = Field(default=None)

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
