#!/usr/bin/python3
# -*- coding: utf-8 -*-
# created by neo
# Version-1.0
import os
import sqlite3

file_location_detect = os.getcwd()
try:
    name_off_app = "BunkerCalc"
    conn = sqlite3.connect(
        (file_location_detect+'/Documents/myapp/Bunker_calc.db'), check_same_thread=False)
except sqlite3.OperationalError as e:
    name_off_app = "BunkerCalc"
    conn = sqlite3.connect(
        (file_location_detect+'/Bunker_calc.db'), check_same_thread=False)
cur = conn.cursor()


# def select_DefDens(tk_name):
#     cur.execute("SELECT density FROM '%s'" % (tk_name))
#     global density
#     density = 0
#     for dens in cur:
#         if len(dens) > 0:
#             y = str(dens)
#             density = y.strip('(),')
#         elif dens == 0:
#             density = ("zero set")
#         else:
#             density = ("Error")

#     return density


def calculation(tk_name, sound):
    '''
    Takes value from DB
    '''
    global volume_in_m3
    volume_in_m3 = []
    try:
        cur.execute("SELECT volume FROM '%s' WHERE sound_id='%s'" %
                    (tk_name, sound))
        for data in cur:
            x = str(data)
            x = x.strip('(),')
            volume_in_m3.append(x)

        return volume_in_m3
        conn.close()
    except Exception as e:
        print(f"Erorr: {e}")


# def def_dens_modify(tk_name, new_val):
#     try:
#         cur.execute("ALTER TABLE `%s` DROP COLUMN density" % tk_name)
#         cur.execute(
#             "ALTER TABLE `%s` ADD density FLOAT DEFAULT %s" % (
#                 tk_name, new_val)
#         )
#         conn.commit()

#     except Exception as e:
#         print(f"DB Connection error: {e}")


# def type_select_tank(tk_names, new_type):

#     try:
#         # try to know what type of tank is it from
#         # and if "new_type" == 0 then add new table type
#         if new_type == 0:
#             cur.execute("ALTER TABLE `%s` DROP COLUMN type" % tk_names)
#             cur.execute(
#                 "ALTER TABLE `%s` ADD type INT DEFAULT %s" % (
#                     tk_names, new_type)
#             )
#             conn.commit()
#         else:
#             new_type_tk_add(tk_names, new_type)

#     except Exception as e:
#         print(f"DB Connection error: {e}")


# def new_type_tk_add(tk, t):
#     try:
#         cur.execute("ALTER TABLE `%s` DROP COLUMN type" % tk)
#         cur.execute(
#             "ALTER TABLE `%s` ADD type INT DEFAULT %s" % (tk, t)
#         )

#         cur.execute("ALTER TABLE `%s` DROP COLUMN volume" % tk)
#         cur.execute(
#             "ALTER TABLE `%s` ADD volume FLOAT DEFAULT 0" % tk
#         )
#         conn.commit()
#     except Exception as error:
#         print(f"DB Connection error on string 87: {error}")
