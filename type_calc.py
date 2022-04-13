#!/usr/bin/python3
# -*- coding: utf-8 -*-
# created by neo
# Version-1.0
import os
import sqlite3
from tkinter import (Label, Button, Checkbutton,
    Frame, Listbox, Tk, IntVar, Menu, UNDERLINE, StringVar,
    Entry)
from main import cur, conn
import insert_in_db



def check_tk_type(tk):
   
    global set_type
    global type_dict
    
    type_dict = list()
    
    cur.execute("SELECT type FROM '%s' " % (tk))
    for data in cur:
        
        if int(data[0]) == 0 :
            set_type = 0
            type_dict.append(data[0])
        if int(data[0]) == 1 :
            
            set_type = 1
            type_dict.append(data[0])

    return type_dict

