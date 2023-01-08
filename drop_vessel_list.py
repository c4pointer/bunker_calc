from kivymd.uix.menu import MDDropdownMenu
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