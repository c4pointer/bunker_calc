#!/usr/bin/python3
# -*- coding: utf-8 -*-
# created by neo
# Version-1.0

from tkinter import *
import platform
import math
# import gnupg
# import getpass
import sqlite3
import sys, os
from tkinter.filedialog import askdirectory, askopenfilenames, askopenfiles
from tkinter.messagebox import showerror, showinfo, askokcancel
from pathlib import Path

file_location_detect=os.getcwd()
try:
    name_off_app="Bunker calc for i3"
    conn=sqlite3.connect(file_location_detect+'/Documents/myapp/Bunker_calc1.db')
except sqlite3.OperationalError as e:
    name_off_app="Bunker calc VS code"
    conn=sqlite3.connect(file_location_detect+'/Bunker_calc1.db')
cur=conn.cursor()

import insert_in_db
import db_commands_calc
import mdo_tanks

operation_platform = str("Arch_Linux") # platform.system()

username =str("Oleg Zubak") # str(os.getlogin())  Тут мы получаем имя владельца Компьютера
user = str(username)  # укажите имя пользователя
m3=str(" m3")
mt=str(" mt")

class App(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title(name_off_app)
        self.master.maxsize(1980, 1080)
        self.master.minsize(1200,1200)
        
        # self.master.geometry('500x300')
        self.grid(ipadx=1, ipady=1, rowspan=5, columnspan=5)
    
        self.create_widgets()

    #### Start to create Frame widgets and some main buttons
    def create_widgets(self):
        '''Create all our Frames and footer and Menu'''
        padding = {'padx':5, 'pady':2}
        self.padding2 = { 'padx': 20, 'pady':2}
        self.padding3 = { 'padx': 20, 'pady':2}
        self.frame0 = Frame()
        self.frame1 = Frame()
        self.frame2 = Frame()
        self.frame3 = Frame()
        self.frame4 = Frame()
        self.frame5 = Frame()

        self.frame0.grid(columnspan=20,ipadx=10, ipady=1)
        self.frame1.grid(columnspan=20,ipadx=10, ipady=1)
        self.frame2.grid(columnspan=20,ipadx=10, ipady=1)
        self.frame3.grid(columnspan=20,ipadx=10, ipady=1)
        self.frame4.grid(columnspan=20,ipadx=10, ipady=1)
        self.frame5.grid(columnspan=20,ipadx=10, ipady=1 )
        
        ## Initial state of MDO section

        self.mdo_state=IntVar()
        self.mdo_state.set(1)
        self.global_i = 0

        ##################
        ## Menu section ##
        ##################

        menubar=Menu(self.master)
        self.master.config(menu=menubar)
        emenubar=Menu(menubar, tearoff = 0)
        emenubar.add_command(label="Admin Panel", command=self.admin_panel_check)

        emenubar.add_separator()
        menubar.add_cascade(label="App", menu=emenubar)

        submenu=Menu(emenubar, tearoff = 0)
        submenu.add_checkbutton(label="Add MDO",
        variable=self.mdo_state,
        command=(lambda:self.cb())
        )
        # submenu.add_command(label="Remove MDO", command=self.remove_mdo)
        emenubar.add_cascade(label="MDO", menu=submenu)
        
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
            font=('Sans-serif', 9), pady=10 
            )

        self.footer_text.grid(
            column=10,
            row=100
            )
        
        self.satrt_build_interface()
        
    ####################
    ### CALCULATION  ###
    ####################


    def satrt_build_interface(self):
        insert_in_db.sort_tanks_mdo()
        
        insert_in_db.sort_tanks()
        self.table_DB=[]
        self.t=insert_in_db.table_names
        
        for i in self.t:

            i=str(i)
            self.tables_in_DB=i.strip('(),\'')
            self.table_DB.append(self.tables_in_DB)
        
        self.mdo=[]
        self.t2=insert_in_db.table_names_md

        for i in self.t2:
            i=str(i)
            self.tables_in_DB_mdo=i.strip('(),\'')
            self.mdo.append(self.tables_in_DB_mdo)


        self.hfo_section=Label(self.frame0, text="HFO Tanks",
        font=('Sans-serif', 8, UNDERLINE), pady=4
        )
        self.hfo_section.grid(row = 0, column=0,
        columnspan=20)

        self.name_of_tanks(self.table_DB, self.frame0)


        self.mdo_section=Label(self.frame5, text="MDO Tanks",
            font=('Sans-serif', 8, UNDERLINE), pady=4
            )
        self.mdo_section.grid(row=0, column=0,
            columnspan=20)

        if self.mdo_state.get() != 0:
            self.cb()


    def name_of_tanks(self, tk_list, frame):  ### Start to build structure of the app
        j=0

        x=list(tk_list)

        self.name_reference_point=(len(x))
        self.names_of_tank=[]
        self.sounding_lbl=StringVar()
        self.labelWidgets_Name=[]

        self.labelWidgets_tankLabel=[]

        self.labelWidgets_soundLabel=[]
        self.entryWidgets_entered_suond={}

        self.labelWidgets_volumeLabel=[]
        self.labelWidgets_volumeResult={}

        self.labelWidgets_Temp=[]
        self.entryWidgets_Temp={}

        self.labelWidgets_DefDens=[]
        self.labelWidgets_DefDens_num={}
        self.labelWidgets_Dens=[]
        self.entryWidgets_Dens_num={}

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
            (frame, **self.padding3, text="Volume in "+m3, width=12,
            bg="#ccc", relief="ridge", borderwidth=2,
            font=('Sans-serif', 8))
            )

        self.labelWidgets_Temp.append(Label
            (frame, **self.padding3, text="Temp", bg="#ccc", relief="ridge", borderwidth=2,
            font=('Sans-serif', 8))
            )
        
        self.labelWidgets_DefDens.append(Label
            (frame,  **self.padding3, bg="#ccc", text="Default Dens", relief="ridge",
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

        for num , i in enumerate(x):
            
            self.table_name_var=StringVar()
            self.table_name_var.set(i)
            self.sounding_lbl.set(i)
            self.names_of_tank.append(self.sounding_lbl.get())


            self.labelWidgets_Name.append(Label(frame,
            textvariable=self.table_name_var, **self.padding2,
            font=('Sans-serif', 8))
            )

            self.entryWidgets_entered_suond[i]=Entry(frame,
            width=10, relief="ridge", borderwidth=2,
            font=('Sans-serif', 8)
            )

            db_commands_calc.calculation(self.table_name_var.get(),self.entryWidgets_entered_suond[i])

            self.labelWidgets_volumeResult[i]=Label(frame,
            **self.padding3, width=10, relief="ridge", borderwidth=2,
            font=('Sans-serif', 8)
            )

            self.entryWidgets_Temp[i]=Entry(
                frame, width=10,
                borderwidth=2, relief="ridge",
                fg="black"
                )

            db_commands_calc.select_DefDens(self.table_name_var.get())

            self.labelWidgets_DefDens_num[i]=(Label
            (frame, **self.padding3, width=8, text=str(db_commands_calc.density),
            relief="ridge", borderwidth=2,
            font=('Sans-serif', 8))
            )


            self.entryWidgets_Dens_num[i]=Entry(
                frame, fg="#00cc00",
                width=8, relief="ridge",
                borderwidth=2, font=('Sans-serif', 8)
                )

            
            self.labelWidgets_ResultMT_num[i]=(Label(
                frame, **self.padding3, fg="blue",
                bg="#c2ccff", width=10,
                relief="ridge", borderwidth=2,font=('Sans-serif', 8))
                )
            
            
            for f in range(len(x)) :
                
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
                
                
                self.entryWidgets_entered_suond[i].grid(row=self.entry_row, column=1, padx=self.padx_for_lbl)

                self.labelWidgets_volumeResult[i].grid(row=self.entry_row, column=2, padx=self.padx_for_lbl)

                self.entryWidgets_Temp[i].grid(row=self.entry_row, column=3, padx=self.padx_for_lbl)

                
                self.labelWidgets_DefDens_num[i].grid(row=self.entry_row, column=4, padx =self.padx_for_lbl)

                
                self.entryWidgets_Dens_num[i].grid(row=self.entry_row, column=5, padx =self.padx_for_lbl)

                self.labelWidgets_ResultMT_num[i].grid(row=self.entry_row, column=6, padx =self.padx_for_lbl)


                j += 1
        
        
        
        self.button_Widget_number=Button(
        frame, bg='green',  text="Calculate",
        relief="ridge",
        activebackground='#aa3666', command=lambda:self.calculate(self.hfo_data_sound,
        self.hfo_data_vol_result, self.hfo_data_temp,
        self.hfo_data_def_dens, self.hfo_data_new_dens,
        self.hfo_data_result_num,
        frame, self.change_sound_hfo
        ),
        **self.padding3
        )
        self.button_Widget_number.grid(row=1, column=8)
        self.hfo_data_sound=self.entryWidgets_entered_suond
        self.hfo_data_vol_result=self.labelWidgets_volumeResult
        self.hfo_data_temp=self.entryWidgets_Temp
        self.hfo_data_def_dens=self.labelWidgets_DefDens_num
        self.hfo_data_new_dens=self.entryWidgets_Dens_num
        self.hfo_data_result_num=self.labelWidgets_ResultMT_num
        self.change_sound_hfo=self.entryWidgets_entered_suond

    def name_of_tanks_mdo(self, tk_list, frame):  ### Start to build structure of the app
        j=0
        
        x=list(tk_list)

        self.name_reference_point=(len(x))
        self.names_of_tank=[]
        self.sounding_lbl=StringVar()
        self.labelWidgets_Name=[]

        self.labelWidgets_tankLabel=[]

        self.labelWidgets_soundLabel=[]
        self.entryWidgets_entered_suond={}

        self.labelWidgets_volumeLabel=[]
        self.labelWidgets_volumeResult={}

        self.labelWidgets_Temp=[]
        self.entryWidgets_Temp={}

        self.labelWidgets_DefDens=[]
        self.labelWidgets_DefDens_num={}
        self.labelWidgets_Dens=[]
        self.entryWidgets_Dens_num={}

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
            (frame, **self.padding3, text="Volume in "+m3, width=12,
            bg="#ccc", relief="ridge", borderwidth=2,
            font=('Sans-serif', 8))
            )

        self.labelWidgets_Temp.append(Label
            (frame, **self.padding3, text="Temp", bg="#ccc", relief="ridge", borderwidth=2,
            font=('Sans-serif', 8))
            )
        
        self.labelWidgets_DefDens.append(Label
            (frame,  **self.padding3, bg="#ccc", text="Default Dens", relief="ridge",
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

        for num , i in enumerate(x):
            
            self.table_name_var=StringVar()
            self.table_name_var.set(i)
            self.sounding_lbl.set(i)
            self.names_of_tank.append(self.sounding_lbl.get())


            self.labelWidgets_Name.append(Label(frame,
            textvariable=self.table_name_var, **self.padding2,
            font=('Sans-serif', 8))
            )

            self.entryWidgets_entered_suond[i]=Entry(frame,
            width=10, relief="ridge", borderwidth=2,
            font=('Sans-serif', 8)
            )

            db_commands_calc.calculation(self.table_name_var.get(),self.entryWidgets_entered_suond[i])

            self.labelWidgets_volumeResult[i]=Label(frame,
            **self.padding3, width=10, relief="ridge", borderwidth=2,
            font=('Sans-serif', 8)
            )

            self.entryWidgets_Temp[i]=Entry(
                frame, width=10,
                borderwidth=2, relief="ridge",
                fg="black"
                )

            db_commands_calc.select_DefDens(self.table_name_var.get())

            self.labelWidgets_DefDens_num[i]=(Label
            (frame, **self.padding3, width=8, text=str(db_commands_calc.density),
            relief="ridge", borderwidth=2,
            font=('Sans-serif', 8))
            )


            self.entryWidgets_Dens_num[i]=Entry(
                frame, fg="#00cc00",
                width=8, relief="ridge",
                borderwidth=2, font=('Sans-serif', 8)
                )

            
            self.labelWidgets_ResultMT_num[i]=(Label(
                frame, **self.padding3, fg="blue",
                bg="#c2ccff", width=10,
                relief="ridge", borderwidth=2,font=('Sans-serif', 8))
                )
            
            
            for f in range(len(x)) :
                
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
                
                
                self.entryWidgets_entered_suond[i].grid(row=self.entry_row, column=1, padx=self.padx_for_lbl)

                self.labelWidgets_volumeResult[i].grid(row=self.entry_row, column=2, padx=self.padx_for_lbl)

                self.entryWidgets_Temp[i].grid(row=self.entry_row, column=3, padx=self.padx_for_lbl)

                
                self.labelWidgets_DefDens_num[i].grid(row=self.entry_row, column=4, padx =self.padx_for_lbl)

                
                self.entryWidgets_Dens_num[i].grid(row=self.entry_row, column=5, padx =self.padx_for_lbl)

                self.labelWidgets_ResultMT_num[i].grid(row=self.entry_row, column=6, padx =self.padx_for_lbl)


                j += 1
        
        
        
        self.button_Widget_number=Button(
        frame, bg='green',  text="Calculate",
        relief="ridge",
        activebackground='#aa3666', command=lambda:self.calculate(self.mdo_data_sound,
        self.mdo_data_vol_result, self.mdo_data_temp,
        self.mdo_data_def_dens, self.mdo_data_new_dens,
        self.mdo_data_result_num,
        frame, self.change_sound_mdo
        ),
        **self.padding3
        )
        self.button_Widget_number.grid(row=1, column=8)

        self.mdo_data_sound=self.entryWidgets_entered_suond
        self.mdo_data_vol_result=self.labelWidgets_volumeResult
        self.mdo_data_temp=self.entryWidgets_Temp
        self.mdo_data_def_dens=self.labelWidgets_DefDens_num
        self.mdo_data_new_dens=self.entryWidgets_Dens_num
        self.mdo_data_result_num=self.labelWidgets_ResultMT_num
        self.change_sound_mdo=self.entryWidgets_entered_suond


    def calculate(self, data, vol_res, temperature, def_dens, new_dens, result_num, frame, change_sound):


        def result_in_MT(data):

            # Insert the extracted volume into the lbl
            self.result_insert_to_Lbl={}

            for key, value in zip(data.items(), self.res):
                    key=key[0]
                    self.result_insert_to_Lbl[key]=value

            for key1, value1 in self.result_insert_to_Lbl.items():        
                result_num[key1]['text']=str(value1)

            
            # for key, value in result_num.items():
            #     self.result_value=str(
            #         result_num[key]['text'])
            if self.real_vol:
                self.total_widget(frame)
            else:
                pass
            
        
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
                
                if volume_value == 0:
                    pass
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
                                # self.show_error=showinfo(
                                #     "Error", message=str(
                                #     "Введите правильно температуру или посчитает при : \n + 15 С"))

                # Weight factor
                self.weight_cor_factor=float(conv_dens/1000-0.0011)

                # real volume is calculating:
                self.q=float(volume_value)*float(self.temp_cor_factor)
                self.real_vol=str(round((self.q*self.weight_cor_factor),4))
                self.res.append(self.real_vol)

            except Exception as e:

                print(str("Error in string No 698: ")+str(e))


        def volume_by_density(data):

            self.volume_density=[]
            self.convert_density=[]
            self.res=[] # Create an empty list for append calculated results

            for volume_value, dens in zip(self.vol.items(), self.new_dens.items()):
                volume_value=(volume_value[1])
                
                dens=(dens[1])
                
                try:

                    
                    volume_density=float(volume_value)*float(dens)
                    self.volume_density.append(volume_density)
                    convert_density=((float(dens)/2)*1000)*2
                    self.convert_density.append(convert_density)

                except ValueError as e:

                    # pass
                    self.show_error=showerror(
                    "Error", message=str("Error in sounding value \n"))

            for conv_dens, volume_value, temp in zip(self.convert_density, self.vol.items(), self.temp.items()):
                vol_correction_factor_calc(conv_dens,volume_value[1],temp[1])

            result_in_MT(self.vol)

        ## The calculation and gathering of information is started Below
        self.name=[]
        self.sound=dict()
        self.vol=dict()
        self.vol_insert_to_Lbl=dict()
        self.temp=dict()
        self.def_dens=dict()
        self.new_dens=dict()
        # Extract value of sound

        for key, value in data.items():
            if value.get() !='':
                try:
                    self.sound_value=float(value.get())

                    

                    # self.sound.append(self.sound_value)
                    self.sound[key]=(self.sound_value)
                    self.name.append(key)
            
                except ValueError:

                    pass
                    # self.show_error=showerror(
                    #     "Error", message=str("Вы ввели не цыфры а :\n"+str(ValueError)))
        
            else:
                self.sound[key]=0
                
        # Extarct the value of volume for the given sounding value

        for i, d in self.sound.items():
            try:
                db_commands_calc.calculation(i,d)
                data1=(db_commands_calc.volume_in_m3)
                data1=str(data1).strip('\'[]')
                data1=float(data1)
                self.vol[i]=data1

            except ValueError:

                # self.show_error=showerror(
                #     "Error", message=str("Вы ввели не цыфры или такого значение нет\n")
                #     )
                self.vol[i]=("<--- check")

            except TypeError:
                pass
                # self.show_error=showerror(
                #     "Error", message=str("Пусто или нет такого занчения\n")
                #     )

            except IndexError:
                pass
                # self.show_error=showerror(
                #     "Error", message=str("Такого значение нет\n")
                # )

        # Insert the extracted volume into the lbl
            
        self.vol_insert_to_Lbl={}

        for num, f in vol_res.items() :

            try:
                    self.vol_insert_to_Lbl[num]=self.vol[num]
                    f['bg']="#cc6cc6"

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
        
        

        # Extract value of new denseti if it not corresponds to default
        # and also if was entered new dedsity we hide the lbl widget of 
        # default densety
        for j, d in new_dens.items():

            new_density=d.get()

            if new_density != '':
                try:
                    if  0 < float(new_density) < 1.0760:

                        self.show_info=askokcancel(
                                "Wait until Database will be filled",
                                message=str("Поменять вязкость \n"+
                                "для танка: " + str(j)+
                                " на " + str(new_density)
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
                        message=str("Такого значение нет\n"+str(e))
                        )
        
        # go to  function were will calculate all inputed data in 
        # the Entry widgets upper^
        volume_by_density(data)

    def total_widget(self, frame):

            self.lbl_row=(len(self.table_DB)**2)+1
            try:
                result=[]


                self.total_widget_Lbl=Label(frame, text="Total in "+ str(mt),
                width=12, **self.padding2, borderwidth = 2, relief="ridge"
                )
                self.total_widget_Lbl.grid(row = self.lbl_row+2, column = 6, pady =2)
                self.total_widget_Lbl_num = Label(frame,
                width = 12, **self.padding2, borderwidth = 2, relief = "ridge",
                bg = "#c6c5c7"
                )

                self.total_widget_Lbl_num.grid(row=self.lbl_row+3, column=6, pady =2)

                for i, d in enumerate(self.res) :

                    data = float(d)
                    result.append(data)
                total_quantity = round(sum(result),3)
                self.total_widget_Lbl_num['text'] = float(total_quantity)
  
            except Exception as e :

                pass
                # self.show_error = showerror("Eror with total",
                # message="Somthing goes wrong with inputed data \n"+
                # "Please recheck"
                # )
        
    def cb(self):

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

        if self.global_i == 0:
            
            self.name_of_tanks_mdo(self.mdo, self.frame5)
            self.global_i +=1
        else:

            self.frame5.grid()
            self.footer_text.grid_forget()
            self.name_of_tanks_mdo(self.mdo, self.frame5)
            self.footer_text.grid()

    def remove_mdo(self):
        try:

            self.frame5.grid_forget()

        except Exception as e:

            pass
            # self.show_error=showerror(
            # "Error", message = "Can't remove MDO tanks") 

    ####################
    ### ADMIN PANEL  ###
    ####################

    def admin_panel_check(self):
        self.set_tank_for_mdo=IntVar()
        self.set_mdo_tk_text=StringVar()
        self.set_mdo_tk_text.set("Set to ")
        def get_api_pass():

            try:
                self.password=str(self.password_entry.get())
                if self.password == "":
                    self.show_error=showerror(
                    "Error", message = "Пароль пустой: \n"+ str(e))
                
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
                    self.show_error=showerror("Error", message = ("Пароль неверный \n"+ str(e)))

            except AttributeError as e:
                self.show_error=showerror(
                "Error", message = "Пароль пустой: \n"+ str(e))


        def click():
            try:
                get_api_pass()

                # print(str(self.password))
                if str(apipass) == str(self.password):
                    self.admin_panel()
                else:
                    self.show_error=showerror(
                    "Error", message=str("Пароль не верный\n")
                    )
            except NameError as e:
                pass

        self.frame0.grid_forget()
        self.frame5.grid_forget()

        self.password_entry = Entry(self.frame4, width = 10)
        self.password_entry.config(show = "*")
        self.password_entry.focus_set()
        self.password_entry.grid(row = 0, column = 0)

        enter_password = Button(self.frame4,
        text = "Submit", command = click,
        bg = "blue"
        )
        enter_password.grid(row = 0, column = 1)



    def admin_panel(self):

        self.frame4.grid_forget()

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
        self.chapter_name_lbl=Label(self.frame1, textvariable=self.chapter_text_var,
        fg="blue", font=('Sans-serif', 15)
        )
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
        # # mdo_tanks.check_tk_for_mdo(self.table_name)
        # print(mdo_tanks.set_value)




    def new_tank_interface(self):   ## Start of the section that allow to add NEW 
                                    ## TANK DATA TABLE 
        def addtk():
            new_tank_name=(self.new_tank_name.get())
            addb["command"]=insert_in_db.create_tk(new_tank_name)
            succes=Label(self.frame2, text="Succes added "+str(new_tank_name))
            succes.grid(row=2, column=2)
        self.chapter_text_var1=StringVar()
        self.chapter_text_var1.set("You want to add a new Tank.\n"+
        "Please enter a name of Tank: ")
        self.chapter_name_lbl1=Label(self.frame2, textvariable=self.chapter_text_var1,
        fg="blue", font=('Sans-serif', 15)
        )
        self.chapter_name_lbl1.grid(row=0, column=0, columnspan=10)

        self.new_tank_name_lbl=Label(self.frame2, text="Name of the Tank")
        self.new_tank_name_lbl.grid(row=1, column=0)
        self.new_tank_name=Entry(self.frame2)
        self.new_tank_name.grid(row=2, column=0)

        self.btn_add_txt_var=StringVar()
        self.btn_add_txt_var.set("Add new Tank")        
        addb=Button(
            self.frame2, command=addtk,
            textvariable=self.btn_add_txt_var,
            bg="#cfdfa1"
        )
        addb.grid(row=2, column=1)



    def edit_tank_interface(self):

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
        textvariable=self.set_mdo_tk_text, command=lambda: mdo_tanks.mdo_select_tank(self.table_name,self.set_tank_for_mdo.get()),
        bg="red"
        )
        self.set.grid(row=8, column=4)
        self.add_column.grid(row=8, column=5)

        # if mdo_tanks.check_tk_for_mdo.set_value == 0 :
        #     self.set_mdo_tk_text.set("Seted To MDO")
        # else:
        #     self.set_mdo_tk_text.set("Seted To HFO")
        self.addsound_var=IntVar()
        self.i=0
    def btn_add_sound_val(self):

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

        insert_in_db.show_all_in_tb(self.table_name)

        # self.all_sound=insert_in_db.all_sound
        self.all_vol=insert_in_db.all_vol
        self.all_dens=insert_in_db.all_dens
        self.all_temp=insert_in_db.all_temp

        # self.all_soundLbl=Label(self.frame3, width=12, text="Sounding")
        self.all_volLbl=Label(self.frame3, width=12, text="Volume")
        self.all_densLbl=Label(self.frame3, width=12, text="Density")
        self.all_tempLbl=Label(self.frame3, width=12, text="Temperature")

        # self.show_all_soundList=Listbox(self.frame3, width=12)
        self.show_all_volList=Listbox(self.frame3, width=12)
        self.show_all_densList=Listbox(self.frame3, width=12)
        self.show_all_tempList=Listbox(self.frame3, width=12)
        # for data in self.all_sound:
        #     self.show_all_soundList.insert(END, data)
        for data in self.all_vol:
            self.show_all_volList.insert(END, data)
        for data in self.all_dens:
            self.show_all_densList.insert(END, data)
        for data in self.all_temp:
            self.show_all_tempList.insert(END, data)

        # self.all_soundLbl.grid(row=5 , column=4 )
        self.all_volLbl.grid(row=5 , column=5 )
        self.all_densLbl.grid(row=5, column=6 )
        self.all_tempLbl.grid(row=5, column=7 )


        self.show_all_volList.grid(row=6, column=5)
        self.show_all_densList.grid(row=6, column=6)
        self.show_all_tempList.grid(row=6, column=7)


    def restart(self):

        python = sys.executable
        os.execl(python, python, * sys.argv)


if __name__ == "__main__":
    root = Tk()
    app = App(master=root)
    app.mainloop()
