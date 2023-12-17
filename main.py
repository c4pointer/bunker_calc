import logging
import os
import threading
from logging import Logger
import traceback

from kivy import platform
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.tab import MDTabsBase

import create_vessel
# import file from project
import db_editing
import db_reading
import vol_coorection

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(module)s - - %(lineno)d  - %(message)s", filename='mylog.log',
    level=logging.WARNING,  # %(pathname)s

)
logger: Logger = logging.getLogger(__name__)

## Window resizing. To be deleted or commented before compiling
# from kivy.core.window import Window
# Window.size = (400, 700)

if platform == "android":
    from android.permissions import request_permissions, Permission

    request_permissions(
        [Permission.WRITE_EXTERNAL_STORAGE,
         Permission.READ_EXTERNAL_STORAGE])

    from android.storage import primary_external_storage_path

    SD_CARD = primary_external_storage_path()

# Here we store our dict with total quantity of fuel
tank_total_hfo = []
tank_total_mdo = []

# Default variables
def_temp = int(15)  # The conventional Default temperature for calculating fuel
vessel_db = "viking_ocean.db"  # deafault vessel for build primary structure of App

prev_label_text = {}

file_location_detect = os.getcwd()


class Tank:
    def __init__(self, name, metric_tons, measurement, temp, density, volume):
        self.name = name
        self.metric_tons = metric_tons
        self.measurement = measurement
        self.temp = temp
        self.density = density
        self.volume = volume

    @staticmethod
    def add_tank_to_list(tank, tank_list):
        names = {t.name for t in tank_list}
        if tank.name in names:
            tank_list[:] = [t for t in tank_list if t.name != tank.name]
        tank_list.append(tank)
        return True

    def add_tank_hfo(self):
        return self.add_tank_to_list(self, tank_total_hfo)

    def add_tank_mdo(self):
        return self.add_tank_to_list(self, tank_total_mdo)


# Screens
class TabScreen(Screen):
    pass


class TotalScreen(Screen):
    pass


class AdminScreen(Screen):
    pass


class NewVesselScreen(Screen):
    pass


class AddTankScreen(Screen):
    pass


class DelVesselScreen(Screen):
    pass


class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''


class BunkerCalc(MDApp):

    def build(self):
        # Theme and colors
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.primary_hue = "600"
        self.theme_cls.theme_style = "Dark"

    def on_start(self):
        # Dict for storing all vessel sounding table data
        self.the_DB = {}
        self.the_DB_admin = {}
        # Calculation button state is Disabled
        self.button_state = 0
        self.name_of_tank(vessel_db)
        self.mdo_tank_extract(vessel_db)
        self.add_tab(vessel_db)
        self.slider_value = {}
        self.j = 0
        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
        # Label for toggle screens between the total screen and Tabs
        screen = self.root.get_screen("tab_screen")
        screen.ids.right_action.text = "Sounding Screen"
        screen.ids.select_vessel.text = "Select vessel"

    def change_vessel(self, vessel):
        try:
            tabs = self.root.get_screen('tab_screen').ids.tabs.get_tab_list()
            for i in tabs:
                self.root.get_screen("tab_screen").ids.tabs.remove_widget(i)
            try:
                self.name_of_tank(vessel)
                self.mdo_tank_extract(vessel)
                self.add_tab(vessel)
            except Exception as error:
                logger.debug(traceback.format_exc())
        except Exception as error:
            logger.debug(traceback.format_exc())

    def calculate_total(self):
        # Calculate the total m3 in our "total_list"
        self.mdo_tons = []
        self.hfo_tons = []
        # HFO
        self.sum_hfo = 0
        self.sum_hfo_tons = 0
        # MDO
        self.sum_mdo = 0
        self.sum_mdo_tons = 0

        for tank in tank_total_hfo:
            self.sum_hfo += float(tank.volume)
            self.sum_hfo_tons += float(tank.metric_tons)

        for tank in tank_total_mdo:
            self.sum_mdo += float(tank.volume)
            self.sum_mdo_tons += float(tank.metric_tons)

        if len(self.hfo_tons) == 0:
            self.hfo_tons.append(float(0))
        if len(self.mdo_tons) == 0:
            self.mdo_tons.append(float(0))
        return self.sum_mdo, self.sum_hfo, self.hfo_tons, self.mdo_tons, self.sum_mdo_tons, self.sum_hfo_tons

    def screen2(self):
        """
        Go to the total screen where the total figure is shown.
        Each time "total_screen" is pressed, the total figure is recalculated.
        """
        current_screen = self.root.current

        if current_screen != "total_screen":
            if current_screen == "tab_screen":
                self.root.current = "total_screen"
                self.calculate_total()
                # Display total results for MDO and HFO
                total_screen = self.root.get_screen("total_screen")
                total_screen.ids.right_action.text = "Total Screen"
                total_screen.ids.total_hfo.text = (
                    f"{round(self.sum_hfo, 3)} m3 HFO\n"
                    f"{round(self.sum_hfo_tons, 2)} MT HFO\n___________________"
                )
                total_screen.ids.total_mdo.text = (
                    f"{round(self.sum_mdo, 3)} m3 MDO\n"
                    f"{round(self.sum_mdo_tons, 2)} MT MDO"
                )
            else:
                self.root.current = "tab_screen"
        else:
            self.root.current = "tab_screen"

    def vessel_name(self, vessel_name):
        """
        Set the selected vessel as the title of the App.
        """
        try:
            self.name_of_vessel_db = f"{vessel_name.lower()}.db"  # Name of DB if it is non-default

            # THREAD FOR selecting and switching vessel DB
            self.start_thread(self.name_of_vessel_db)

            if len(self.the_DB) != 0:
                self.vessel = str(vessel_name)
                self.root.get_screen("tab_screen").ids.top_menu.title = str(vessel_name).replace("_", ' ')
                self.menu.dismiss()

            self.root.get_screen("total_screen").ids.total_menu_total.title = str(vessel_name)
        except Exception as error:
            logger.warning(f"Vessel name method - {error} : {traceback.format_exc()}")

    def choose_vessel(self, x):
        """
        Create a dropdown menu for selecting the Vessel's Database.
        """
        vessel_name_db = []
        self.the_DB = {}
        vessels = []
        file_location_detect = os.getcwd()

        try:
            # Scan current working Directory
            scan_dir = os.listdir(file_location_detect)
            for file in scan_dir:
                if not file.endswith('_prev.db') and file.endswith(".db"):
                    parsed_vessel = os.path.splitext(file)[0].title()
                    vessel_name_db.append(parsed_vessel)
                    vessels.append(parsed_vessel)
        except Exception as error:
            logger.warning(f"Choose vessel files function - {error} : {traceback.format_exc()}")

        try:
            self.root.get_screen("tab_screen").ids.select_vessel.text = "Vessel"
            self.db_tuple = {}

            for vessel in iter(vessels):
                self.the_DB[vessel] = vessels[0]

            menu_items = [
                {
                    "viewclass": "OneLineListItem",
                    "text": f"{vessels[i]}",
                    "on_release": lambda x=f"{vessels[i]}": self.vessel_name(x)
                } for i in range(len(vessels))
            ]

            self.menu = MDDropdownMenu(
                items=menu_items,
                width_mult=4
            )
            self.menu.caller = x
            self.menu.open()

        except ValueError as error:
            logger.warning(f"Create a dropdown menu - {error} : {traceback.format_exc()}")

    def start_thread(self, vessel):
        self.button_state += 1
        self.x_thread = threading.Thread(target=self.change_vessel(vessel), daemon=True)
        self.x_thread.start()

        if not self.x_thread.is_alive():
            try:
                self.button_state += 1
            except Exception as error:
                logger.debug(traceback.format_exc())

    def name_of_tank(self, vessel_db):
        """
        Extract tank names from the database.
        """
        try:
            self.names = []
            extract_name = db_reading.extract_names(vessel_db)
            self.tank_name = extract_name
            self.names = [i[0] for i in self.tank_name]
        except Exception as error:
            self.root.get_screen("tab_screen").ids.top_menu.title = "No DATA in Vessel database"
            logger.debug(traceback.format_exc())

    def mdo_tank_extract(self, v):
        """
        Extract MDO tank names from the database.
        """
        self.mdo_names = []
        sorted_tank = db_reading.sort_tanks_mdo(v)
        self.mdo_tanks = sorted_tank
        self.mdo_names = [i[0] for i in self.mdo_tanks]

    def add_tab(self, vessel):
        try:
            names_for_do = list(set(self.mdo_names).intersection(set(self.names)))
            # print(names_for_do)
            self.tab_iterator = 0
            for i in (self.names):
                prev_names = db_reading.extract_prev(i, vessel)

                if not i in names_for_do:
                    self.root.get_screen('tab_screen').ids.tabs.add_widget(Tab(tab_label_text=f"{i}"))
                for do in names_for_do:
                    if do == i:
                        self.root.get_screen('tab_screen').ids.tabs.add_widget(Tab(tab_label_text=f"{do} mdo"))

            # afetr add text to label of first tab we delete here the last widget that is non-correct
            self.root.get_screen('tab_screen').ids.tabs.remove_widget(
                self.root.get_screen('tab_screen').ids.tabs.get_tab_list()[-1]
            )
        except Exception as error:
            logger.warning(f"Exception in add tab - {error} : {traceback.format_exc()}")

    def on_tab_switch(
            self, instance_tabs, instance_tab, instance_tab_label, tab_text
    ):
        '''Called when switching tabs.

        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        '''
        self.sound_filed_help = instance_tab.ids.sound_field
        instance_tab.ids.sound_field.text_color_normal = 1, 1, 0.8, 1
        self.button_calc = instance_tab.ids.calc
        self.text_vessel = self.root.get_screen("tab_screen").ids.top_menu.title
        self.sound_value = instance_tab.ids.sound_field
        self.tank_name = instance_tab_label
        self.result = instance_tab.ids.label
        self.dens_new = instance_tab.ids.density_field
        self.result_mt = instance_tab.ids.label_mt
        self.result_mt.font_size = "20dp"
        self.hint_text = instance_tab.ids.sound_field
        if self.button_state > 0:
            self.button_calc.disabled = False
            self.root.get_screen("tab_screen").ids.select_vessel.text_color = 1, 1, 0.9, 1
        else:
            self.button_calc.disabled = True
            self.result.font_size = "30dp"
            self.result.text = "Select Vessel first"
            self.root.get_screen("tab_screen").ids.select_vessel.text_color = "#f43434"

        if not self.result.text == "Select Vessel first":
            try:
                if self.text_vessel:
                    self.sound_filed_help.hint_text = f"Prev quant:\n{db_reading.prev_label_text[str(self.tank_name.text.removesuffix('mdo')).strip(' ')][0]} m3, at {db_reading.prev_label_text[str(self.tank_name.text.removesuffix('mdo')).strip(' ')][1]} cm"
                else:
                    self.sound_filed_help.hint_text = f"Prev quant:\n{db_reading.prev_label_text[str(self.tank_name.text.removesuffix('mdo')).strip(' ')][0]} m3, at {db_reading.prev_label_text[str(self.tank_name.text.removesuffix('mdo')).strip(' ')][1]} cm"
            except Exception as error:
                logger.warning(f"On tab switch method - {error} : {traceback.format_exc()}")

    def callback_Calc(self, *args):
        try:
            calculations = db_editing.calculation(
                str(self.tank_name.text.removesuffix('mdo')).strip(' '),
                self.sound_value.text,
                self.name_of_vessel_db)
            type_selected = db_editing.type_sel(
                str(self.tank_name.text.removesuffix('mdo')).strip(' '), self.name_of_vessel_db)
            state_selected = db_editing.state_sel(
                str(self.tank_name.text.removesuffix('mdo')).strip(' '), self.name_of_vessel_db)
            try:
                volume = str(calculations[0])
            except IndexError as error:
                logger.debug(traceback.format_exc())
            # If tank is in MDO state than we make calcs for it and append to
            # "total_list_mdo" for displaying in Total result screen
            if state_selected[0] == 1:
                try:
                    self.result.font_size = "30dp"
                    if type_selected[0] == 1:
                        self.result.text = str(self.sound_value.text)
                        volume = self.result.text
                        self.temp_dens_extraction()
                        self.result.text = str(self.sound_value.text) + str(" m3")
                        tank_vessel = Tank(str(self.tank_name.text.removesuffix('mdo')).strip(' '), (self.real_volume),
                                           self.sound_value.text, self.temperature, self.def_dens, volume)
                        # vessel_class = Vessel(self.name_of_vessel_db)
                        tank_vessel.add_tank_mdo()

                    else:
                        self.result.text = str(calculations[0])
                        self.temp_dens_extraction()
                        # Define below row for take into prev function use
                        self.result.text = str(calculations[0]) + str(" m3")
                        tank_vessel = Tank(str(self.tank_name.text.removesuffix('mdo')).strip(' '), (self.real_volume),
                                           self.sound_value.text, self.temperature, self.def_dens, volume)
                        # vessel_class = Vessel(self.name_of_vessel_db)
                        tank_vessel.add_tank_mdo()
                    # Insert data to prev DB for prev values extarcting on start
                    if tank_vessel:
                        db_reading.add_to_prevdb(
                            tank_vessel.name, tank_vessel.measurement, tank_vessel.volume,
                            self.name_of_vessel_db)

                except IndexError as error:
                    # Printing on display the error and change the font-size
                    self.result.text = str("Wrong sounding value!")
                    self.result.font_size = "20dp"
                    logger.debug(traceback.format_exc())
            # Calculate if tank is NOT MDO but is HFO
            else:
                try:
                    self.result.font_size = "30dp"
                    # If type of tank is not with sounding table,
                    # but only gauging than inputted value is added
                    # to total screen
                    if type_selected[0] == 1:
                        self.result.text = str(self.sound_value.text)
                        volume = self.result.text
                        self.temp_dens_extraction()
                        # Define below row for take into prev function use
                        self.result.text = str(self.sound_value.text) + str(" m3")
                        tank_vessel = Tank(str(self.tank_name.text.removesuffix('mdo')).strip(' '), (self.real_volume),
                                           self.sound_value.text, self.temperature, self.def_dens, volume)
                        # vessel_class = Vessel(self.name_of_vessel_db)
                        tank_vessel.add_tank_hfo()
                    else:
                        self.result.font_size = "30dp"
                        self.result.text = str(calculations[0])
                        self.temp_dens_extraction()

                        # Define below row for take into prev function use
                        self.result.text = str(calculations[0]) + str(" m3")
                        tank_vessel = Tank(str(self.tank_name.text.removesuffix('mdo')).strip(' '), (self.real_volume),
                                           self.sound_value.text, self.temperature, self.def_dens, volume)
                        # vessel_class = Vessel(self.name_of_vessel_db)
                        tank_vessel.add_tank_hfo()
                    # Insert data to prev DB for prev values extracting on start
                    if tank_vessel:
                        db_reading.add_to_prevdb(
                            tank_vessel.name, tank_vessel.measurement, tank_vessel.volume,
                            self.name_of_vessel_db)
                except IndexError as error:
                    # Printing on display the error and change the font-size
                    self.result.text = str("Wrong sounding value!\nRecheck")
                    self.result.font_size = "20dp"
                    logger.debug(traceback.format_exc())
            self.sound_filed_help.hint_text = "Sounding value (cm):"
        except AttributeError as error:
            self.root.get_screen("tab_screen").ids.select_vessel.text = "Select the vessel first"
            logger.debug(traceback.format_exc())

    def my_value(self, *args):  # Value from Temp slider
        try:
            self.slider_value[str(self.tank_name.text.removesuffix('mdo')).strip(' ')] = round(int((args[1])), 0)
        except Exception as error:
            logger.debug(traceback.format_exc())
            pass
        return self.slider_value

    def temp_dens_extraction(self):
        try:
            try:
                if len(self.slider_value) != 0:
                    self.temperature = str(self.slider_value[str(self.tank_name.text.removesuffix('mdo')).strip(' ')])
                else:
                    # if temperature was not selected than default temperature is applied
                    self.temperature = def_temp
            except Exception as error:
                self.temperature = def_temp
            # Density selecting
            if len(self.dens_new.text) == 0:
                # If density is not inputed by user than we collect it from
                # database
                self.def_dens = db_editing.select_DefDens(
                    str(self.tank_name.text.removesuffix('mdo')).strip(' '),
                    self.name_of_vessel_db)

            else:
                # if is inputted than put that what user inputted
                if float(self.dens_new.text) >= 1.1:
                    try:
                        self.dens_new.hint_text = "Wrong Density"
                        self.dens_new.text_color_normal = "#ff2233"
                    except Exception as error:
                        logger.debug(traceback.format_exc())
                else:
                    self.dens_new.hint_text = "Density (example: 0.9588)"
                    self.dens_new.text_color_normal = 1, 1, 0.8, 1
                    self.def_dens = self.dens_new.text
        except AttributeError as error:
            self.temperature = def_temp
            if len(self.dens_new.text) == 0:
                # If density is not inputted by user than we collect it from
                # database
                self.def_dens = db_editing.select_DefDens(
                    str(super.tank_name.text.removesuffix('mdo')).strip(' '),
                    super.name_of_vessel_db)
            else:
                # if is inputted than put that what user inputted
                if float(self.dens_new.text) >= 1.1:
                    try:
                        self.dens_new.hint_text = "Wrong Density"
                        self.dens_new.text_color_normal = "#ff2233"
                    except Exception as error:
                        logger.debug(traceback.format_exc())

                else:
                    self.dens_new.hint_text = "Density (example: 0.9588)"
                    self.dens_new.text_color_normal = 1, 1, 0.8, 1
                    self.def_dens = self.dens_new.text
        except KeyError as error:
            self.temperature = def_temp
            if len(self.dens_new.text) == 0:
                # If density is not inputted by user than we collect it from
                # database
                self.def_dens = db_editing.select_DefDens(
                    str(super.tank_name.text.removesuffix('mdo')).strip(' '),
                    super.name_of_vessel_db)
            else:
                # if is inputted than put that what user inputted
                if float(self.dens_new.text) >= 1.1:
                    try:
                        self.dens_new.hint_text = "Wrong Density"
                        self.dens_new.text_color_normal = "#ff2233"
                    except Exception as error:
                        logger.debug(traceback.format_exc())
                else:
                    self.dens_new.hint_text = "Density (example: 0.9588)"
                    self.dens_new.text_color_normal = 1, 1, 0.8, 1
                    self.def_dens = self.dens_new.text
        try:
            self.converted_density = ((float(self.def_dens) / 2) * 1000) * 2
        except Exception as error:
            logger.debug(traceback.format_exc())
        vol_ = vol_coorection.vol_correction_factor_calc(
            self.converted_density, self.result.text, int(self.temperature))
        self.real_volume = vol_
        self.result_mt.text = f"{str(self.real_volume)} mt"
        return self.temperature, self.def_dens, self.real_volume

    def admin_panel(self):
        self.vessel_name_db = []
        self.vessels_admin = []
        self.db_tuple_admin = {}
        self.root.current = "admin_screen"
        self.root.get_screen("add_tank_screen").ids.drop_vessels.text = "Choose vessel"
        self.root.get_screen("del_vessel_screen").ids.drop_vessels.text = "Choose vessel"

    def create_vessel(self, name):
        # Create new Vessel database
        try:
            create_vessel.create_vessel(name)
        except Exception as error:
            logger.debug(traceback.format_exc())

    def file_manager_open(self):
        # print(self.tk)
        if len(self.tk) == 0:
            self.manager_open = False
            self.file_manager = MDFileManager(
                exit_manager=self.exit_manager, select_path=self.select_path,
                ext=['.csv', ], selection=[]
            )
            if platform == "android":
                self.file_manager.show(SD_CARD)
            else:
                self.file_manager.show(os.path.expanduser("~"))  # output manager to the screen

            self.manager_open = True
        else:
            self.tk = self.root.get_screen("add_tank_screen").ids.new_tank.text = "Enter name of Tank"
            pass

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''
        self.manager_open = False
        self.file_manager.close()

    def select_path(self, path: str, ):
        '''
        It will be called when you click on the file nameF
        or the catalog selection button.

        :param path: path to the selected directory or file;
        '''

        self.selected_tank_import = path
        self.exit_manager()
        # print(self.selected_tank_import)
        # print(self.root.get_screen("add_tank_screen").ids.new_tank.text)
        self.tk = self.root.get_screen("add_tank_screen").ids.new_tank.text
        toast(path)
        db_reading.import_data(self.selected_tank_import, self.vessel_for_import, self.tk)

    def choose_vessel_admin(self):
        """
        Create a dropdown menu for selecting the Vessel`s Data Base
        """
        self.vessel_name_db = []
        self.vessels_admin = []
        self.db_tuple_admin = {}

        try:
            try:
                # scan current working Directory
                scan_dir = os.listdir(file_location_detect)
                for file in scan_dir:
                    if not file.endswith('_prev.db') and file.endswith(".db"):
                        parsed_vessel = str(file).removesuffix('.db').title()
                        self.vessel_name_db.append(parsed_vessel)
                        self.vessels_admin.append(parsed_vessel)
            except Exception as error:
                logger.debug(traceback.format_exc())
            for vessel in iter(self.vessels_admin):
                self.the_DB_admin[vessel] = self.vessels_admin[0]
            # print(vessels_admin)
            menu_items = [(
                {
                    "viewclass": "OneLineListItem",
                    "text": f"{self.vessels_admin[i]}",
                    "on_release": lambda x=f"{self.vessels_admin[i]}": self.selected_vessel_import(x)
                }) for i in range(len(self.vessels_admin))
            ]
            self.menu_admin = MDDropdownMenu(
                items=menu_items,
                width_mult=4,
                caller=self.root.get_screen("add_tank_screen").ids.drop_vessels,
            )
            self.menu_admin.open()
            self.vessel_to_delete = self.vessels_admin
        except ValueError as error:
            logger.debug(traceback.format_exc())
            pass

    def selected_vessel_import(self, vessel: str):
        self.root.get_screen("add_tank_screen").ids.drop_vessels.text = vessel
        self.root.get_screen("del_vessel_screen").ids.drop_vessels.text = vessel
        self.menu_admin.dismiss()
        self.vessel_for_import = (str(vessel).lower() + ".db")
        self.root.get_screen("add_tank_screen").ids.new_tank.disabled = False
        self.root.get_screen("add_tank_screen").ids.btn_add.disabled = False
        self.tk = self.root.get_screen("add_tank_screen").ids.new_tank.text = str()

    def delete_vessel(self):
        file_db = str(self.root.get_screen("del_vessel_screen").ids.drop_vessels.text).lower() + ".db"
        file_db_prev = str(self.root.get_screen("del_vessel_screen").ids.drop_vessels.text).lower() + "_prev.db"
        os.remove(str(file_location_detect + "/" + str(file_db)))
        os.remove(str(file_location_detect + "/" + str(file_db_prev)))


if __name__ == "__main__":
    try:
        BunkerCalc().run()
    except Exception as error:
        logger.debug(traceback.format_exc())
