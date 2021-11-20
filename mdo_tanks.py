#!/usr/bin/python3
# -*- coding: utf-8 -*-
# created by neo
# Version-1.0

import sqlite3
import os, re

from myapp import cur, conn

r = re.compile('[^a-zA-Z-0-9]')

def mdo_select_tank(tk_name, new_state):
    try:
        cur.execute("ALTER TABLE `%s` DROP COLUMN state" % tk_name)
        cur.execute(
            "ALTER TABLE `%s` ADD state FLOAT DEFAULT %s" %(tk_name, new_state) 
            )
        conn.commit()
        
    except Exception as e :
        print(f"DB Connection error: {e}" )
    

def mdo_show():
    table_name=[]
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    for tables in cur:
        table_name.append(tables)
    global mdo_tanks_arr
    mdo_tanks_arr=[]
    try:
        
        for row in table_name:
            
            x0=str(row).strip('\'(),')
            cur.execute(" SELECT  state FROM '"+x0+"' WHERE sound_id = 0" )
            for q in cur:
                x1=str(q).strip('\'(),')
                if float(x1) == 1:
                    mdo_tanks_arr.append(row)      
            
    except Exception as e:
        print(f"MDO show errors: {e}" )

    return mdo_tanks_arr


def check_tk_for_mdo(tk):
    global set_value
    
    try:
       
        cur.execute("SELECT state FROM '%s' " % (tk))
        for data in cur:
            
            if int(data[0]) == 0 :
                set_value = 0

            if int(data[0]) == 1 :
                
                set_value = 1
        
    except Exception as e:
        print(f"MDO show errors: {e}" )
        
    return set_value


