
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.dialog import MDDialog
# from kivymd.uix.label import MDLabel
# from collections import ChainMap

# import file from project
import db_editing
import db_reading
import vol_coorection
import drop_vessel_list
import calculation

import os
import sqlite3
import threading
# Window resizing. To be deleted or commented before compiling
# from kivy.core.window import Window
# Window.size = (400, 700)

# Here we store our dict with total quantity of fuel
total_list_hfo= {}
total_list_mdo= {}

# Declare empty list for tanks
names_hfo =[]
names_mdo =[]

# Default variables
def_temp = int(str("15"))
vessel_db = "viking_ocean.db"

prev_label_text = {}

# Store the all ships
vessels =[]

# Store db names for each ship
vessel_name_db =[]

file_location_detect = os.getcwd()
try:
    # scan current working Directory
    scan_dir=os.scandir(file_location_detect)
    for entries in scan_dir:
        if not entries.name.endswith('_prev.db') and entries.is_file:
            if entries.name.endswith(".db"):
                parsed_vessel = str(entries).removeprefix('<DirEntry \'').removesuffix('.db\'>').title()
                vessel_name_db_parsed = str(entries).removeprefix('<DirEntry \'').removesuffix('\'>')
                vessel_name_db.append(vessel_name_db_parsed)
                vessels.append(parsed_vessel)
    
except:
    print(f"Error in DB choosing code")


class TabScreen(Screen):
    pass


class TotalScreen(Screen):
    pass


class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''


sm = ScreenManager()
sm.add_widget(TabScreen(name='tab_screen'))
sm.add_widget(TotalScreen(name='total_screen'))


class BunkerCalc(MDApp):

    def build(self):
        # Theme and colors
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.primary_hue = "600"
        self.theme_cls.theme_style = "Dark"
        
    def on_start(self):
        self.the_DB = {}
        # Calculation button state is Disabled
        self.button_state = 0
        self.name_of_tank(vessel_db)
        self.mdo_tank_extract(vessel_db)
        self.add_tab(vessel_db)
        self.slider_value={}
        self.j = 0

        # Label for toggle screens between the total screen and Tabs
        self.root.get_screen("tab_screen").ids.right_action.text = "Total  result"
        self.root.get_screen("tab_screen").ids.select_vessel.text = "Select vessel"
        # self.root.get_screen("tab_screen").ids.calc.disabled = True

    def change_vessel(self, v ):
        f =self.root.get_screen('tab_screen').ids.tabs.get_tab_list()
        for i in f:
            self.root.get_screen("tab_screen").ids.tabs.remove_widget(i)
        self.name_of_tank(v)
        self.mdo_tank_extract(v)
        self.add_tab(v)


    # def dropdown(self, x):
    #     """
    #     Create a dropdown menu for navigate beetwen the screens
    #     """
    #     self.menu_items = [
    #         {
    #             "viewclass": "OneLineListItem",
    #             "text": "Tanks Sounding",
    #             "on_release": lambda x= 'lambda':self.screen2()
    #         },
    #         {
    #             "viewclass": "OneLineListItem",
    #             "text": "Total Result",
    #             "on_release": lambda x= 'lambda':self.screen2()
    #         }
    #     ]
    #     self.menu = MDDropdownMenu(
    #         items=self.menu_items,
    #         width_mult=4
    #     )
    #     self.menu.caller = x
    #     self.menu.open()


    def calculate_total(self):
        # Calculate the total m3 in our "total_list"
        self.total_result_hfo = []
        self.total_result_mdo = []
        self.mdo_tons = []
        self.hfo_tons = []
        # HFO
        self.sum_hfo = 0
        self.sum_hfo_tons = 0
        for i in (self.names):
            try:
                if len(total_list_hfo[i]) > 0:
                    self.total_result_hfo.append(total_list_hfo[i])

            except KeyError as err:
                # print("eror string 147")
                pass
        


        for i in self.total_result_hfo:
            self.sum_hfo += float(i[4])
            self.sum_hfo_tons += float(i[0])    
        
        # MDO
        self.sum_mdo = 0
        self.sum_mdo_tons = 0
        for d in (list(set(self.mdo_names).intersection(set(self.names)))):
            try:
                if len(total_list_mdo[d]) > 0:
                    self.total_result_mdo.append(total_list_mdo[d])

            except KeyError as err:
                # print("eror string 164")
                pass
        
        for i in self.total_result_mdo:
            self.sum_mdo += float(i[4])
            self.sum_mdo_tons += float(i[0])
        
        if len(self.hfo_tons) ==0 :
            self.hfo_tons.append(float(0))
        if len(self.mdo_tons) ==0:
            self.mdo_tons.append(float(0))
        return self.sum_mdo, self.sum_hfo, self.hfo_tons, self.mdo_tons,self.sum_mdo_tons ,self.sum_hfo_tons  


    def screen2(self):
        """
        Go to total screen where is shown total figure
        At each time when "total_screen" is pressed is recalculated
        total figure
        """
        if self.root.current != "total_screen":
            self.root.current = "total_screen"
            self.calculate_total()
            # Display total results for MDO and HFO
            self.root.get_screen("total_screen").ids.right_action.text = "Tank sounding"
            self.root.get_screen("total_screen").ids.total_hfo.text = str(round(self.sum_hfo, 3)) + str(" m3 HFO") \
                + str(f"\n {round((self.sum_hfo_tons),2)} MT HFO"+f"\n___________________")
            self.root.get_screen("total_screen").ids.total_mdo.text = str(round(self.sum_mdo, 3)) + str(" m3 MDO") \
                + str(f"\n {round((self.sum_mdo_tons),2)} MT MDO")
        else:
            self.root.current = "tab_screen"


    def vessel_name(self,vessel):
        """
        Set selected vessel as title of App
        """
        self.name_of_vessel_db = str(vessel).lower()+".db"  # Name of DB if is non default
        # THREAD FOR selecting and switching vessel DB
        # print(f"{vessel} == {str(self.the_DB[vessel])} ")
        # if self.j == 0:
        #     self.start_thread(self.name_of_vessel_db)
        #     self.j += 1
        
        # else:
        #     if self.name_of_vessel_db == str(self.the_DB[vessel]):
        #         print("pass block")
                
        #     else:
        #         self.start_thread(self.name_of_vessel_db)
        #         self.j += 1
        #         print("here")
        self.start_thread(self.name_of_vessel_db)
        if len(self.the_DB) != 0:
            self.vessel = self.root.get_screen("tab_screen").ids.top_menu.title = str(vessel)
            self.menu.dismiss()
        

        self.root.get_screen("total_screen").ids.total_menu.title = str(vessel)

        


    def choose_vessel(self,x):
        """
        Create a dropdown menu for selecting the Vessel`s Data Base
        """
        try:
            self.root.get_screen("tab_screen").ids.select_vessel.text = "Vessel"
            self.db_tuple = {}
            
            for v in iter(vessels):
                self.the_DB[v]=vessels[0]
        
            menu_items= [(
                {
                    "viewclass": "OneLineListItem",
                    "text": f"{vessels[i]}",
                    "on_release": lambda x=f"{vessels[i]}": self.vessel_name(x)
                }) for i in range(len(vessels))
                ]

            self.menu = MDDropdownMenu(
                items= menu_items,
                width_mult=4
            )
            self.menu.caller = x
            self.menu.open()
            
        except ValueError:
            print("Error on choose vessel")


    def start_thread(self, vessel):
        self.button_state += 1
        self.x_thread = threading.Thread(target=self.change_vessel(vessel), daemon=True)
        self.x_thread.start()
        if not self.x_thread.is_alive() == True:
            try:
                self.button_state += 1
                
            except Exception as e:
                print(e)
                print("eror string 251")
        

    def name_of_tank(self, vessel_db):
        # Extract from DB names of each tank
        self.names = []
        db_reading.extract_names(vessel_db)

        self.tank_name = db_reading.name_of_tank
        for i in self.tank_name:
            self.names.append(i[0])


    def mdo_tank_extract(self, v):
        self.mdo_names = []
        db_reading.sort_tanks_mdo(v)
        self.mdo_tanks = db_reading.table_names_md
        for i in self.mdo_tanks:
            self.mdo_names.append(i[0])
        # print(self.mdo_names)


    def add_tab(self,vessel):
        
        names_for_do = list(set(self.mdo_names).intersection(set(self.names)))
        # print(names_for_do)
        self.tab_iterator = 0
        for i in (self.names):
            db_reading.extract_prev(i,vessel)
            
            if not i in names_for_do:
            
                self.root.get_screen('tab_screen').ids.tabs.add_widget(Tab(tab_label_text=f"{i}"))
            for do in names_for_do :
                if do == i:
                    self.root.get_screen('tab_screen').ids.tabs.add_widget(Tab(tab_label_text=f"{do} mdo"))
        try:
            if self.text_vessel==True:
                print(self.text_vessel)
                self.root.get_screen('tab_screen').ids.tabs.add_widget(
                    Tab(title=f"Previous quantity:\n{db_reading.prev_label_text[str(self.tank_name.text.removesuffix('mdo')).strip(' ')][0]} m3, at \
                    {db_reading.prev_label_text[str(self.tank_name.text.removesuffix('mdo')).strip(' ')][1]} cm")
                )

            else:
                self.root.get_screen('tab_screen').ids.tabs.add_widget(
                    Tab(title=f"Previous quantity: {prev_label_text}"))

        except AttributeError:
            self.root.get_screen('tab_screen').ids.tabs.add_widget(
                    Tab(title=f"Previous quantity: {prev_label_text}"))
            print("eror string 302")

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
        self.button_calc = instance_tab.ids.calc
        
        self.sound_value = instance_tab.ids.sound_field
        self.tank_name = instance_tab_label
        self.result = instance_tab.ids.label
        self.dens_new = instance_tab.ids.density_field
        if self.button_state > 0:
            self.button_calc.disabled = False
            self.root.get_screen("tab_screen").ids.select_vessel.text_color = 1, 1, 0.9, 1
        else:
            self.button_calc.disabled = True
            
            self.result.font_size = "30dp"
            self.result.text = "Select Vessel first"
            self.root.get_screen("tab_screen").ids.select_vessel.text_color ="#f43434"
        #if no any entries are inserted we show below text to user
        if len(total_list_mdo)==0 and len(total_list_hfo)==0:
            try:
                if self.text_vessel == True:
                    self.root.get_screen('tab_screen').ids.tabs.add_widget(
                        Tab(title=f"Previous quantity:\n{db_reading.prev_label_text[str(self.tank_name.text.removesuffix('mdo')).strip(' ')][0]} m3, at \
                        {db_reading.prev_label_text[str(self.tank_name.text.removesuffix('mdo')).strip(' ')][1]} cm")
                    )
                else:
                    self.root.get_screen('tab_screen').ids.tabs.add_widget(
                        Tab(title=f"Previous quantity: {prev_label_text}"))
            except Exception as e:
                # print(str(e) + " error string 346")
                pass
   

    def callback_Calc(self, *args):
        try:
            
            db_editing.calculation(str(self.tank_name.text.removesuffix('mdo')).strip(' '), self.sound_value.text, self.name_of_vessel_db)
            db_editing.type_sel(str(self.tank_name.text.removesuffix('mdo')).strip(' '), self.name_of_vessel_db)
            db_editing.state_sel(str(self.tank_name.text.removesuffix('mdo')).strip(' '), self.name_of_vessel_db)
            try:
                volume = str(db_editing.volume_in_m3[0])
            except IndexError:
                print("eror string 365")
                pass
            # If tank is in MDO state than we make calcs for it and append to
            # "total_list_mdo" for displaing in Totoal result screnn
            if db_editing.state_of_tank[0] ==1:

                try:
                    self.result.font_size = "30dp"
                    if db_editing.type_of_tank[0] == 1:
                        self.result.text=str(self.sound_value.text)
                        volume = self.result.text
                        self.temp_dens_extraction()
                        # Define below row for take into prev function use
                        total_list_mdo[str(self.tank_name.text.removesuffix('mdo')).strip(' ')] =  ((self.real_volume), self.sound_value.text, self.temperature, self.def_dens, volume)
                        self.result.text = str(self.sound_value.text) + str(" m3")

                    else:
                        self.result.text = str(db_editing.volume_in_m3[0])
                        self.temp_dens_extraction()
                        # Define below row for take into prev function use
                        total_list_mdo[str(self.tank_name.text.removesuffix('mdo')).strip(' ')] =  ((self.real_volume), self.sound_value.text, self.temperature, self.def_dens, volume)
                        self.result.text = str(db_editing.volume_in_m3[0]) + str(" m3")
                                
                

                    # Insert data to prev DB for prev values extarcting on start
                    if len(total_list_mdo) >0 :
                        print(total_list_hfo)
                        print("\n")
                        print(total_list_mdo)
                        print("********\n")
                        for i  in (total_list_mdo):
                            "     "
                            db_reading.add_to_prevdb(i, total_list_mdo[i][1], total_list_mdo[i][0], self.name_of_vessel_db)

                except IndexError as e:
                    # Printing on display the error and change the font-size
                    self.result.text = str("Wrong sounding value!")
                    self.result.font_size = "20dp"
                    print("eror string 406")
            # Calculate if tank is NOT MDO but is HFO
            else:
                
                try:
                    self.result.font_size = "30dp"

                    # If type of tank is not with sounding table,
                    # but only gauging than inputed value is added
                    # to total screen
                    if db_editing.type_of_tank[0] == 1:
                        self.result.text=str(self.sound_value.text)
                        volume = self.result.text
                        self.temp_dens_extraction()
                        # Define below row for take into prev function use
                        total_list_hfo[str(self.tank_name.text.removesuffix('mdo')).strip(' ')] =   ((self.real_volume), self.sound_value.text, self.temperature, self.def_dens, volume)
                        self.result.text = str(self.sound_value.text) + str(" m3")

                    else:
                        self.result.font_size = "30dp"
                        self.result.text = str(db_editing.volume_in_m3[0])
                        self.temp_dens_extraction() 

                        # Define below row for take into prev function use
                        total_list_hfo[str(self.tank_name.text.removesuffix('mdo')).strip(' ')] =   ((self.real_volume), self.sound_value.text, self.temperature, self.def_dens, volume)
                        self.result.text = str(db_editing.volume_in_m3[0]) + str(" m3")
                                
                

                    # Insert data to prev DB for prev values extarcting on start
                    if len(total_list_hfo) >0 :
                        print(total_list_hfo)
                        print("\n")
                        print(total_list_mdo)
                        print("*************\n")
                        for i  in (total_list_hfo):
                            db_reading.add_to_prevdb(i, total_list_hfo[i][1], total_list_hfo[i][0], self.name_of_vessel_db)
                            # print(f"Data insert in {i} with sound = {total_list[i][1]} and volume ={total_list[i][0]} , deleted value is = { total_list} ")

                except IndexError as e:
                    # Printing on display the error and change the font-size
                    self.result.text = str("Wrong sounding value!")
                    self.result.font_size = "20dp"
        except AttributeError as e:
            self.root.get_screen("tab_screen").ids.select_vessel.text = "Select the vessel first"
            print(str("error string 451"))
        
    def my_value(self, *args):  # <<<<<<<<<<< Value from Temp slider
        try:
            # self.slider_value={}
            self.slider_value[str(self.tank_name.text.removesuffix('mdo')).strip(' ')] = round(int((args[1])),0)
        except Exception as e:
            print(str(e) +str("error string 458"))
        return self.slider_value

    def temp_dens_extraction(self):
            try:
                try:
                    if len(self.slider_value) !=0 :
                        self.temperature = str(self.slider_value[str(self.tank_name.text.removesuffix('mdo')).strip(' ')])
                    else:
                        self.temperature = def_temp
                        print('else')
                except Exception as e:
                    self.temperature = def_temp
                    print(str(e) +str(" string 486"))
                # Density selecting
                if len(self.dens_new.text) == 0:
                    # If density is not inputed by user than we collect it from
                    # database
                    self.def_dens = db_editing.select_DefDens(str(self.tank_name.text.removesuffix('mdo')).strip(' '), self.name_of_vessel_db)

                else:
                    # if is inputed than put that what user inputed
                    if float(self.dens_new.text) >= 1.1:
                        try:
                            self.dens_new.hint_text = "Wrong Density"
                            self.dens_new.text_color_normal = "#ff2233"
                        except Exception as e:
                            print(e)
                            print("HERE")
                            
                    else:
                        self.dens_new.hint_text = "Density (example: 0.9588)"
                        self.dens_new.text_color_normal = 1, 1, 0.8, 1
                        self.def_dens = self.dens_new.text
                

            except AttributeError as e:
                self.temperature = def_temp
                print("eror string 490 " + str(e))
                if len(self.dens_new.text) == 0:
                    # If density is not inputed by user than we collect it from
                    # database
                    self.def_dens = db_editing.select_DefDens(str(super.tank_name.text.removesuffix('mdo')).strip(' '), super.name_of_vessel_db)
                else:
                    # if is inputed than put that what user inputed
                    if float(self.dens_new.text) >= 1.1:
                        try:
                            self.dens_new.hint_text = "Wrong Density"
                            self.dens_new.text_color_normal = "#ff2233"
                        except Exception as e:
                            print(e)
                            print("eror string 498")
                    else:
                        self.dens_new.hint_text = "Density (example: 0.9588)"
                        self.dens_new.text_color_normal = 1, 1, 0.8, 1
                        self.def_dens = self.dens_new.text
            except KeyError as e:
                self.temperature = def_temp
                print("eror string 513 Keyerror=" +str(e) )
                if len(self.dens_new.text) == 0:
                    # If density is not inputed by user than we collect it from
                    # database
                    self.def_dens = db_editing.select_DefDens(str(super.tank_name.text.removesuffix('mdo')).strip(' '), super.name_of_vessel_db)
                else:
                    # if is inputed than put that what user inputed
                    if float(self.dens_new.text) >= 1.1:
                        try:
                            self.dens_new.hint_text = "Wrong Density"
                            self.dens_new.text_color_normal = "#ff2233"
                        except Exception as e:
                            print(e)
                            print("eror string 526")
                    else:
                        self.dens_new.hint_text = "Density (example: 0.9588)"
                        self.dens_new.text_color_normal = 1, 1, 0.8, 1
                        self.def_dens = self.dens_new.text

            try:
                self.converted_density = ((float(self.def_dens)/2)*1000)*2       
                
            except Exception as e:
                print(e)
                print("eror string 538")
            vol_coorection.vol_correction_factor_calc(self.converted_density, self.result.text, int(self.temperature))
            self.real_volume = vol_coorection.result
            return self.temperature, self.def_dens, self.real_volume


if __name__ == "__main__":
    BunkerCalc().run()
