#!/usr/bin/python3
# -*- coding: utf-8 -*-
# created by neo
# Version-1.0

# import csv
import sqlite3

# from main import prev_label_text
# import re
# import os

# file_location_detect = os.getcwd()
# try:
#     name_off_app = "BunkerCalc"
#     conn = sqlite3.connect(
#         (file_location_detect+'/Documents/myapp/bunker_calc.db'), check_same_thread=False)
# except sqlite3.OperationalError as e:
#     name_off_app = "BunkerCalc"
#     conn = sqlite3.connect(
#         (file_location_detect+'/bunker_calc.db'), check_same_thread=False)
conn = sqlite3.connect("viking_ocean.db")
cur = conn.cursor()

# Create empty dict for placing here data from previous DB for Showing on start App
prev_label_text = {}

def add_to_prevdb(tank, val, volume):
    """
    Function for Create Prev DB  tables and inserting data into there
    """
    connection= sqlite3.connect(('bunker_calc_prev.db'))
    
    cur = connection.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS '"+tank+
                "' (sound_id INT ,volume FLOAT NULL,density FLOAT DEFAULT 0.9855 NULL,temperature INT DEFAULT 15 NULL, state INT DEFAULT 0 NULL, type INT DEFAULT 0 NULL) ;")
    
    connection.commit()
    update(tank,val, volume)


def update(t,v,volume):
    """
    Update data in Prev DB
    """
    connection= sqlite3.connect(('viking_ocean_prev.db'))
    
    cur = connection.cursor()
    cur.execute("SELECT * from '"+ t +
            "' ;")
    if len(list(cur)) <= 0:
        cur.execute("INSERT INTO '"+ t +
            "' (sound_id, volume) VALUES (?,?)  ;", (v,volume))

    cur.execute("UPDATE '"+ t +
            "' SET  sound_id = ?, volume=? WHERE rowid=1;", (v, volume))
    connection.commit()
    connection.close()



def extract_prev(e):
    """
    Make a query for extracting data from DB table and inserting into
    empty Dict from beggining of this file
    """
    
    connection= sqlite3.connect(('viking_ocean_prev.db'))
    
    cur = connection.cursor()
    cur.execute("SELECT * from '"+ e +
            "' ;")
    for i in cur:
        prev_label_text[e]=((i[1]),(i[0]))

    connection.close()

    
    

# r = re.compile('[^a-zA-Z-0-9]')


def extract_names():
    """
    Here we connect to our DB and select all tank names
    that we will display in ListBox
    """
    global name_of_tank
    name_of_tank = []
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    for data in cur:
        name_of_tank.append(data)
    return name_of_tank


# def sort_tanks():

#     table_name = []

#     cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
#     for tables in cur:
#         table_name.append(tables)

#     global table_names
#     table_names = []
#     for row in table_name:
#         x0 = str(row).strip('\'(),')
#         cur.execute(" SELECT  state==1 FROM '"+x0+"' WHERE sound_id = 0")
#         for q in cur:
#             x1 = str(q).strip('\'(),')
#             if float(x1) == 0:
#                 table_names.append(row)
#     return table_names


def sort_tanks_mdo():

    table_name_md = []
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    for tables in cur:
        table_name_md.append(tables)

    global table_names_md
    table_names_md = []
    for row in table_name_md:
        x0 = str(row).strip('\'(),')
        cur.execute(" SELECT  state=='"+str(0) +
                    "' FROM '"+x0+"' WHERE sound_id = 0")
        for q in cur:
            x1 = str(q).strip('\'(),')
            if float(x1) == 0:
                table_names_md.append(row)
    return table_names_md


# def create_tk(arg):
#     new_tank = str(arg)
#     if new_tank:
#         new_tank = r.sub('', new_tank)
#         new_tank = new_tank.replace('-', '_')
#     cur.execute("CREATE TABLE IF NOT EXISTS '"+new_tank +
#                 "' (sound_id INT,volume FLOAT NULL,density FLOAT DEFAULT 0.9855 NULL,temperature INT DEFAULT 15 NULL, state INT DEFAULT 0 NULL, type INT DEFAULT 0 NULL, PRIMARY KEY(sound_id)) ;")
#     conn.commit()


# def delete_tk(tk_name):

#     cur.execute("DROP TABLE '%s';" % (tk_name))
#     conn.commit()

# ####### EDIT SECTION ##########


# def edit_row(tk, sound, volume):  # add data to tank database
#     tk = str(tk)

#     if tk:
#         tk = r.sub('', tk)
#         tk = tk.replace('-', '')
#         tk = tk.strip('".,')
#     cur.execute("DELETE FROM '"+tk+"' WHERE sound_id=%s;" % (sound))

#     cur.execute("INSERT INTO '"+tk +
#                 "' (sound_id,volume,density,temperature) VALUES (%s,%s,0.9555,15);" % (sound, volume))
#     conn.commit()


# def show_all_in_tb(arg):  # show all data in specific tank database

#     global all_vol
#     all_vol = []

#     global all_dens
#     all_dens = []

#     global all_temp
#     all_temp = []

#     global all_state
#     all_state = []

#     global all_type
#     all_type = []

#     for i in range(1000):
#         cur.execute(
#             "SELECT sound_id, volume, density,temperature, state, type FROM `%s` WHERE sound_id=%s;" % (arg, i))
#         for data in cur:
#             all_vol.append(str(str(int(data[0]))+"= "+str(float(data[1]))))
#             all_dens.append(str(str(int(data[0]))+"= "+str(float(data[2]))))
#             all_temp.append(str(str(int(data[0]))+"= "+str(int(data[3]))))
#             all_state.append(str(str(int(data[0])) + "= " + str(int(data[4]))))
#             all_type.append(str(str(int(data[0])) + "= " + str(int(data[5]))))

#     return all_vol, all_dens, all_temp, all_state, all_type


# def import_data(tk):
#     file_choose = askopenfilenames(
#         title="Import to tank" + str(tk), initialdir=os.sep+"home/neo/Documents/myapp/"
#     )
#     file_import = str(file_choose).strip('()\',')

#     with open(file_import, 'r') as fin:  # `with` statement available in 2.5+
#         # csv.DictReader uses first line in file for column headings by default
#         dr = csv.DictReader(fin)  # comma is default delimiter
#         to_db = [(i['sound_id'], i['volume']) for i in dr]
#         try:
#             cur.executemany("INSERT INTO '"+tk +
#                             "' (sound_id, volume) VALUES (?, ?);", to_db)
#             conn.commit()
#         except sqlite3.IntegrityError as e:
#             show_error = showerror("Error with input data",
#                                    message="Allready have data. Confirm to Delete\n" +
#                                    str(e)
#                                    )
#             cur.execute("DROP TABLE '%s';" % (tk))
#             show_info = askokcancel(
#                 "Create new tank ",
#                 message=str("Create new tank with name:\n" +
#                             str(tk)
#                             )
#             )
#             if show_info == True:
#                 cur.execute("CREATE TABLE IF NOT EXISTS '"+tk+"' (sound_id INT,volume FLOAT NULL,density FLOAT DEFAULT 0.9855 NULL,\
#                     temperature INT DEFAULT 15 NULL, state INT DEFAULT 0 NULL, type INT DEFAULT 0 NULL, PRIMARY KEY(sound_id)) ;")
#                 conn.commit()
#                 show_info = askokcancel(
#                     "Import again",
#                     message=str("Start to import data to tank:\n" +
#                                 str(tk) + "again?"
#                                 )
#                 )
#                 if show_info == True:
#                     import_data(tk)
#                 else:
#                     pass
#             else:
#                 pass
