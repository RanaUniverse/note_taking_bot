"""
This is the engine part having the engine to use
and it will have a table making fun
i need to import `create_db_and_engine()`
"""

from pathlib import Path


from sqlmodel import (
    create_engine,
    SQLModel,
)


from my_modules import bot_config_settings


DATABASE_FILE_NAME = bot_config_settings.DATABASE_FILE_NAME


sqlite_file_name = Path.cwd() / DATABASE_FILE_NAME


sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(url=sqlite_url)


def create_db_and_engine():
    """
    When i will call this function it will make the database file,
    i need to call this in the main.py beginning
    """
    sqlite_file_name.parent.mkdir(exist_ok=True)
    SQLModel.metadata.create_all(engine)
