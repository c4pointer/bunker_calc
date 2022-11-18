import db_reading
import db_editing

import kivy

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.icon_definitions import md_icons
from kivymd.uix.button import MDFlatButton
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen

import sqlite3



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
            self.root.ids.tabs.add_widget(Tab(tab_label_text=f"{i}"))

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

        self.sound_value= instance_tab.ids.sound_field
        self.tank_name = instance_tab_label
        self.result = instance_tab.ids.label

    def callback_Calc(self, er):

        db_editing.calculation(self.tank_name.text, self.sound_value.text)
        try:
            self.result.text = str(db_editing.volume_in_m3[0]) + str(" m3")
        except IndexError as e:
            self.result.text = str(e)
        # r = (self.root.ids.tabs.get_tab_list())
        # print(r)


if __name__ == "__main__":
    BunkerCalc().run()
