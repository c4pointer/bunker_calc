"""
Planing to put here the calculation metod from BunkerCalc class
"""

import db_editing
import vol_coorection

from main import def_temp
from main import BunkerCalc

from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.datatables import MDDataTable


class Example(BunkerCalc):
    def build(self):
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.primary_hue = "600"
        self.theme_cls.theme_style = "Dark"
        self.table = MDDataTable(
                size_hint=(0.7, 0.6),
                use_pagination=True,
                check=True,
                # name column, width column, sorting function column(optional)
                column_data=[
                    ("No.", dp(30)),
                    ("Status", dp(30)),
                    ("Signal Name", dp(60)),
                    ("Severity", dp(30)),
                    ("Stage", dp(30)),
                    ("Schedule", dp(30),
                     lambda *args: print("Sorted using Schedule")),
                    ("Team Lead", dp(30)),
                ],
            )
            
        
