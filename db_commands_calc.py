#!/usr/bin/python3
# -*- coding: utf-8 -*-
# created by neo
# Version-1.0
import os
import sqlite3
from tkinter import *
from myapp import cur, conn






######################################################
#######                                     ##########
#######         Calculation section         ##########
#######                                     ##########
######################################################


def select_DefDens(tk_name):
    cur.execute("SELECT density FROM '%s'" % (tk_name) )
    global density
    density=0
    for dens in cur:
        if len(dens) > 0:
            y=str(dens)
            density=y.strip('(),')
        elif dens==0:
            density=("zero set")
        else:
            density=("Error")
    
    return density


def calculation(tk_name, sound):
    global volume_in_m3
    volume_in_m3=[]
    try:
        cur.execute("SELECT volume FROM '%s' WHERE sound_id='%s'" % (tk_name, sound))
        for data in cur :
            x=str(data)
            x=x.strip('(),')
            volume_in_m3.append(x)

        return  volume_in_m3
        conn.close()
    except Exception as e :
        print(f"Erorr: {e}" )

def def_dens_modify(tk_name, new_val):
    try:
        cur.execute("ALTER TABLE `%s` DROP COLUMN density" % tk_name)
        cur.execute(
            "ALTER TABLE `%s` ADD density FLOAT DEFAULT %s" %(tk_name, new_val) 
            )
        conn.commit()
        
    except Exception as e :
        print(f"DB Connection error: {e}" )