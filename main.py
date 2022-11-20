import db_reading
import db_editing

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.icon_definitions import md_icons
from kivymd.uix.button import MDFlatButton
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.menu import MDDropdownMenu

import sqlite3

# Window resizing. To be deleted before compiling
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase

import db_editing
import db_reading

Window.size = (360, 600)

total_list={}

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

sm = ScreenManager()
sm.add_widget(TabScreen(name='tab_screen'))
sm.add_widget(TotalScreen(name='total_screen'))


class BunkerCalc(MDApp):

    def build(self):

        # Theme and colors
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.primary_hue = "600"
        self.theme_cls.theme_style = "Dark"

    def dropdown(self, instance):
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
        self.menu.caller = instance
        self.menu.open()

    def screen2(self):

        self.root.current = "total_screen"
        self.root.get_screen("total_screen").ids.total.text=str(total_list)

    def screen1(self):

        self.root.current = "tab_screen"

    def name_of_tank(self):
        # Extract from DB names of each tank
        self.names = []
        db_reading.extract_names()

        self.tank_name = db_reading.name_of_tank
        for i in self.tank_name:
            self.names.append(i[0])

    def add_tab(self):

        for i in (self.names):
            self.root.get_screen('tab_screen').ids.tabs.add_widget(Tab(tab_label_text=f"{i}"))

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

    def callback_Calc(self, sound):

        db_editing.calculation(self.tank_name.text, self.sound_value.text)
        try:
            self.result.font_size = "60dp"
            self.result.text = str(db_editing.volume_in_m3[0])
            total_list[self.tank_name.text]=(self.result.text)
            self.result.text = str(db_editing.volume_in_m3[0]) + str(" m3")


        except IndexError as e:
            # Printing on display the error and change the font-size
            self.result.text = str("Wrong sounding value!")
            self.result.font_size = "20dp"

    def on_start(self):

        self.name_of_tank()

        self.add_tab()


if __name__ == "__main__":
    BunkerCalc().run()
