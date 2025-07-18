"""
Here i will write code which will do the work
Of Some Database Functions to interect with DB.

And the main logic is i will call this function
and it will work in my main places.

"""

import datetime

from typing import Sequence


from sqlalchemy import Engine
from sqlmodel import func
from sqlmodel import Session, select


from my_modules import bot_config_settings
from my_modules.database_code.models_table import NotePart, UserPart
from my_modules.logger_related import RanaLogger


IST_TIMEZONE = bot_config_settings.IST_TIMEZONE


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


# This Below Is Not Usefull. It Is Just for old reference.
def count_user_notes_old(
    engine: Engine,
    user_id: int,
) -> int:
    """
    This is Old Function's Logic, this is not good.
    I shouldn't use this ever.
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


def get_some_note_rows(
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


def add_one_note_and_update_the_user(
    engine: Engine,
    user_row: UserPart,
    note_row: NotePart,
) -> NotePart:
    """
    I will pass the note obj and user obj, so that i can use this
    funcions in other place to create any note.
    This will also refresh the note_row and user_row value,
    and after run this fun the old variable will be updated value.
    """

    with Session(engine) as session:

        user_row.points -= 1
        user_row.note_count += 1
        note_row.user = user_row

        session.add(note_row)
        session.commit()
        session.refresh(note_row)
        session.refresh(user_row)

    return note_row


def edit_note_obj(engine: Engine, note_obj: NotePart) -> NotePart:
    """
    Save updates to an existing NotePart object.
    Commits any changes made to the object and refreshes it.
    """
    with Session(engine) as session:

        note_obj.edited_time = datetime.datetime.now(IST_TIMEZONE)
        session.add(note_obj)
        session.commit()
        session.refresh(note_obj)

    return note_obj


def add_new_user_to_user_table(engine: Engine, user_row: UserPart) -> UserPart:
    """
    I will pass a user_row obj and this function will try to add the user
    to the usertable and return 0,1 as failure or success.
    It also refresh the given user_row value so i can also use old argument value.
    """
    with Session(engine) as session:
        session.add(user_row)
        session.commit()
        session.refresh(user_row)

    return user_row


def delete_note_obj_old_1(
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
                RanaLogger.warning(
                    f"The Note Row Not Found,maybe the user_id or note_id got changed "
                    "maybe this has some issue i dont know now, when user "
                    "run the fun to delete the row note."
                )
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


def delete_note_obj(
    engine: Engine,
    note_id: str,
    user_id: int | None,
) -> bool:
    """
    Delete a note if it belongs to the given user.
    Returns True if deleted successfully, False otherwise.
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

            if note_row:
                note_row.user.note_count -= 1
                session.delete(note_row)
                session.commit()
                return True

            RanaLogger.warning(
                f"Note not found for note_id={note_id} and user_id={user_id}."
            )

    except Exception as e:
        RanaLogger.warning(f"UNEXPECTED ERROR WHEN DELETING NOTE: {e}")

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


# This function need to change a very big, as on failed in database it will retunr the 0


def delete_all_notes_of_user(engine: Engine, user_id: int) -> int:
    """
    By returning the 0 or the integer value i can know if the note has delted
    or how many notse gote deleted successfully.
    """
    try:
        with Session(engine) as session:
            stmt = select(NotePart).where(NotePart.user_id == user_id)
            results_for_notes = session.exec(stmt).all()

            statement = select(UserPart).where(UserPart.user_id == user_id)
            result_for_user = session.exec(statement).first()

            if result_for_user is None:
                RanaLogger.warning(
                    "User note id deleting but user not exists a big problem"
                )
                return 0

            if not results_for_notes:
                RanaLogger.info(f"No notes found for user_id={user_id}.")
                return 0

            for note in results_for_notes:
                session.delete(note)

            result_for_user.note_count -= len(results_for_notes)

            session.commit()

            RanaLogger.info(
                f"Deleted {len(results_for_notes)} notes for user_id={user_id}."
            )

            return len(results_for_notes)

    except Exception as e:
        RanaLogger.warning(f"Error deleting notes for user_id={user_id}: {e}")
        return 0
