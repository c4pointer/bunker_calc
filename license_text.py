#!/usr/bin/python3
# -*- coding: utf-8 -*-
# created by neo
# Version-1.0

import sqlite3

import sys

import os

import platform

import math

from tkinter import (Frame, Button, Label, Text, Checkbutton, Entry, Listbox,
                     Menu, Tk, IntVar, StringVar, SINGLE, ACTIVE, END, SW, SE,
                     S, UNDERLINE)

from tkinter import ttk

from tkinter import colorchooser

import threading

# import gnupg

# import getpass

import time

from datetime import datetime

from tkinter.messagebox import showerror, showinfo, askokcancel

from pathlib import Path

file_location_detect=os.getcwd()

try:
    name_off_app="BunkerCalc"
    conn=sqlite3.connect((file_location_detect+'/Documents/myapp/Bunker_calc1.db'),check_same_thread=False)
except sqlite3.OperationalError as e:
    name_off_app="BunkerCalc"
    conn=sqlite3.connect((file_location_detect+'/Bunker_calc1.db'),check_same_thread=False)
cur=conn.cursor()

import insert_in_db

import db_commands_calc

import mdo_tanks

import type_calc

import prev_measurments

import threading


def read_license():
    global license_strings
    license_strings=list()
    file_license=str("LICENSE")
    with open(file_license, "r") as f:
        d=f.readlines()
        for strings in d:
            license_strings.append(strings)
    return license_strings

  