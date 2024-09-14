import sqlite3
from sqlite3 import Error
from main import logger

def create_vessel(db_file):
    """
    Create two SQLite database connections: one for the main database and one for the previous version.

    Args:
        db_file (str): The base name of the database file (without extension).

    Returns:
        tuple: A tuple containing two SQLite connection objects (main_conn, prev_conn).
               Returns (None, None) if connections couldn't be established.
    """
    main_conn = None
    prev_conn = None

    try:
        main_conn = sqlite3.connect(f"{db_file}.db")
        prev_conn = sqlite3.connect(f"{db_file}_prev.db")
        return main_conn, prev_conn
    except Error as error:
        logger.error(f"Error creating database connections: {error}")
        if main_conn:
            main_conn.close()
        if prev_conn:
            prev_conn.close()
        return None, None
