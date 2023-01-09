from kivymd.uix.menu import MDDropdownMenu
import sqlite3
import os
vessels =[]
file_location_detect = os.getcwd()
try:
    scan_dir=os.scandir(file_location_detect)
    for entries in scan_dir:
        if not entries.name.endswith('_prev.db') and entries.is_file:
            if entries.name.endswith(".db"):
                parsed_vessel = str(entries).removeprefix('<DirEntry \'').removesuffix('.db\'>').title()
                vessels.append(parsed_vessel)
    
except sqlite3.OperationalError as e:
    print(f"Error in DB choosing code")

def vessels_list():
    """
    Create a dropdown menu for navigate beetwen the screens
    """
    for i in vessels:
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{i}",
                "on_release": lambda x="lambda":x
            },

        ]
    menu = MDDropdownMenu(
        items=menu_items,
        width_mult=4
    )
    menu.caller = x
    menu.open()
