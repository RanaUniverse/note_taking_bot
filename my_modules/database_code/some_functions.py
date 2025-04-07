"""
Here i will write code which is same as

def count_user_notes(user_id: str) -> int
    # do logic to return a number of notes


def get_user_notes(user_id: str, offset: int = 0, limit: int = 10) -> list[NotePart]:
    # do logic to get user notes

And the main logic is i will call this function and it will work in my main places.

"""

from typing import Sequence


from sqlalchemy import Engine

from sqlmodel import func
from sqlmodel import Session, select

# from my_modules.database_code.database_make import engine

from my_modules.database_code.models_table import NotePart


def count_user_notes_old(
    engine: Engine,
    user_id: int,
) -> int:
    """
    When the user_id (from tg) is passed it will count the total note he own
    and return the integer value of his notes
    """

    with Session(engine) as session:

        statement = select(NotePart).where(NotePart.user_id == user_id)
        results = session.exec(statement).all()
        all_note_count = len(results)

        return all_note_count


def count_user_notes(
    engine: Engine,
    user_id: int,
) -> int:
    """
    This is the new way of getting a information of note row by a condition,
    i will pass the user id and it will return how many notes he has by finding
    notes's row's user_id value match this or not.

    """

    with Session(engine) as session:
        statement = (
            select(func.count())
            .select_from(NotePart)
            .where(NotePart.user_id == user_id)
        )

        all_note_count = session.exec(statement).one()
        return all_note_count


def get_user_notes(
    engine: Engine,
    offset_value: int,
    limit_value: int,
    user_id: int,
) -> list[NotePart] | Sequence[NotePart]:
    """
    here i will pass the how many row i want to get and from which
    """

    with Session(engine) as session:
        statement = (
            select(NotePart)
            .where(NotePart.user_id == user_id)
            .offset(offset_value)
            .limit(limit_value)
        )
        results = session.exec(statement)
        notes = results.all()

        return notes


def note_obj_from_note_id(
    engine: Engine,
    note_id: str,
) -> NotePart | None:
    """
    i want to pass the note_id = uuid4().hex which i got from user
    and then access the note obj or None
    """
    with Session(engine) as session:
        statement = select(NotePart).where(NotePart.note_id == note_id)
        results = session.exec(statement)
        note_row = results.first()

    return note_row
