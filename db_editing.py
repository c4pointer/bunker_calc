#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# created by Oleg Zubak
# Version-1.0

import sqlite3
from typing import List, Union

def connect_to_db(vessel: str) -> sqlite3.Connection:
    """
    Establishes a connection to the SQLite database.

    Args:
        vessel (str): The name of the database file.

    Returns:
        sqlite3.Connection: A connection object to the database.
    """
    return sqlite3.connect(vessel)

def select_DefDens(tk_name: str, vessel: str) -> str:
    """
    Selects the default density for a given tank.

    Args:
        tk_name (str): The name of the tank.
        vessel (str): The name of the database file.

    Returns:
        str: The density value or an error message.
    """
    with connect_to_db(vessel) as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT density FROM '{tk_name}' WHERE sound_id='1'")
        result = cur.fetchone()

    if result:
        return str(result[0])
    elif result == (0,):
        return "zero set"
    else:
        return "Error"

def calculation(tk_name: str, sound: str, vessel: str) -> List[str]:
    """
    Retrieves the volume for a given tank and sound level.

    Args:
        tk_name (str): The name of the tank.
        sound (str): The sound level.
        vessel (str): The name of the database file.

    Returns:
        List[str]: A list containing the volume in m3.
    """
    try:
        with connect_to_db(vessel) as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT volume FROM '{tk_name}' WHERE sound_id=?", (sound,))
            result = cur.fetchone()
        
        return [str(result[0])] if result else []
    except Exception as e:
        print(f"Error in calculation: {e}")
        return []

def type_sel(tank: str, vessel: str) -> List[str]:
    """
    Selects the type of tank.

    Args:
        tank (str): The name of the tank.
        vessel (str): The name of the database file.

    Returns:
        List[str]: A list containing the tank type.
    """
    with connect_to_db(vessel) as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT type FROM '{tank}' WHERE sound_id='0'")
        result = cur.fetchone()
    
    return [result[0]] if result else []

def state_sel(tank: str, vessel: str) -> List[int]:
    """
    Selects the state of the tank.

    Args:
        tank (str): The name of the tank.
        vessel (str): The name of the database file.

    Returns:
        List[int]: A list containing the tank state.
    """
    with connect_to_db(vessel) as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT state FROM '{tank}' WHERE sound_id='0'")
        result = cur.fetchone()
    
    return [result[0]] if result else []

