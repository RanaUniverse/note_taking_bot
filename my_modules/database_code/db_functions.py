"""
Here i will write code which is same as

def count_user_notes(user_id: str) -> int
    ## do logic to return a number of notes


def get_user_notes(user_id: str, offset: int = 0, limit: int = 10) -> list[NotePart]:
    ## do logic to get user notes

And the main logic is i will call this function and it will work in my main places.

"""

from typing import Sequence


from sqlalchemy import Engine

from sqlmodel import func
from sqlmodel import Session, select

# from my_modules.database_code.database_make import engine

from my_modules.database_code.models_table import NotePart, UserPart
from my_modules.logger_related import RanaLogger


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
) -> Sequence[NotePart]:
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


def user_obj_from_user_id(
    engine: Engine,
    user_id: int,
) -> UserPart | None:
    """
    here i will pass the user_id and it will send me the user obj or none if not
    This user_id value will come from telegram user id unique id
    """

    with Session(engine) as session:
        statement = select(UserPart).where(UserPart.user_id == user_id)
        results = session.exec(statement)
        user_row = results.first()

    return user_row


def delete_note_obj(
    engine: Engine,
    note_id: str,
    user_id: int | None,
) -> bool:
    """
    Here i will pass the note id and user id, it will check if the note's owner is the
    user id, if yes, then it will delete the note and return the True
    after successful deleteion of the note obj
    """

    try:
        with Session(engine) as session:
            stat = (
                select(NotePart)
                .where(NotePart.note_id == note_id)
                .where(NotePart.user_id == user_id)
            )
            results = session.exec(stat)
            note_row = results.first()

            if note_row is None:
                print("Note Row is not present this, should not happens")
                return False

            else:
                session.delete(note_row)
                session.commit()
                return True

    except Exception as e:
        RanaLogger.warning(
            f"Somehing unexpectd maybe a error in database when deleting the note, "
            f"{e}".upper()
        )

        return False


def add_point_to_user_obj(
    engine: Engine,
    user_row: UserPart,
    how_many_points: int,
) -> UserPart:
    """
    Before passing the user_obj i need to sure that the row is present
    or it will be shows problem
    Here i will pass the user obj which take a existing user obj
    and after adding the points return back the new updated user obj
        *** Even if i will not use the return value i can use the old obj value which will got updted automatically
    """
    with Session(engine) as session:
        user_row.points += how_many_points
        session.add(user_row)
        session.commit()
        session.refresh(user_row)

        return user_row
