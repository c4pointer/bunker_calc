import db_reading
import db_editing

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.icon_definitions import md_icons
from kivymd.uix.button import MDFlatButton
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen

import threading
import sqlite3
import os

# file_location_detect = os.getcwd()
# try:
#     name_off_app = "BunkerCalc"
#     conn = sqlite3.connect(
#         (file_location_detect+'/Documents/myapp/Bunker_calc.db'), check_same_thread=False)
# except sqlite3.OperationalError as e:
#     name_off_app = "BunkerCalc"
#     conn = sqlite3.connect(
#         (file_location_detect+'/Bunker_calc.db'), check_same_thread=False)
# cur = conn.cursor()


class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''

# class Tab(MDLabel, MDTabsBase):
#     '''Class implementing content for a tab.'''


class Store_Values():

    def __init__(self, sound, tk_name):
        self.sound = sound
        self.tk_name = tk_name


class BunkerCalc(MDApp):

    def build(self):

        # Theme and colors
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.primary_hue = "600"
        self.theme_cls.theme_style = "Light"

        # screen = Screen()

        screen = Builder.load_file("bunker_calc.kv")

        return screen

    def name_of_tank(self):
        self.names = []
        db_reading.extract_names()

        self.tank_name = db_reading.name_of_tank
        for i in self.tank_name:
            self.names.append(i[0])

    def on_start(self):
            self.name_of_tank()
            self.add_tab()

    # def get_tab_list(self):
    #     '''Prints a list of tab objects.'''

    #     print(self.root.ids.tabs.get_tab_list())

    def add_tab(self):

        for i in (self.names):
            self.root.ids.tabs.add_widget(Tab(text=f"{i}"))

    def on_tab_switch(
        self, instance_tabs, instance_tab, instance_tab_label, tab_text
    ):
        '''Called when switching tabs.

        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        '''

        instance_tab.ids.sound_field.hint_text = "Sounding value :"

        self.x = instance_tab.ids.sound_field
        self.y = instance_tab_label
        self.z = instance_tab.ids.label

    def callback_Calc(self, er):

        db_editing.calculation(self.y.text, self.x.text)
        self.z.text = db_editing.volume_in_m3[0]
        r = (self.root.ids.tabs.get_tab_list())
        #for i in range(len(r)):
        #    print(i)


BunkerCalc().run()
