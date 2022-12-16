# Window resizing. To be deleted before compiling
# from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty

import db_editing
import db_reading
from collections import ChainMap
# Window.size = (400, 600)

total_list = {}


prev_label_text = {}

vessels = ("m/v 'Viking Ocean'",)


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
                "on_release": lambda x="Tanks Sounding": self.screen1()
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
        self.total_result = []
        self.sum = 0
        for i in (self.names):
            try:
                if len(total_list[i]) > 0:
                    self.total_result.append(total_list[i])

            except KeyError as err:
                pass
        
        for i in self.total_result:
            print(i[0])
            self.sum += float(i[0])
        return self.sum

    def screen2(self):
        """
        Go to total screen where is shown total figure
        At each time when "total_screen" is pressed is recalculated
        total figure
        """
        self.root.current = "total_screen"
        self.calculate_total()
        self.root.get_screen("total_screen").ids.total.text = str(round(self.sum, 3)) + str(" m3")

    def screen1(self):
        self.root.current = "tab_screen"


    def vessel_name(self):
        self.vessel = self.root.get_screen("tab_screen").ids.top_menu.title = vessels[0]
        self.set_vessel_name()

    def set_vessel_name(self):
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
        
        
        #if no any entries are inserted we show below text to user
        if len(total_list)==0:
            try:
                self.result.text = str("Previous quantity:\n")+\
                str(db_reading.prev_label_text[str(self.tank_name.text.removesuffix('mdo')).strip(' ')][0])+ \
                str(" m3, at ") + str(db_reading.prev_label_text[str(self.tank_name.text.removesuffix('mdo')).strip(' ')][1])+ str("cm")
                self.result.font_size = "30dp"
                db_editing.type_sel(tab_text)

            except :
                pass

    def callback_Calc(self, *args):

        db_editing.calculation(str(self.tank_name.text.removesuffix('mdo')).strip(' '), self.sound_value.text)
        db_editing.type_sel(str(self.tank_name.text.removesuffix('mdo')).strip(' '))
        if db_editing.type_of_tank[0] == 1:
            self.sound_value.text
            print(self.sound_value.text)
        try:
            self.result.font_size = "60dp"
            if db_editing.type_of_tank[0] == 1:
                self.result.text=str(self.sound_value.text)
                total_list[str(self.tank_name.text.removesuffix('mdo')).strip(' ')] = ((self.result.text), self.sound_value.text)
                self.result.text = str(self.sound_value.text) + str(" m3")
                print(str(self.tank_name.text.removesuffix('mdo')).strip(' '))
            else:
                self.result.font_size = "60dp"
                self.result.text = str(db_editing.volume_in_m3[0])

                # Define below row for take into prev function use
                total_list[str(self.tank_name.text.removesuffix('mdo')).strip(' ')] = ((self.result.text), self.sound_value.text)
                self.result.text = str(db_editing.volume_in_m3[0]) + str(" m3")
                            
            

            # Insert data to prev DB for prev values extarcting on start
            if len(total_list) >0 :
                # print(total_list)
                for i  in (total_list):
                    db_reading.add_to_prevdb(i, total_list[i][1], total_list[i][0])
                    # print(f"Data insert in {i} with sound = {total_list[i][1]} and volume ={total_list[i][0]} , deleted value is = { total_list} ")

        except IndexError as e:
            # Printing on display the error and change the font-size
            self.result.text = str("Wrong sounding value!")
            self.result.font_size = "20dp"
    
    def on_start(self):

        self.name_of_tank()
        self.mdo_tank_extract()
        self.vessel_name()
        self.add_tab()
    




if __name__ == "__main__":
    BunkerCalc().run()
