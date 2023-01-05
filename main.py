
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.label import MDLabel
from collections import ChainMap

# import file from project
import db_editing
import db_reading
import calculations

import os
import sqlite3
# Window resizing. To be deleted or commented before compiling
# from kivy.core.window import Window
# Window.size = (400, 700)

total_list_hfo= {}
total_list_mdo= {}
# def_dens = float(str("0.9000"))
names_hfo =[]
names_mdo =[]
def_temp = int(str("15"))
prev_label_text = {}

vessels =[]
file_location_detect = os.getcwd()
try:
    scan_dir=os.scandir(file_location_detect)
    for entries in scan_dir:
        if not entries.name.endswith('_prev.db') and entries.is_file:
            if entries.name.endswith(".db"):
                vessels.append(str(entries).removeprefix('<DirEntry \'').removesuffix('.db\'>').title())

    # conn = sqlite3.connect(
    #     (file_location_detect+'/Documents/myapp/bunker_calc.db'), check_same_thread=False)
except sqlite3.OperationalError as e:
    pass
    # name_off_app = "BunkerCalc"
    # conn = sqlite3.connect(
    #     (file_location_detect+'/bunker_calc.db'), check_same_thread=False)

print(str(vessels).capitalize())


class TabScreen(Screen):
    pass


class TotalScreen(Screen):
    pass


class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''


# class Store_Values():

#     def __init__(self, sound, tk_name):
#         self.sound = sound
#         self.tk_name = tk_name


# Here we declare 2 screens for our App
# One for input all meassurments, other one for total result
sm = ScreenManager()
sm.add_widget(TabScreen(name='tab_screen'))
sm.add_widget(TotalScreen(name='total_screen'))


class BunkerCalc(MDApp):

    def build(self):
        
        # Theme and colors
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.primary_hue = "600"
        self.theme_cls.theme_style = "Dark"
        

    def dropdown(self, x):
        """
        Create a dropdown menu for navigate beetwen the screens
        """
        self.menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "Tanks Sounding",
                "on_release": lambda x="Tanks Sounding": self.screen2()
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Total Result",
                "on_release": lambda x="Total Result": self.screen2()
            }
        ]
        self.menu = MDDropdownMenu(
            items=self.menu_items,
            width_mult=4
        )
        self.menu.caller = x
        self.menu.open()


    def calculate_total(self):
        # Calculate the total m3 in our "total_list"
        self.total_result_hfo = []
        self.total_result_mdo = []
        self.mdo_tons = []
        self.hfo_tons = []
        # HFO
        self.sum_hfo = 0
        for i in (self.names):
            try:
                if len(total_list_hfo[i]) > 0:
                    self.total_result_hfo.append(total_list_hfo[i])

            except KeyError as err:
                pass
        


        for i in self.total_result_hfo:
            self.sum_hfo += float(i[0])
            # float(i[2]) temperature
            tons_hfo = float(i[0])*float(i[3])
            self.hfo_tons.append(tons_hfo)    
        
        # MDO
        self.sum_mdo = 0
        for d in (list(set(self.mdo_names).intersection(set(self.names)))):
            try:
                if len(total_list_mdo[d]) > 0:
                    self.total_result_mdo.append(total_list_mdo[d])

            except KeyError as err:
                pass
        
        for i in self.total_result_mdo:
            self.sum_mdo += float(i[0])
            # float(i[2]) temperature
            tons_mdo = float(i[0])*float(i[3])
            self.mdo_tons.append(tons_mdo)
        
        if len(self.hfo_tons) ==0 :
            self.hfo_tons.append(float(0))
        if len(self.mdo_tons) ==0:
            self.mdo_tons.append(float(0))
        return self.sum_mdo, self.sum_hfo, self.hfo_tons, self.mdo_tons


    def screen2(self):
        """
        Go to total screen where is shown total figure
        At each time when "total_screen" is pressed is recalculated
        total figure
        """
        if self.root.current != "total_screen":
            self.root.current = "total_screen"
            self.calculate_total()
            self.root.get_screen("total_screen").ids.right_action.text = "Tank sounding"
            self.root.get_screen("total_screen").ids.total_hfo.text = str(round(self.sum_hfo, 3)) + str(" m3 HFO") \
                + str(f"\n {self.hfo_tons[0]} MT HFO")
            self.root.get_screen("total_screen").ids.total_mdo.text = str(round(self.sum_mdo, 3)) + str(" m3 MDO") \
                + str(f"\n {self.mdo_tons[0]} MT MDO")
        else:
            self.root.get_screen("tab_screen").ids.right_action.text = "Total  result"
            self.root.current = "tab_screen"


    def vessel_name(self):
        self.root.get_screen("tab_screen").ids.right_action.text = "Total  result"
        self.vessel = self.root.get_screen("tab_screen").ids.top_menu.title = vessels[0]
        self.set_vessel_name()


    def set_vessel_name(self):
        # self.root.get_screen("tab_screen").ids.top_menu.title.halign = 'right'
        self.root.get_screen("total_screen").ids.total_menu.title = str(self.vessel)


    def name_of_tank(self):
        # Extract from DB names of each tank
        self.names = []
        db_reading.extract_names()

        self.tank_name = db_reading.name_of_tank
        for i in self.tank_name:
            self.names.append(i[0])


    def mdo_tank_extract(self):
        self.mdo_names = []
        db_reading.sort_tanks_mdo()
        self.mdo_tanks = db_reading.table_names_md
        for i in self.mdo_tanks:
            self.mdo_names.append(i[0])
        # print(self.mdo_names)


    def add_tab(self):
        names_for_do = list(set(self.mdo_names).intersection(set(self.names)))
        # print(names_for_do)
        self.tab_iterator = 0
        for i in (self.names):
            db_reading.extract_prev(i)
            
            if not i in names_for_do:
            
                self.root.get_screen('tab_screen').ids.tabs.add_widget(Tab(tab_label_text=f"{i}"))
            for do in names_for_do :
                if do == i:
                    self.root.get_screen('tab_screen').ids.tabs.add_widget(Tab(tab_label_text=f"{do} mdo"))
    
        self.root.get_screen('tab_screen').ids.tabs.add_widget(
            Tab(title=f"Previous quantity:\n{db_reading.prev_label_text[str(self.tank_name.text.removesuffix('mdo')).strip(' ')][0]} m3, at \
            {db_reading.prev_label_text[str(self.tank_name.text.removesuffix('mdo')).strip(' ')][1]} cm")
        )
        
        # afetr add text to label of first tab we delete here the last widget that is non correct 
        self.root.get_screen('tab_screen').ids.tabs.remove_widget(
            self.root.get_screen('tab_screen').ids.tabs.get_tab_list()[-1]
            )


    def on_tab_switch(
            self, instance_tabs, instance_tab, instance_tab_label, tab_text
    ):
        '''Called when switching tabs.

        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        '''
        instance_tab.ids.sound_field.hint_text = "Sounding value (cm):"
        instance_tab.ids.sound_field.text_color_normal = 1, 1, 0.8, 1

        self.sound_value = instance_tab.ids.sound_field
        self.tank_name = instance_tab_label
        self.result = instance_tab.ids.label
        self.dens_new = instance_tab.ids.density_field
        
        #if no any entries are inserted we show below text to user
        if len(total_list_mdo)==0 and len(total_list_hfo)==0:
            try:
                self.result.text = str("Previous quantity:\n")+\
                str(db_reading.prev_label_text[str(self.tank_name.text.removesuffix('mdo')).strip(' ')][0])+ \
                str(" m3, at ") + str(db_reading.prev_label_text[str(self.tank_name.text.removesuffix('mdo')).strip(' ')][1])+ str(" cm")
                self.result.font_size = "24dp"
                db_editing.type_sel(tab_text)

            except :
                pass


    def callback_Calc(self, *args):

        db_editing.calculation(str(self.tank_name.text.removesuffix('mdo')).strip(' '), self.sound_value.text)
        db_editing.type_sel(str(self.tank_name.text.removesuffix('mdo')).strip(' '))
        db_editing.state_sel(str(self.tank_name.text.removesuffix('mdo')).strip(' '))
        # db_editing.select_DefDens(str(self.tank_name.text.removesuffix('mdo')).strip(' '))
        # print(self.root.get_screen('tab_screen').ids.slider_lbl.text==("45"))
        # if db_editing.type_of_tank[0] == 1:
            
        #     print(f"Type of tank {str(self.tank_name.text.removesuffix('mdo')).strip(' ')} is: {self.sound_value.text} \n")

        # If tank is in MDO state than we make calcs for it and append to
        # "total_list_mdo" for displaing in Totoal result screnn
        if db_editing.state_of_tank[0] ==1:
            
            try:
                self.result.font_size = "30dp"
                if db_editing.type_of_tank[0] == 1:
                    self.result.text=str(self.sound_value.text)
                    self.temp_dens_extraction()
                    # Define below row for take into prev function use
                    total_list_mdo[str(self.tank_name.text.removesuffix('mdo')).strip(' ')] = ((self.result.text), self.sound_value.text, self.temperature, self.def_dens)
                    self.result.text = str(self.sound_value.text) + str(" m3")

                else:
                    self.result.font_size = "30dp"
                    self.result.text = str(db_editing.volume_in_m3[0])
                    self.temp_dens_extraction()
                    # Define below row for take into prev function use
                    total_list_mdo[str(self.tank_name.text.removesuffix('mdo')).strip(' ')] = ((self.result.text), self.sound_value.text, self.temperature, self.def_dens)
                    self.result.text = str(db_editing.volume_in_m3[0]) + str(" m3")
                            
            

                # Insert data to prev DB for prev values extarcting on start
                if len(total_list_mdo) >0 :
                    print(total_list_hfo)
                    print("\n")
                    print(total_list_mdo)
                    print("********\n")
                    for i  in (total_list_mdo):
                        db_reading.add_to_prevdb(i, total_list_mdo[i][1], total_list_mdo[i][0])

            except IndexError as e:
                # Printing on display the error and change the font-size
                self.result.text = str("Wrong sounding value!")
                self.result.font_size = "20dp"

        # Calculate if tank is NOT MDO but is HFO
        else:
            try:
                self.result.font_size = "30dp"
                if db_editing.type_of_tank[0] == 1:
                    self.result.text=str(self.sound_value.text)
                    self.temp_dens_extraction()
                    # Define below row for take into prev function use
                    total_list_hfo[str(self.tank_name.text.removesuffix('mdo')).strip(' ')] = ((self.result.text), self.sound_value.text, self.temperature, self.def_dens)
                    self.result.text = str(self.sound_value.text) + str(" m3")

                else:
                    self.result.font_size = "30dp"
                    self.result.text = str(db_editing.volume_in_m3[0])
                    self.temp_dens_extraction()

                    # Define below row for take into prev function use
                    total_list_hfo[str(self.tank_name.text.removesuffix('mdo')).strip(' ')] = ((self.result.text), self.sound_value.text, self.temperature, self.def_dens)
                    self.result.text = str(db_editing.volume_in_m3[0]) + str(" m3")
                            
            

                # Insert data to prev DB for prev values extarcting on start
                if len(total_list_hfo) >0 :
                    print(total_list_hfo)
                    print("\n")
                    print(total_list_mdo)
                    print("*************\n")
                    for i  in (total_list_hfo):
                        db_reading.add_to_prevdb(i, total_list_hfo[i][1], total_list_hfo[i][0])
                        # print(f"Data insert in {i} with sound = {total_list[i][1]} and volume ={total_list[i][0]} , deleted value is = { total_list} ")

            except IndexError as e:
                # Printing on display the error and change the font-size
                self.result.text = str("Wrong sounding value!")
                self.result.font_size = "20dp"
        
    def my_value(self, object_property, value):  # <<<<<<<<<<< Value from Temp slider
        self.slider_value={}
        self.slider_value[str(self.tank_name.text.removesuffix('mdo')).strip(' ')]= str(int(round(value,0)))

    def temp_dens_extraction(self):
        try:
            if len(self.slider_value) !=0 :
                self.temperature = str(self.slider_value[str(self.tank_name.text.removesuffix('mdo')).strip(' ')])

                print(self.slider_value[str(self.tank_name.text.removesuffix('mdo')).strip(' ')])
            # Density selecting
            if len(self.dens_new.text) == 0:
                self.def_dens = db_editing.select_DefDens(str(self.tank_name.text.removesuffix('mdo')).strip(' '))
                
            else:
                self.def_dens = self.dens_new.text
                
        except KeyError as error:
            if len(self.dens_new.text) == 0:
                self.def_dens = db_editing.select_DefDens(str(self.tank_name.text.removesuffix('mdo')).strip(' '))
                
            else:
                self.def_dens = self.dens_new.text
            self.temperature = def_temp

        except AttributeError as error2:
            if len(self.dens_new.text) == 0:
                self.def_dens = db_editing.select_DefDens(str(self.tank_name.text.removesuffix('mdo')).strip(' '))
                
            else:
                self.def_dens = self.dens_new.text
            self.temperature = def_temp
            
        return self.temperature, self.def_dens
        
    def on_start(self):

        self.name_of_tank()
        self.mdo_tank_extract()
        self.vessel_name()
        self.add_tab()
    




if __name__ == "__main__":
    BunkerCalc().run()
