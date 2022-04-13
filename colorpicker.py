#!/usr/bin/python3
# -*- coding: utf-8 -*-
# created by neo
# Version-1.0
import sqlite3

import sys

import os

from tkinter import (Frame, Button, Label, Text, Checkbutton, Entry, Listbox,
                     Menu, Tk, IntVar, StringVar, SINGLE, ACTIVE, END, SW, SE,
                     S, UNDERLINE)

from tkinter import ttk

from tkinter import colorchooser

import threading

import time

from datetime import datetime

from tkinter.messagebox import showerror, showinfo, askokcancel

class App(Frame):
    # def __init__(self, master=None):
    #     super().__init__(master)
    #     self.master = master
    #     self.master.title()
    #     self.master.maxsize(420,250)
    #     self.master.minsize(420,250)

    #     # self.master.geometry('500x300')
    #     self.grid(ipadx=1, ipady=1, rowspan=5, columnspan=5)


        color=colorchooser.askcolor()
        print(color[1])

         
if __name__ == "__main__":
    root = Tk()
    app = App(master=root)
    app.mainloop()