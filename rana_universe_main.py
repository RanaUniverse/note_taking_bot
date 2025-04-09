"""'
This file i will check some python code how those is running
"""

from my_modules.database_code import db_functions
from my_modules.database_code.database_make import engine

usr = 5393096971
nots = "00441077BE3A469E8E88D0CFEFF86B02"


rana = db_functions.delete_note_obj(engine, nots, usr)


print(rana)

if rana:
    print("The Note has been deleted successfully.")
else:
    print("note delete got failed.")
