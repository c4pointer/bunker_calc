from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivymd.uix.button import MDFillRoundFlatIconButton, MDFillRoundFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp

import os
import sqlite3
file_location_detect=os.getcwd()
conn=sqlite3.connect('Bunker_calc1.db')
cur=conn.cursor()
import insert_in_db
import db_commands_calc
import mdo_tanks

class ConverterApp(MDApp):
    def flip(self):
        # a function for the "flip" icon
        # changes the state of the app
        if self.state == 0:
            self.state = 1
            self.toolbar.title = "Banker Calc"
            self.input.text = "enter a decimal number"
        else:
            self.state = 0
            self.toolbar.title = "Banker Calc"
            self.input.text = "enter a binary number"
        # hide labels until needed
        self.converted.text = ""
        self.label.text = ""

    # def convert(self, args):
    #     # a function to fint the decimal/binary equivallent
    #     if self.state == 0:
    #         # binary to decimal
    #         val = str(int(self.input.text,2))
    #         self.label.text = "in decimal is:"
    #     else:
    #         # decimal to binary
    #         val = bin(int(self.input.text))[2:]
    #         self.label.text = "in binary is:"
    #     self.converted.text = val

    def build(self):
        self.state = 0 #initial state
        self.theme_cls.primary_palette = "DeepOrange"
        screen = MDScreen()

        # top toolbar
        self.toolbar = MDToolbar(title="Banker Calc")
        self.toolbar.pos_hint = {"top": 1}
        self.toolbar.right_action_items = [
            ["rotate-3d-variant", lambda x: self.flip()]]
        screen.add_widget(self.toolbar)

        # logo
        # screen.add_widget(Image(
        #     source="logo.png",
        #     pos_hint = {"center_x": 0.5, "center_y":0.7}
        #     ))

        #collect user input
        # self.input = MDTextField(
        #     text="",
        #     halign="center",
        #     size_hint = (2,2),
        #     pos_hint = {"center_x": 0.5, "center_y":0.5},
        #     font_size = 22
        # )
        # screen.add_widget(self.input)
        
        # #secondary + primary labels
        # self.label = MDLabel(
        #     halign="center",
        #     pos_hint = {"center_x": 0.5, "center_y":0.35},
        #     theme_text_color = "Secondary"
        # )

        # self.converted = MDLabel(
        #     halign="center",
        #     pos_hint = {"center_x": 0.5, "center_y":0.3},
        #     theme_text_color = "Primary",
        #     font_style = "H5"
        # )
        # screen.add_widget(self.label)
        # screen.add_widget(self.converted)

        # "CONVERT" button
        # screen.add_widget(MDFillRoundFlatButton(
        #     text="CONVERT",
        #     font_size = 17,
        #     pos_hint = {"center_x": 0.5, "center_y":0.15},
        #     # on_press = self.convert
        # ))

        self.table = MDDataTable(
                # MDDataTable allows the use of size_hint
                size_hint=(0.99, 0.935),
                use_pagination=True,
                rows_num=20,
                check=True,
                column_data=[
                    ("No.", dp(20)),
                    ("Name of Tank", dp(25)),
                    ("Total Vol", dp(20)),
                    ("Sound Val", dp(20)),
                    ("Volume", dp(20)),
                    ("Density", dp(20)),
                    ("Temp", dp(20)),
                    ("MT", dp(20)),
                    ],
                row_data=[
                        (
                            f"{i+1}",
                            "[color=#53351B]Name of tank[/color]",
                            "[color=#55551B]Total Vol[/color]",
                            "[color=#52251B]Sound Val[/color]",
                            "[color=#52251B]Volume[/color]",
                            "[color=#52251B]Density[/color]",
                            "[color=#52251B]Temp[/color]",
                            "[color=#52251B]m3[/color]",
                        )
                        for i in range(12)

                        # ("1", ("alert", [255 / 256, 165 / 256, 0, 1], "No Signal"),
                        #     "Astrid: NE shared managed", "Medium", "Triaged", "0:33",
                        #     "Chase Nguyen"),
                        # ("2", ("alert-circle", [1, 0, 0, 1], "Offline"),
                        #     "Cosmo: prod shared ares", "Huge", "Triaged", "0:39",
                        #     "Brie Furman"),
                        # ("3", (
                        #     "checkbox-marked-circle",
                        #     [39 / 256, 174 / 256, 96 / 256, 1],
                        #     "Online"), "Phoenix: prod shared lyra-lists", "Minor",
                        #     "Not Triaged", "3:12", "Jeremy lake"),
                        # ("4", (
                        #     "checkbox-marked-circle",
                        #     [39 / 256, 174 / 256, 96 / 256, 1],
                        #     "Online"), "Sirius: NW prod shared locations",
                        #     "Negligible",
                        #     "Triaged", "13:18", "Angelica Howards"),
                        # ("5", (
                        #     "checkbox-marked-circle",
                        #     [39 / 256, 174 / 256, 96 / 256, 1],
                        #     "Online"), "Sirius: prod independent account",
                        #     "Negligible",
                        #     "Triaged", "22:06", "Diane Okuma"),
                        

                ],

        )
        screen.add_widget(self.table)

        return screen


if __name__ == '__main__':
    ConverterApp().run()
