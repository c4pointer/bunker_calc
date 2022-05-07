#!/usr/bin/python3
# -*- coding: utf-8 -*-
# created by Zubak Oleg
# Version-1.1

import sqlite3

import sys

import os

import platform

import math

from tkinter import (Frame, Button, Label, Text, Checkbutton, Entry, Toplevel, Listbox,
                     Menu, Tk, IntVar, StringVar, SINGLE, ACTIVE, END, SW, SE,
                     S, UNDERLINE, NORMAL, DISABLED, HORIZONTAL)

from tkinter import ttk

from tkinter import colorchooser

import threading

# import gnupg

# import getpass

import time

import threading

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

import license_text


operation_platform = str("Arch_Linux") # platform.system()

# str(os.getlogin())  Тут мы получаем имя владельца Компьютера
username =str("Oleg Zubak") 
user = str(username)  # укажите имя пользователя
# m3=str(" m3")
# mt=str(" mt")

class App(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title(name_off_app)
        self.master.maxsize(1200,800)
        self.master.minsize(1000,600)

        # self.master.geometry('500x300')
        self.grid(ipadx=1, ipady=1, rowspan=5, columnspan=5)

        self.create_widgets()
    

    #### Start to create Frame widgets and some main buttons
    def create_widgets(self):
        
        # self.start_time = datetime.now()
        
        '''Create all Frames, footer and Menu'''
        padding = {'padx':5, 'pady':2}
        self.padding2 = { 'padx': 20, 'pady':2}
        self.padding3 = { 'padx': 20, 'pady':2}
        self.frame0 = ttk.Frame()
        self.frame1 = ttk.Frame()
        self.frame2 = ttk.Frame()
        self.frame3 = ttk.Frame()
        self.frame4 = ttk.Frame()
        self.frame5 = ttk.Frame()
        self.frame6 = ttk.Frame()
        self.frame7 = ttk.Frame()

        self.frame0.grid(columnspan=20,ipadx=10, ipady=1)
        self.frame1.grid(columnspan=20,ipadx=10, ipady=1)
        self.frame2.grid(columnspan=20,ipadx=10, ipady=1)
        self.frame3.grid(columnspan=20,ipadx=10, ipady=1)
        self.frame4.grid(columnspan=20,ipadx=10, ipady=1)
        self.frame5.grid(columnspan=20,ipadx=10, ipady=1)
        self.frame6.grid(columnspan=20,ipadx=10, ipady=1)
        self.frame7.grid(columnspan=20,ipadx=10, ipady=1)

        ## Initial state of MDO section
        # 1 means that MDO section is True(shown)
        self.mdo_state=IntVar()
        self.mdo_state.set(1)

        self.global_iterator = 0
        self.iterator_for_license = 0
        self.go_back_indicator = IntVar()
        self.go_back_indicator.set(0)
        
        self.return_var = StringVar()
        self.return_var.set("Admin Panel")
        ## Menu section ##

        menubar=Menu(self.master)
        self.master.config(menu=menubar)
        self.emenubar=Menu(menubar, tearoff = 0)

        self.emenubar.add_separator()
        menubar.add_cascade(label="App", menu=self.emenubar)
        
        self.emenubar.add_command(label=str(self.return_var.get()), command=self.admin_thread,
                )
        self.emenubar.add_command(label= "Return Prev", command=self.insert_previous_func,
                )
        submenu=Menu(self.emenubar, tearoff = 0)
        submenu.add_checkbutton(label="Add MDO",
            variable=self.mdo_state,
            command=(lambda:self.cb())
            )
        self.emenubar.add_cascade(label="MDO", menu=submenu)
        
        
        print_menu=Menu(menubar, tearoff = 0)
        print_menu.add_command(label="Print", command=self.print_window)
        menubar.add_cascade(label="Print", menu=print_menu)

        help_menu=Menu(menubar, tearoff = 0)
        help_menu.add_command(label="Manual", command=self.manual_page)
        help_menu.add_command(label="About", command=self.help_about)
        help_menu.add_command(label="License", command=self.license_show)
        menubar.add_cascade(label="Help", menu=help_menu)

        exit_menu=Menu(menubar, tearoff = 0)
        exit_menu.add_command(label="Restart", command=self.restart)
        exit_menu.add_command(label="Quit", command=self.master.quit)
        menubar.add_cascade(label="Exit", menu=exit_menu)

        ## footer

        self.footer_text = Label(
            self.master, text="Created by " +
            user + str(" on \"") +
            str(operation_platform) +
            '" OS',
            font=('Sans-serif', 9), pady=25 
            )

        self.footer_text.grid(
            column=10,
            sticky=S
            )
        self.sounding_All_vars=[]
        self.temperature_All_vars=[]
        self.result_All_vars=[]
        
        self.satrt_build_interface()

    ### Build interface  ###

    def satrt_build_interface(self):
        
        self.total_widget_Lbl_dict = dict()
        self.total_widget_Lbl_dict_num = dict()
        self.difference_Btn_dict = dict()
        self.difference_Lbl_dict = dict()
        self.difference_Lbl_dict_var = dict()
        self.by_log_Entry_dict = dict()
        
        
        
        
        
        self.calc_Btn_dict = dict()
        self.footer_text.grid()
        insert_in_db.sort_tanks_mdo()
        insert_in_db.sort_tanks()
        
        self.table_DB=[]
        self.table_items=insert_in_db.table_names
        
        for i in self.table_items:
            i=str(i)
            self.tables_in_DB=i.strip('(),\'')
            self.table_DB.append(self.tables_in_DB)

        self.mdo=[]
        self.table_items2=insert_in_db.table_names_md

        for i in self.table_items2:
            i=str(i)
            self.tables_in_DB_mdo=i.strip('(),\'')
            self.mdo.append(self.tables_in_DB_mdo)

        self.hfo_section=Label(self.frame0, text="HFO Tanks",
        font=('Sans-serif', 8, UNDERLINE), pady=4
        )
        self.hfo_section.grid(row = 0, column=0,
        columnspan=20)

        self.hfo_tanks(self.table_DB, self.frame0)

        self.mdo_section=Label(self.frame5, text="MDO Tanks",
            font=('Sans-serif', 8, UNDERLINE), pady=4
            )
        self.mdo_section.grid(row=0, column=0,
            columnspan=20)

        if self.mdo_state.get() != 0:
            self.cb()

    def hfo_tanks(self, tk_list, frame):  ### Start to build structure of the app

        j=0 # iterator to calculate how many rows need to create

        all_tanks=list(tk_list)

        self.name_reference_point=(len(all_tanks))
        self.names_of_tank=[]
        self.sounding_lbl=StringVar()
        self.labelWidgets_Name=[]

        self.labelWidgets_tankLabel=[]

        self.sounding_var_Dict={}
        self.labelWidgets_soundLabel=[]
        self.entryWidgets_entered_suond={}

        self.labelWidgets_volumeLabel=[]
        self.labelWidgets_volumeResult={}

        self.temperature_var={}
        self.labelWidgets_Temp=[]
        self.entryWidgets_Temp={}
        
        self.string_for_label={}
        self.labelWidgets_DefDens=[]
        self.labelWidgets_DefDens_num={}
        
        self.string_for_NewDens={}
        self.labelWidgets_Dens=[]
        self.entryWidgets_Dens_num={}

        self.result_textvar_Dict={}
        self.labelWidgets_ResultMT=[]
        self.labelWidgets_ResultMT_num={}

        self.Widgets_Button=[]
        self.button_Widget_number={}

        ########################################
        # Initialize the labales for head rows #
        ########################################

        self.labelWidgets_tankLabel.append(Label
            (frame, **self.padding3, text="Tank",
            bg="#ccc", relief="ridge", borderwidth=2,
            font=('Sans-serif', 8))
            )

        self.labelWidgets_soundLabel.append(Label
            (frame, **self.padding3, text="Sounding in cm",
            bg="#ccc", relief="ridge", borderwidth=2,
            font=('Sans-serif', 8))
            )
        

        self.labelWidgets_volumeLabel.append(Label
            (frame, **self.padding3, text="Volume in m3", width=12,
            bg="#ccc", relief="ridge", borderwidth=2,
            font=('Sans-serif', 8))
            )

        self.labelWidgets_Temp.append(Label
            (frame, **self.padding3, text="Temp", bg="#ccc", relief="ridge", borderwidth=2,
            font=('Sans-serif', 8))
            )

        self.labelWidgets_DefDens.append(Label
            (frame,  **self.padding3, bg="#ccc", text="Density", relief="ridge",
            borderwidth=2,
            font=('Sans-serif', 8))
            )

        self.labelWidgets_Dens.append(Label
            (frame, **self.padding3, text="New Dens", bg="#ccc", relief="ridge",
            borderwidth=2,
            font=('Sans-serif', 8))
            )

        self.labelWidgets_ResultMT.append(Label
            (frame, **self.padding3, width=12, text="Result MT", bg="#ccc",
            relief="ridge", borderwidth=2,
            font=('Sans-serif', 8))
            )

        self.labelWidgets_tankLabel[-1].grid(row=1, column=0, padx=1)

        self.labelWidgets_soundLabel[-1].grid(row=1, column=1, padx=1)
        
        self.labelWidgets_volumeLabel[-1].grid(row=1 , column=2, padx=1)

        self.labelWidgets_Temp[-1].grid(row=1, column=3, padx=1)

        self.labelWidgets_DefDens[-1].grid(row =1, column = 4, padx =1)
        
        self.labelWidgets_Dens[-1].grid(row=1, column=5, padx =1)
        
        self.labelWidgets_ResultMT[-1].grid(row=1, column=6, padx =1)

        ##################################################
        # end block Initialize the labales for head rows #
        ##################################################

        for index , names in enumerate(all_tanks):

            self.table_name_var=StringVar()
            self.table_name_var.set(names)
            self.sounding_lbl.set(names)
            self.names_of_tank.append(self.sounding_lbl.get())


            self.labelWidgets_Name.append(Label(frame,
            textvariable=self.table_name_var, **self.padding2,
            font=('Sans-serif', 8))
            )

            self.sounding_var=StringVar()
            self.sounding_var_Dict[names]=self.sounding_var
            self.entryWidgets_entered_suond[names]=Entry(frame,
            width=10, relief="ridge", borderwidth=2, textvariable=self.sounding_var,
            justify="center",
            font=('Sans-serif', 8)
            )

            db_commands_calc.calculation(self.table_name_var.get(),self.entryWidgets_entered_suond[names])

            self.labelWidgets_volumeResult[names]=Label(frame,
            **self.padding3, width=10, relief="ridge", borderwidth=2,
            font=('Sans-serif', 8)
            )

            self.temperature_variable=StringVar()
            self.temperature_var[names]=self.temperature_variable
            self.entryWidgets_Temp[names]=Entry(
                frame, width=8, textvariable=self.temperature_variable,
                borderwidth=2, relief="ridge",
                justify="center",
                fg="black"
                )

            db_commands_calc.select_DefDens(self.table_name_var.get())
            self.def_density_var=StringVar()
            self.def_density_var.set(str(db_commands_calc.density))
            self.string_for_label[names]=self.def_density_var
            self.labelWidgets_DefDens_num[names]=(Label
            (frame, **self.padding3, width=6, textvariable=self.def_density_var,
            relief="ridge", borderwidth=2,
            font=('Sans-serif', 8))
            )
            
            
            self.new_dens_txt_var=StringVar()
            self.string_for_NewDens[names]=self.new_dens_txt_var
            self.entryWidgets_Dens_num[names]=Entry(
                frame, fg="#00cc00",
                width=8, relief="ridge",
                borderwidth=2, font=('Sans-serif', 8),
                textvariable=self.new_dens_txt_var,
                takefocus=0, justify="center"
                )

            self.result_textvar=StringVar()
            self.result_textvar_Dict[names]=self.result_textvar
            self.labelWidgets_ResultMT_num[names]=(Label(
                frame, **self.padding3, fg="blue",
                bg="#c2ccff", width=8, textvariable=self.result_textvar,
                relief="ridge", borderwidth=2,font=('Sans-serif', 8))
                )

            for items in range(len(all_tanks)) :

                self.padx_for_lbl=2
                # if want to change the position for Name of tank
                # can change the value of "tank_name_row" and 
                # "self.tank_name_column" column parameter
                if self.name_reference_point != 2:
                    self.tank_name_row=int(j+3)
                    self.tank_name_column=0
                else:
                    self.tank_name_column=3
                    self.tank_name_row=int(j+1)
                self.lbl_row=int(j+2)
                self.entry_row=int(j+3)

                self.labelWidgets_Name[-1].grid(row=self.tank_name_row, column=self.tank_name_column)

                self.entryWidgets_entered_suond[names].grid(row=self.entry_row, column=1, padx=self.padx_for_lbl)

                self.labelWidgets_volumeResult[names].grid(row=self.entry_row, column=2, padx=self.padx_for_lbl)

                self.entryWidgets_Temp[names].grid(row=self.entry_row, column=3, padx=self.padx_for_lbl)

                self.labelWidgets_DefDens_num[names].grid(row=self.entry_row, column=4, padx =self.padx_for_lbl)

                self.entryWidgets_Dens_num[names].grid(row=self.entry_row, column=5, padx =self.padx_for_lbl)

                self.labelWidgets_ResultMT_num[names].grid(row=self.entry_row, column=6, padx =self.padx_for_lbl)


                j += 1

        
        self.calculate_Button = Button(
            frame, bg='green',  text="Calculate",
            relief="ridge",activebackground='#aa3666',
            command=lambda:self.calculate(
                self.hfo_data_sound,
                self.hfo_data_vol_result, self.hfo_data_temp,
                self.hfo_data_def_dens, self.hfo_data_new_dens,
                self.hfo_data_result_num,
                frame, self.change_sound_hfo,
                self.string_variable_hfo,
                self.new_dens_var_hfo,
                self.result_textvar_hfo,
                frame
            ),
            **self.padding3)
        self.calculate_Button.grid(row=1, column=7)

        self.hfo_data_sound=self.entryWidgets_entered_suond
        self.hfo_data_vol_result=self.labelWidgets_volumeResult
        self.hfo_data_temp=self.entryWidgets_Temp
        self.hfo_data_def_dens=self.labelWidgets_DefDens_num
        self.hfo_data_new_dens=self.entryWidgets_Dens_num
        self.hfo_data_result_num=self.labelWidgets_ResultMT_num
        self.change_sound_hfo=self.entryWidgets_entered_suond
        self.string_variable_hfo=self.string_for_label
        self.new_dens_var_hfo=self.string_for_NewDens
        self.result_textvar_hfo=self.result_textvar_Dict

        self.sounding_All_vars.append(self.sounding_var_Dict)
        self.temperature_All_vars.append(self.temperature_var)
        self.result_All_vars.append(self.result_textvar_Dict)
        self.calc_Btn_dict[frame]=self.calculate_Button
        
        
    def mdo_tanks(self, tk_list, frame):  ### Start to build structure of the app

        j=0

        all_tanks=list(tk_list)

        self.name_reference_point=(len(all_tanks))
        self.names_of_tank=[]
        self.sounding_lbl=StringVar()
        self.labelWidgets_Name=[]

        self.labelWidgets_tankLabel=[]

        self.sounding_var_Dict={}
        self.labelWidgets_soundLabel=[]
        self.entryWidgets_entered_suond={}

        self.labelWidgets_volumeLabel=[]
        self.labelWidgets_volumeResult={}

        self.temperature_var={}
        self.labelWidgets_Temp=[]
        self.entryWidgets_Temp={}
        
        self.string_for_label={}
        self.labelWidgets_DefDens=[]
        self.labelWidgets_DefDens_num={}
        
        self.string_for_NewDens={}
        self.labelWidgets_Dens=[]
        self.entryWidgets_Dens_num={}

        self.result_textvar_Dict={}
        self.labelWidgets_ResultMT=[]
        self.labelWidgets_ResultMT_num={}

        self.Widgets_Button=[]
        self.button_Widget_number={}

        ########################################
        # Initialize the labales for head rows #
        ########################################

        self.labelWidgets_tankLabel.append(Label
            (frame, **self.padding3, text="Tank",
            bg="#ccc", relief="ridge", borderwidth=2,
            font=('Sans-serif', 8))
            )


        self.labelWidgets_soundLabel.append(Label
            (frame, **self.padding3, text="Sounding in cm",
            bg="#ccc", relief="ridge", borderwidth=2,
            font=('Sans-serif', 8))
            )

        self.labelWidgets_volumeLabel.append(Label
            (frame, **self.padding3, text="Volume in m3", width=12,
            bg="#ccc", relief="ridge", borderwidth=2,
            font=('Sans-serif', 8))
            )

        self.labelWidgets_Temp.append(Label
            (frame, **self.padding3, text="Temp", bg="#ccc", relief="ridge", borderwidth=2,
            font=('Sans-serif', 8))
            )

        self.labelWidgets_DefDens.append(Label
            (frame,  **self.padding3, bg="#ccc", text="Dendsity", relief="ridge",
            borderwidth=2,
            font=('Sans-serif', 8))
            )

        self.labelWidgets_Dens.append(Label
            (frame, **self.padding3, text="New Dens", bg="#ccc", relief="ridge",
            borderwidth=2,
            font=('Sans-serif', 8))
            )

        self.labelWidgets_ResultMT.append(Label
            (frame, **self.padding3, width=12, text="Result MT", bg="#ccc",
            relief="ridge", borderwidth=2,
            font=('Sans-serif', 8))
            )

        self.labelWidgets_tankLabel[-1].grid(row=1, column=0, padx=1)

        self.labelWidgets_soundLabel[-1].grid(row=1, column=1, padx=1)

        self.labelWidgets_volumeLabel[-1].grid(row=1 , column=2, padx=1)

        self.labelWidgets_Temp[-1].grid(row=1, column=3, padx=1)

        self.labelWidgets_DefDens[-1].grid(row =1, column = 4, padx =1)

        self.labelWidgets_Dens[-1].grid(row=1, column=5, padx =1)

        self.labelWidgets_ResultMT[-1].grid(row=1, column=6, padx =1)

        ##################################################
        # end block Initialize the labales for head rows #
        ##################################################

        for index, names in enumerate(all_tanks):

            self.table_name_var=StringVar()
            self.table_name_var.set(names)
            self.sounding_lbl.set(names)
            self.names_of_tank.append(self.sounding_lbl.get())

            self.labelWidgets_Name.append(Label(frame,
            textvariable=self.table_name_var, **self.padding2, width =10,
            font=('Sans-serif', 8))
            )

            self.sounding_var=StringVar()
            self.sounding_var_Dict[names]=self.sounding_var
            self.entryWidgets_entered_suond[names]=Entry(frame,
            width=10, relief="ridge", borderwidth=2, textvariable=self.sounding_var,
            justify="center",
            font=('Sans-serif', 8)
            )

            db_commands_calc.calculation(self.table_name_var.get(),self.entryWidgets_entered_suond[names])

            self.labelWidgets_volumeResult[names]=Label(frame,
            **self.padding3, width=10, relief="ridge", borderwidth=2,
            font=('Sans-serif', 8)
            )

            self.temperature_variable=StringVar()
            self.temperature_var[names]=self.temperature_variable
            self.entryWidgets_Temp[names]=Entry(
                frame, width=8, textvariable=self.temperature_variable,
                borderwidth=2, relief="ridge", justify="center",
                fg="black"
                )

            db_commands_calc.select_DefDens(self.table_name_var.get())
            self.def_density_var=StringVar()
            self.def_density_var.set(str(db_commands_calc.density))
            
            self.string_for_label[names]=self.def_density_var
            
            self.labelWidgets_DefDens_num[names]=(Label
            (frame, **self.padding3, width=6, textvariable=self.def_density_var,
            relief="ridge", borderwidth=2,
            font=('Sans-serif', 8))
            )

            self.new_dens_txt_var=StringVar()
            self.string_for_NewDens[names]=self.new_dens_txt_var
            self.entryWidgets_Dens_num[names]=Entry(
                frame, fg="#00cc00",
                width=8, relief="ridge",
                borderwidth=2, font=('Sans-serif', 8),
                textvariable=self.new_dens_txt_var,
                takefocus=0, justify="center"
                )

            self.result_textvar=StringVar()
            self.result_textvar_Dict[names]=self.result_textvar
            self.labelWidgets_ResultMT_num[names]=(Label(
                frame, **self.padding3, fg="blue",
                bg="#c2ccff", width=8, textvariable=self.result_textvar,
                relief="ridge", borderwidth=2,font=('Sans-serif', 8))
                )

            for items in range(len(all_tanks)) :

                self.padx_for_lbl=2
                # if want to change the position for Name of tank
                # can change the value of "tank_name_row" and 
                # "self.tank_name_column" column parameter
                if self.name_reference_point != 2:
                    self.tank_name_row=int(j+3)
                    self.tank_name_column=0
                else:
                    self.tank_name_column=3
                    self.tank_name_row=int(j+1)
                self.lbl_row=int(j+2)
                self.entry_row=int(j+3)

                self.labelWidgets_Name[-1].grid(row=self.tank_name_row, column=self.tank_name_column)

                self.entryWidgets_entered_suond[names].grid(row=self.entry_row, column=1, padx=self.padx_for_lbl)

                self.labelWidgets_volumeResult[names].grid(row=self.entry_row, column=2, padx=self.padx_for_lbl)

                self.entryWidgets_Temp[names].grid(row=self.entry_row, column=3, padx=self.padx_for_lbl)

                self.labelWidgets_DefDens_num[names].grid(row=self.entry_row, column=4, padx =self.padx_for_lbl)

                self.entryWidgets_Dens_num[names].grid(row=self.entry_row, column=5, padx =self.padx_for_lbl)

                self.labelWidgets_ResultMT_num[names].grid(row=self.entry_row, column=6, padx =self.padx_for_lbl)

                j += 1
        
        
        self.calculate_Button=Button(
        frame, bg='green',  text="Calculate",
        relief="ridge",
        activebackground='#aa3666', command=lambda:self.calculate(self.mdo_data_sound,
        self.mdo_data_vol_result, self.mdo_data_temp,
        self.mdo_data_def_dens, self.mdo_data_new_dens,
        self.mdo_data_result_num,
        frame, self.change_sound_mdo,
        self.string_variable_mdo,
        self.new_dens_var_mdo,
        self.result_textvar_mdo,
        frame
        ),
        **self.padding3
        )
        self.calculate_Button.grid(row=1, column=7)

        self.mdo_data_sound=self.entryWidgets_entered_suond
        self.mdo_data_vol_result=self.labelWidgets_volumeResult
        self.mdo_data_temp=self.entryWidgets_Temp
        self.mdo_data_def_dens=self.labelWidgets_DefDens_num
        self.mdo_data_new_dens=self.entryWidgets_Dens_num
        self.mdo_data_result_num=self.labelWidgets_ResultMT_num
        self.change_sound_mdo=self.entryWidgets_entered_suond
        self.string_variable_mdo=self.string_for_label
        self.new_dens_var_mdo=self.string_for_NewDens
        self.result_textvar_mdo=self.result_textvar_Dict
        self.temp_variable_mdo=self.temperature_var

        self.sounding_All_vars.append(self.sounding_var_Dict)
        self.temperature_All_vars.append(self.temperature_var)
        self.result_All_vars.append(self.result_textvar_Dict)
        self.calc_Btn_dict[frame]=self.calculate_Button
        
    def insert_previous_func(self):
        """
        Method for insert data from previous db into our Table
        """
        
        #sounding entry
        dict_for_insert_sounding={}
        for r, j in enumerate(self.sounding_All_vars):
            
            for ind, value in j.items():
                dict_for_insert_sounding[ind]=value
        
        # temperature entry
        dict_for_insert_temperature={}
        for r, j in enumerate(self.temperature_All_vars):
            
            for ind, value in j.items():
                dict_for_insert_temperature[ind]=value
        
        # result label
        dict_for_insert_results={}
        for r, j in enumerate(self.result_All_vars):
            
            for ind, value in j.items():
                dict_for_insert_results[ind]=value
                
        
        
        prev_measurments.all_tanks_name()
        
        for names in prev_measurments.name_of_all_tanks:
            prev_measurments.extract_from_prev_db(names)
            dict_for_insert_sounding[names].set(prev_measurments.sound_insert)
            dict_for_insert_temperature[names].set(prev_measurments.temperature_insert)
            dict_for_insert_results[names].set(prev_measurments.result_insert)

        
    def calculate(self, data, vol_res, temperature, def_dens, new_dens, result_num, frame, change_sound, var, new_var, result_txt, fr):
        
        # print all data for insertion into previous measurements
        # database
        def print_all():
            
            x_thread = threading.Thread(target=insert_thread, daemon=True)
            x_thread.start()

            if x_thread.is_alive() == True:
                self.calc_Btn_dict[fr]['state'] = NORMAL
                
                
            else:
                print(str(x_thread) + str("Error"))
                self.calc_Btn_dict[fr]['state'] = NORMAL
                
                
        def insert_thread():
            
            self.topwindow = Toplevel()
            self.topwindow.grid()
            progress_bar()    
            for tank_names, values_sound in data.items():
                
                # print("###########" + str(tank_names) + "############")
                # print(str(self.sound[tank_names]) + " = sound_data")
                # print(str(self.vol_insert_to_Lbl[tank_names]) + "= val_of_entry")
                # print(str(self.temp[tank_names]) + " = temperature")
                # print(str(self.def_dens[tank_names]) + " = default density")
                # print(str(var[tank_names].get()) + " = New density")
                # print(str(result_num[tank_names]["text"]) + " = Result")
                # print("\n")
                
                name_of_tank = tank_names
                
                sound_data = str(self.sound[tank_names])
                
                volume_to_insert = str(self.vol_insert_to_Lbl[tank_names])
                
                temperature_to_insert = str(self.temp[tank_names])
                
                dens_to_insert = str(var[tank_names].get())
                
                result_to_insert = str(result_num[tank_names]["text"])


                prev_measurments.create_tk(name_of_tank,
                        sound_data, volume_to_insert,
                        temperature_to_insert, dens_to_insert,
                        result_to_insert)
                
                for i, v in self.calc_Btn_dict.items():

                    v['state'] = DISABLED
                    v['bg'] = '#cc0cc00cc'
            
            change_Btn_state()
            
        def progress_bar():

            try:
                self.info_label=Label(self.topwindow,
                    text="Calculation ...\n")
                self.info_label.grid(row=0, padx=40)
                self.progress = ttk.Progressbar(self.topwindow, orient=HORIZONTAL,
                    length=300, mode='indeterminate')
                self.progress.grid(row=1, columnspan=20, padx=40)
                self.progress.start()
                    
            except Exception as e:
                print(str(e))            
                
            
        
        def change_Btn_state():
            for i, v in self.calc_Btn_dict.items():
                self.progress.stop()
                v['state'] = NORMAL
                v['bg'] = 'green'
                print("################################")
                print("Button state in ", str(fr), " was changed succesefully")
            self.topwindow.destroy()
              

        def result_in_MT(data):
            # delete the text from the new dens Entry
            for tank, val_of_entry in new_var.items(): 
                val_of_entry.set("")
               
            # Insert the extracted volume into the lbl
            self.result_insert_to_Lbl={}
            for key, value in zip(data.items(), self.res):
                    key=key[0]
                    self.result_insert_to_Lbl[key]=value

            for key1, value1 in self.result_insert_to_Lbl.items():        
                result_txt[key1].set(str(value1)+str(" mt"))

            for name_tk, values in var.items():
                db_commands_calc.select_DefDens(name_tk)
                values.set(db_commands_calc.density)

            print_all()

            if self.real_vol:
                self.total_widget(frame)
                
            else:
                print("NO function self.real_vol")

        def vol_correction_factor_calc(conv_dens, volume_value, temp):
            try:
                if float(conv_dens) <= 771 :
                    self.b=346.4228
                else:
                    if float(conv_dens) <= 787:
                        self.b=2680.3206
                    else:
                        if float(conv_dens) <= 838.5:
                            self.b=594.5418
                        else:
                            if float(conv_dens) <=1075:
                                self.b=186.9696
                            else:
                                pass
                                #need to make here an allert message
                if float(conv_dens) <= 771 :
                    self.c=0.4388
                else:
                    if float(conv_dens) <= 787 :
                        self.c=-0.00336312
                    else:
                        if float(conv_dens) <= 838.5 :
                            self.c=0
                        else:
                            if float(conv_dens) <= 1075 :
                                self.c=0.4862
                            else:
                                pass
                                #need to make an allert message
                if self.c >= 0 :
                    self.d=((self.b)/conv_dens**2)+(self.c/conv_dens)
                    self.d=round(self.d,7)
                else:
                    self.d=(self.b/(conv_dens**2))+self.c

                # Volume correction factor formula

                if volume_value == 0 :
                    self.temp_cor_factor=round(
                        math.exp(
                            (-self.d*int((int(temp)*4+0.5)/4-15)*(1+0.8*float(self.d)*int((int(temp)*4+0.5)/4-15)))), 4
                            )
                else:
                    try:
                        if -1 <  float(temp) < 150:
                            try:
                                self.temp_cor_factor=round(
                                    math.exp(
                                        (-self.d*int((int(temp)*4+0.5)/4-15)*(1+0.8*float(self.d)*int((int(temp)*4+0.5)/4-15)))), 4
                                        )

                            except ValueError:

                                # self.show_error=showinfo(
                                #     "Error", message=str(
                                #     "Введите правильно температуру или посчитает при : \n + 15 С\n"
                                #     ))
                                temp=15
                                self.temp_cor_factor=round(
                                    math.exp(
                                        (-self.d*int((int(temp)*4+0.5)/4-15)*(1+0.8*float(self.d)*int((int(temp)*4+0.5)/4-15)))), 4
                                        )
                        else:

                            temp=15
                            # self.show_error=showinfo(
                            #         "Error", message=str(
                            #         "Температура слишком низкая или слишком высокая \n"))

                    except ValueError:

                        temp=15

                        self.temp_cor_factor=round(
                            math.exp(
                                (-self.d*int((int(temp)*4+0.5)/4-15)*(1+0.8*float(self.d)*int((int(temp)*4+0.5)/4-15)))), 4
                                )
                        
                # Weight factor
                self.weight_cor_factor=float(conv_dens/1000-0.0011)

                # real volume is calculating:
                self.q=float(volume_value)*float(self.temp_cor_factor)
                self.real_vol=str(round((self.q*self.weight_cor_factor),2))
                self.res.append(self.real_vol)

            except Exception as e:

                print(str("Error in string No 687: ")+str(e))

        def volume_by_density(data):

            self.volume_density=[]
            self.convert_density=[]
            self.res=[] # Create an empty list for append calculated results

            for volume_value, dens in zip(self.vol.items(), self.new_dens.items()):
                volume_value=(volume_value[1])
                db_commands_calc.select_DefDens(dens[0])
                dens=(db_commands_calc.density)

                try:

                    volume_density=float(volume_value)*float(dens)
                    self.volume_density.append(volume_density)
                    convert_density=((float(dens)/2)*1000)*2
                    self.convert_density.append(convert_density)

                except ValueError as e:

                    self.show_error=showerror(
                    "Error", message=str("Error in sounding value \n"))

            for conv_dens, volume_value, temp in zip(self.convert_density, self.vol.items(), self.temp.items()):
                vol_correction_factor_calc(conv_dens,volume_value[1],temp[1])

            result_in_MT(self.vol)

        ## The calculation and gathering of information is started Below
        self.name=[]
        self.type=dict()
        self.sound=dict()
        self.vol=dict()
        self.vol_insert_to_Lbl=dict()
        self.temp=dict()
        self.def_dens=dict()
        self.new_dens=dict()
        self.updated_dens=dict()
        # Extract value of sound

        for key, value in data.items():
            if value.get() !='':
                try:
                    self.sound_value=float(value.get())

                    # self.sound.append(self.sound_value)
                    self.sound[key]=(self.sound_value)
                    self.name.append(key)
                    type_calc.check_tk_type(key)
                    self.type[key]=type_calc.type_dict[1]
                except ValueError:
                    
                    pass

            else:
                self.sound[key]=0

        # Extarct the value of volume for the given sounding value

        for i, d in self.sound.items():
            try:
                if self.type[i] == 1:
                    try:
                        self.vol[i]=d
                    except KeyError:
                        self.vol[i]=0
                else:
                    try:
                        db_commands_calc.calculation(i,d)
                        data1=(db_commands_calc.volume_in_m3)
                        data1=str(data1).strip('\'[]')
                        data1=float(data1)
                        self.vol[i]=data1

                    except ValueError:

                        self.vol[i]=("<--- check")

                    except TypeError:
                        pass

                    except IndexError:
                        pass
            except KeyError:
                self.vol[i]=0

        # Insert the extracted volume into the lbl
 
        self.vol_insert_to_Lbl={}

        for num, f in vol_res.items() :

            try:
                    self.vol_insert_to_Lbl[num]=self.vol[num]
                    f['bg']="#cccec9"

            except ValueError:
                print("Value")

            except TypeError:
                print("Type")

            except IndexError:

                for num, f in vol_res.items() :
                    f['bg']="red"

            for a, s in self.vol_insert_to_Lbl.items():

                f['text']=s

        # Extract value of the temperature
        for key, value in temperature.items():
            self.temperature=value.get()
            if self.temperature == '':
                self.temperature=15
            self.temp[key]=(self.temperature)
            
        # Extract value of new density if it not corresponds to default
        # and also if was entered new dedsity we hide the lbl widget of 
        # default density
        for j, d in new_dens.items():

            new_density=d.get()

            if new_density != '':
                try:
                    if  0 < float(new_density) < 1.0760:

                        self.show_info=askokcancel(
                                "Wait until Database will be filled",
                                message=str("Change density \n"+
                                "for tank: " + str(j)+
                                " to " + str(new_density)
                                )
                                )
                        if self.show_info == True:

                            try:
                                db_commands_calc.def_dens_modify(j, new_density)
                                conn.close()
                            except Exception as e:
                                print(f"Erorr: {e}" )
                            self.new_dens[j]=new_density
                            

                        else:
                            try:
                                self.new_dens[j]=j['text']
                            except Exception as e:
                                print(f"Erorr: {e}" )
                    else:
                        self.show_error=showerror("Wrong Entry of Density",
                        message="Please check value for Density"
                        )
                except Exception as e:
                    print(f'Error in Density: {e}')

            else:

                try:

                    for key, value in def_dens.items():

                        self.def_dens[key]=value['text']
                            
                        self.new_dens[key]=self.def_dens[key]

                        
                except Exception as e:

                    self.show_error=showerror(
                        "Error",
                        message=str("Wrong density, recheck\n"+str(e))
                        )
                    
        # go to  function were will calculate all inputed data in 
        # the Entry widgets upper^
        volume_by_density(data)
        
            
    def total_widget(self, frame):


        
        self.lbl_row=(len(self.table_DB)**2)+1
        try:
            
            def calc_diff(frame):
                try:
                    actual = (self.total_widget_Lbl_dict_num[frame]['text'])
                    by_log = float(self.by_log_Entry_dict[frame].get())
                    print(actual,"-",by_log)
                    diff = float(actual-by_log)
                    diff = (round(diff,4))
                    self.difference_Lbl_dict_var[frame].set(diff)
                except KeyError:
                    if str(frame) == ".!frame6" :
                        actual = (self.total_widget_Lbl_dict_num['.!frame6']['text'])
                        by_log = float(self.by_log_Entry_dict['.!frame6'].get())
                        print(actual,"-",by_log)
                        diff = float(actual-by_log)
                        diff = (round(diff,4))
                        self.difference_Lbl_dict_var['.!frame6'].set(diff)
                    elif str(frame) == ".!frame":
                        actual = (self.total_widget_Lbl_dict_num['.!frame6']['text'])
                        by_log = float(self.by_log_Entry_dict['.!frame6'].get())
                        print(actual,"-",by_log)
                        diff = float(actual-by_log)
                        diff = (round(diff,4))
                        self.difference_Lbl_dict_var['.!frame6'].set(diff)
                    else:
                        if str(frame) == ".!frame6":
                            print(str(frame))
                        elif str(frame) == ".!frame":
                            print(str(frame))
                        else:    
                            print("Error: Unknown frame")    
            
            result=[]

            self.total_widget_Lbl_dict[frame] = Label(frame, text="Total in mt",
            width=10, **self.padding2, borderwidth = 2, relief="ridge"
            )
            self.total_widget_Lbl_dict[frame].grid(row = self.lbl_row+2, column = 6, pady =2)
            
            
            self.total_widget_Lbl_dict_num[frame] = Label(frame,
            width = 10, **self.padding2, borderwidth = 2, relief = "ridge",
            bg = "#c6c5c7"
            )
            self.total_widget_Lbl_dict_num[frame].grid(row=self.lbl_row+3, column=6, pady =2)
            
            
            self.by_log_Label=Label(frame, text="By Log mt",
            width=10, **self.padding2, borderwidth = 2, relief="ridge"
            )
            self.by_log_Label.grid(row = self.lbl_row+2, column = 5, pady =2)
            
            
            # self.by_log_variable = IntVar()
            self.by_log_Entry_dict[frame] = Entry(frame,
                width=10, relief="ridge", borderwidth=2,
                    justify="center",
                    font=('Sans-serif', 8)
                                        )
            self.by_log_Entry_dict[frame].grid(row =self.lbl_row+3, column=5, pady=2)

            self.difference_var = IntVar()
            
            self.difference_Lbl_dict_var[frame] = self.difference_var
            
            self.difference_Lbl_dict[frame] = Label(frame, textvariable=self.difference_var,
                width=10, **self.padding2, borderwidth = 2, relief="ridge"
                )
            self.difference_Lbl_dict[frame].grid(row =self.lbl_row+3, column=7, pady=2)

            
            
            self.difference_Btn_dict[frame] = Button(
                frame, bg='green',  text="Diff",
                relief="ridge",
                activebackground='#aa3666', command = lambda:calc_diff(frame),
                **self.padding3
                )
            self.difference_Btn_dict[frame].grid(row =self.lbl_row+2, column=7, pady=2)

            for i, d in enumerate(self.res) :
                data = float(d)
                result.append(data)
            total_quantity = round(sum(result),3)
            self.total_widget_Lbl_dict_num[frame]['text'] = float(total_quantity)

        except Exception as e :
            self.show_error=showerror(
                "Error",
                message=str(str(e))
                )   

    def cb(self):
        """
        Action after click on cascade menu
        to show or hide the MDO section
        """

        if self.mdo_state.get() == 1:
            self.add_mdo_start() 

        else:
            self.remove_mdo()

    def add_mdo_start(self):

        insert_in_db.sort_tanks_mdo()
        self.mdo=[]
        self.t2=insert_in_db.table_names_md

        for i in self.t2:
            i=str(i)
            self.tables_in_DB_mdo=i.strip('(),\'')
            self.mdo.append(self.tables_in_DB_mdo)

        if self.global_iterator == 0:

            self.mdo_tanks(self.mdo, self.frame5)
            self.global_iterator +=1
        else:

            self.frame5.grid()
            self.footer_text.grid_forget()
            self.mdo_tanks(self.mdo, self.frame5)
            self.footer_text.grid()

    def remove_mdo(self):
        try:
            self.frame5.grid_forget()

        except Exception as e: 
            print(str(e))



    ### ADMIN PANEL  ###
    
    
    def admin_thread(self):
        if self.go_back_indicator.get() == 0:
            self.go_back_indicator.set(1)
            self.admin_panel_check()
            
        else:
            self.go_back_indicator.set(0)
            self.go_back()
           

    def go_back(self):
        self.frame0.grid()
        self.frame1.grid_forget()
        self.frame2.grid_forget()
        self.frame3.grid_forget()
        self.satrt_build_interface()

    def admin_panel_check(self):

        self.emenubar.grid_remove()
        self.footer_text.grid_forget()
        
        self.set_type_var=IntVar()
        self.set_type_txt=StringVar()
        self.set_type_txt.set("Type")
        
        self.set_tank_for_mdo=IntVar()
        self.set_mdo_tk_text=StringVar()
        self.set_mdo_tk_text.set("Set to ")
        
        def get_pass():

            try:
                self.password=str(self.password_entry.get())
                if self.password == "":
                    self.show_error=showerror(
                    "Error", message = "Empty password: \n"+ str(e))

                global apipass
                # homedir = str(Path.home())
                # gpg = gnupg.GPG(gnupghome=os.path.join(homedir,".gnupg"), use_agent=True)

                # with open(os.path.join(homedir,'Documents','myapp','passwd.gpg'), 'rb') as f:
                #     apipass = (gpg.decrypt_file(f, passphrase=self.password))

                # f.close()

                # return str(apipass)

                try:
                    if self.password == str(8050):
                        apipass=8050
                    return str(apipass)
                except Exception as e:
                    self.show_error=showerror("Error",
                        message = ("Wrong password \n"+ str(e)))

            except AttributeError as e:
                self.show_error=showerror(
                "Error", message = "Password is empty: \n"+ str(e))

        def click():
            try:
                get_pass()

                if str(apipass) == str(self.password):
                    self.frame4.grid_forget()
                    self.admin_panel()
                else:
                    self.show_error=showerror(
                    "Error", message=str("Wrong password\n")
                    )
            except NameError as e:
                print(str(e))

        self.frame0.grid_forget()
        self.frame5.grid_forget()
        self.frame1.grid()
        self.footer_text.grid()
        self.password_entry = Entry(self.frame4, width = 10)
        self.password_entry.config(show = "*")
        self.password_entry.focus_set()
        self.password_entry.bind(
                '<Return>', lambda event, f="click()":click()
        )
        self.password_entry.bind(
                '<KP_Enter>', lambda event, f="click()":click()
        )
        self.password_entry.grid(row = 0, column = 0)

        enter_password = Button(self.frame4,
            text = "Submit", command = click,
            bg = "blue"
            )
        enter_password.bind(
                '<Return>', lambda event, f="click()":click()
        )

        
        enter_password.grid(row = 0, column = 1)

    def admin_panel(self):
        i=[]
        insert_in_db.admin_start()

        self.list_db=Listbox(self.frame1, selectmode=SINGLE,
                            borderwidth=4,
                            width=25
                            )
        for data in insert_in_db.name_of_tank:
            self.list_db.insert(END, data)
            i.append(data)
        self.list_db["height"]=int(len(i))
        self.list_db.grid(row=1, column=0, columnspan=10)

        self.tables_tuple=list(i)

        self.chapter_text_var=StringVar()
        self.chapter_text_var.set("ADMIN Panel \n"+
        "Choose what to do: create new Tank or add colum, or insert \n"+
        "new values in DB table:")
        self.chapter_name_lbl=Label(self.frame1,
            textvariable=self.chapter_text_var,
            fg="blue", font=('Sans-serif', 15))
        self.chapter_name_lbl.grid(row=0, column=0, columnspan=10)

        ## add buttons and labeles for editing DB
        self.add_tk=Button(self.frame1,
        text="Add new Tank", command=lambda: self.edit_db(1),
        bg="green"
        )
        self.add_col=Button(self.frame1,
        text="Add new Column", command=lambda: self.edit_db(2),
        bg="blue"
        )
        self.edit_tk=Button(self.frame1,
        text="Edit Tank", command=lambda: self.edit_db(3),
        bg="yellow"
        )
        self.delete_tk=Button(self.frame1,
        text="Delete Tank", command=lambda: self.edit_db(4),
        bg="red"
        )

        self.add_tk.grid(row=2, column=0)
        self.add_col.grid(row=2, column=1)
        self.edit_tk.grid(row=2,column=2)
        self.delete_tk.grid(row=2, column=3)

    def edit_db(self, arg):

        if arg == 1:  # Add new tank
            self.frame1.grid_forget()
            self.new_tank_interface()
        if arg == 2:  # New column
            print("New Column")
            return
        if arg == 3:  # Edit tank
            try:
                self.frame1.grid_forget()
                self.choose_db_table()
                self.edit_tk_names=self.table_name
                self.edit_tank_interface()
            except AttributeError as e:
                self.show_error=showerror(
                "Error", message = "Choose tank. \n"+ str(e))
                self.restart() 

        if arg == 4:  # Delete tank
            try:
                self.choose_db_table()
                insert_in_db.delete_tk(self.table_name)
                self.admin_panel()
            except AttributeError as e:
                self.show_error=showerror(
                "Error", message = "Choose tank. \n"+ str(e))
                self.restart()
                
    def choose_db_table(self):
        try:
            x=self.tables_tuple
            z=str(self.list_db.curselection())
            z=z.strip('(),')
            z=int(z)
            self.table_name=str(x[z]).strip('()\',')
        except ValueError as e:
            self.show_error=showerror(
            "Error", message = "Choose tank. \n"+ str(e))

    ## Start of the section that allow to add NEW
    ## TANK DATA TABLE 
    def new_tank_interface(self):
        
        self.footer_text.grid_forget()
        self.frame2.grid()
        self.footer_text.grid()
        
        def addtk():
            new_tank_name=(self.new_tank_name.get())
            ad_db["command"]=insert_in_db.create_tk(new_tank_name)
            succes=Label(self.frame2, text="Succes added "+str(new_tank_name))
            succes.grid(row=2, column=2)
        self.chapter_text_var1=StringVar()
        self.chapter_text_var1.set("You want to add a new Tank.\n"+
        "Please enter a name of Tank: ")
        self.chapter_name_lbl1=Label(self.frame2,
            textvariable=self.chapter_text_var1,
            fg="blue", font=('Sans-serif', 15))
        self.chapter_name_lbl1.grid(row=0, column=0, columnspan=10)

        self.new_tank_name_lbl=Label(self.frame2, text="Name of the Tank")
        self.new_tank_name_lbl.grid(row=1, column=0)
        self.new_tank_name=Entry(self.frame2)
        self.new_tank_name.grid(row=2, column=0)

        self.btn_add_txt_var=StringVar()
        self.btn_add_txt_var.set("Add new Tank")        
        ad_db=Button(
            self.frame2, command=addtk,
            textvariable=self.btn_add_txt_var,
            bg="#cfdfa1"
        )
        ad_db.grid(row=2, column=1)

    def edit_tank_interface(self):
        self.footer_text.grid_forget()
        self.frame3.grid()
        self.footer_text.grid()
        self.chapter_text_var=StringVar()

        self.chapter_text_var.set("You want to edit "+str(self.edit_tk_names)+
        " Tank.\n")
        self.chapter_name_lbl1=Label(self.frame3, 
        textvariable=self.chapter_text_var,
        fg="blue", font=('Sans-serif', 15)
        )   # this a label that have short instructions
        self.chapter_name_lbl1.grid(row=0, column=0, columnspan=10)

        self.new_tank_name_lbl=Label(self.frame3, text="Start to edit:")
        self.new_tank_name_lbl.grid(row=1, column=0)

        self.btn_add_txt_var=StringVar()
        self.btn_add_txt_var.set("Add data to "+
        str(self.edit_tk_names)+" Tank "
        )

        edit=Button(
            self.frame3,
            textvariable=self.btn_add_txt_var,
            command=self.btn_add_sound_val  
        )  #button that confirm selected Tank
        edit.grid(row=2, column=0)
        import_data=Button(
            self.frame3,
            text="Import data",
            command=lambda: insert_in_db.import_data(str(self.edit_tk_names)) 
        )  #button that confirm selected Tank
        import_data.grid(row=2, column=1)

        self.list_of_values=[]
        self.list_of_volumes=[]
        self.show_all_btn=Button(self.frame3,
        command=self.show_all, text="Show_all DATA",
        bg="green"
        )
        self.show_all_btn.grid(row=1, column=4)

        self.set=Checkbutton(self.frame3,
        variable=self.set_tank_for_mdo,
        bg="red"
        )
        self.add_column=Button(self.frame3,
        textvariable=self.set_mdo_tk_text,
        command=lambda: mdo_tanks.mdo_select_tank\
            (self.table_name,self.set_tank_for_mdo.get()),
            bg="red")
        self.set.grid(row=8, column=4)
        self.add_column.grid(row=8, column=5)
        
        
        self.set_type=Checkbutton(self.frame3,
            variable=self.set_type_var,
            bg="red")
        self.add_type=Button(self.frame3,
        textvariable=self.set_type_txt,
        command=lambda: db_commands_calc.type_select_tank(self.table_name,self.set_type_var.get()),
        bg="red")
  
        self.set_type.grid(row=9, column=4)
        self.add_type.grid(row=9, column=5)
        
        self.addsound_var=IntVar()
        self.i=0

    def btn_add_sound_val(self):
        self.footer_text.grid_forget()
        self.frame3.grid()
        self.footer_text.grid()
        def add_value():

            if self.i == 0 :

                self.add_sound_auto=(str(self.addsound.get()))
                self.addsound_var.set(int(self.add_sound_auto)+1)

            if self.i > 0 :

                self.add_sound_auto=int(str(self.addsound.get()))
                self.addsound_var.set(int(self.add_sound_auto)+1)
            try:
                tank = str(self.edit_tk_names)
                sound = self.add_sound_auto
                vol = str(addvol.get())
                insert_in_db.edit_row(tank, str(int(sound)), str(float(vol)))
                self.list_of_values.append(sound)
                self.list_of_volumes.append(vol)
                self.height_volume=int(len(self.list_of_volumes))

                self.i += 1
            except ValueError as e :
                self.show_error=showerror("Error with input data",
                message ="In function(btn_add_sound_val) " + str(e)
                )

        if self.i == 0:
            self.addsound_var.set(0)

        self.addsound = Entry(self.frame3, width=12, textvariable=self.addsound_var)
        self.addsound.grid(row=5, column=0)
        addvol = Entry(self.frame3, width=8)
        addvol.grid(row=5, column=1) 
        btn_add_init_sound=Button(self.frame3, text="add value",
            bg="red", command=add_value
        )
        btn_add_init_sound.grid(row=5, column=2)

    def show_all(self):
        
        self.footer_text.grid_forget()
        self.frame3.grid()
        self.footer_text.grid()

        insert_in_db.show_all_in_tb(self.table_name)
        
        # self.all_sound=insert_in_db.all_sound
        self.all_vol=insert_in_db.all_vol
        self.all_dens=insert_in_db.all_dens
        self.all_temp=insert_in_db.all_temp
        self.all_state=insert_in_db.all_state
        self.all_type=insert_in_db.all_type


        # self.all_soundLbl=Label(self.frame3, width=12, text="Sounding")
        self.all_volLbl=Label(self.frame3, width=12, text="Volume")
        self.all_densLbl=Label(self.frame3, width=12, text="Density")
        self.all_tempLbl=Label(self.frame3, width=12, text="Temperature")
        self.all_stateLbl=Label(self.frame3, width=12, text="State")
        self.all_typeLbl=Label(self.frame3, width=12, text="Type")

        # self.show_all_soundList=Listbox(self.frame3, width=12)
        self.show_all_volList=Listbox(self.frame3, width=12)
        self.show_all_densList=Listbox(self.frame3, width=12)
        self.show_all_tempList=Listbox(self.frame3, width=12)
        self.show_all_stateList=Listbox(self.frame3, width=12)
        self.show_all_typeList=Listbox(self.frame3, width=12)
        
        for data in self.all_vol:
            self.show_all_volList.insert(END, data)
        for data in self.all_dens:
            self.show_all_densList.insert(END, data)
        for data in self.all_temp:
            self.show_all_tempList.insert(END, data)
        for data in self.all_state:
            self.show_all_stateList.insert(END, data)
        for data in self.all_type:
            self.show_all_typeList.insert(END, data)

        self.all_volLbl.grid(row=5 , column=5)
        self.all_densLbl.grid(row=5, column=6)
        self.all_tempLbl.grid(row=5, column=7)
        self.all_stateLbl.grid(row=5, column=8)
        self.all_typeLbl.grid(row=5, column=9)
        
        self.show_all_volList.grid(row=6 , column=5)
        self.show_all_densList.grid(row=6, column=6)
        self.show_all_tempList.grid(row=6, column=7)
        self.show_all_stateList.grid(row=6, column=8)
        self.show_all_typeList.grid(row=6, column=9)


    def restart(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)

    def print_window(self):
        """
        Method for make a screenshot of the window and
        send it for printing
        """
        print_folder="~/Screenshots/"
        screenshot_name=str(time.strftime('%d%m%Y'))+str(".jpg")
        print_file=print_folder+screenshot_name
        print(print_file)
        try:
            comm=str("scrot -u " +str(print_file))
            command=os.system(comm)
            #os.startfile(print_file, "print")
            showinfo("self", message=str("Printed in: "+str(print_folder)))
           
        except Exception as e:
            showinfo("self", message=str(e))
    
    def license_show(self):
        """
        This class method in depends on what is the valueof the
        of self.iterator_for_license show the License
        """
        def close():
            self.footer_text.grid_forget()
            self.frame0.grid()
            self.frame5.grid()
            self.footer_text.grid()
            self.close_license.grid_forget()
            self.license_Text.grid_forget()
            self.frame6.grid_forget()
        
        # call the function from file license_text
        license_text.read_license()
        self.license_text_variable=license_text.license_strings

        self.frame0.grid_forget()
        self.frame5.grid_forget()
        self.footer_text.grid_forget()

        if self.iterator_for_license == 0 :
            self.license_Text=Text(self.frame6 , padx=40)
            self.license_Text.grid(row=0, column=0, columnspan=20)

            self.close_license=Button(self.frame6, command=close, text="Close")
            self.close_license.grid(row=1, column=0, columnspan=20)
            
            for ind, data in enumerate(self.license_text_variable):
                self.license_Text.insert(END, data)
            self.footer_text.grid()
        elif self.iterator_for_license > 0 :
            self.frame6.grid()
            self.license_Text.grid()
            self.close_license.grid()
            self.footer_text.grid()
            self.frame0.grid_forget()
            self.frame5.grid_forget()

        
        else:
            print("error with License Function")
        
        self.iterator_for_license += 1
    
    def help_about(self):
        print("help")
    
    def manual_page(self):
        print("manual")
        
if __name__ == "__main__":
    root = Tk()
    app = App(master=root)
    app.mainloop()
