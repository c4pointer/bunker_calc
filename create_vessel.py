import sqlite3
from sqlite3 import Error
from main import logger
def create_vessel(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    conn_prev = None
    try:
        # create new vessel database
        conn = sqlite3.connect(db_file+".db")
        conn_prev = sqlite3.connect(db_file+"_prev.db")
    except Error as error:
       logger.warning(error)
    finally:
        if conn:
            conn_prev.close()
            conn.close()
