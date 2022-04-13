#!/usr/bin/python3
# -*- coding: utf-8 -*-
# created by neo
# Version-1.0

import os
import sqlite3
from tkinter import (Label, Button, Checkbutton,
    Frame, Listbox, Tk, IntVar, Menu, UNDERLINE, StringVar,
    Entry)

file_location_detect=os.getcwd()

try:
    name_off_app="BunkerCalc"
    conn=sqlite3.connect((file_location_detect+'/Documents/myapp/Bunker_calc_prev.db'),check_same_thread=False)
except sqlite3.OperationalError as e:
    name_off_app="BunkerCalc"
    conn=sqlite3.connect((file_location_detect+'/Bunker_calc_prev.db'),check_same_thread=False)
cur=conn.cursor()

# def select_DefDens(tk_name):
#     cur.execute("SELECT density FROM '%s'" % (tk_name) )
#     global density
#     density=0
#     for dens in cur:
#         if len(dens) > 0:
#             y=str(dens)
#             density=y.strip('(),')
#         elif dens==0:
#             density=("zero set")
#         else:
#             density=("Error")
    
#     return density

def create_tk(name, sound, volume, temperature, density, result_mt):
    try:
        name_off_app="BunkerCalc"
        conn=sqlite3.connect((file_location_detect+'/Documents/myapp/Bunker_calc_prev.db'),check_same_thread=False)
    except sqlite3.OperationalError as e:
        name_off_app="BunkerCalc"
        conn=sqlite3.connect((file_location_detect+'/Bunker_calc_prev.db'),check_same_thread=False)
    cur=conn.cursor()
    
    cur.execute("DROP TABLE IF EXISTS '%s';" % (name))
    conn.commit()
    
    cur.execute("CREATE TABLE IF NOT EXISTS '"+name+"' (sound_id INT,volume FLOAT NULL, temperature INT, density FLOAT , result_mt, PRIMARY KEY(sound_id)) ;")
    
    
    t=str(result_mt)
    result_mt=t.strip(' mt')
    cur.execute("INSERT INTO '%s' (sound_id,volume,temperature,density,result_mt) VALUES (%s,%s,%s,%s, %s);" % (name,sound, volume, temperature, density, result_mt))
    conn.commit()

    
def extract_from_prev_db(name):
    
    global sound_insert
    sound_insert={}
    
    global volume_insert
    volume_insert={}
    
    global temperature_insert
    temperature_insert={}
    
    global density_insert
    density_insert={}
    
    global result_insert
    result_insert={}

    cur.execute("SELECT * FROM '%s';" % (name))
    for int_data in cur:
        sound_insert = int_data[0]
        volume_insert = int_data[1]
        temperature_insert = int_data[2]
        density_insert = int_data[3]
        result_insert = int_data[4]
        
    return sound_insert, volume_insert, temperature_insert, density_insert, result_insert

def all_tanks_name():
    global name_of_all_tanks
    name_of_all_tanks={}
    
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    for tables in cur:
        y=str(tables)
        tables=y.strip('\'(),')
        name_of_all_tanks[tables] = tables
    
    return name_of_all_tanks
    
    
