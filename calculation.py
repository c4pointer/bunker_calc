"""
Planing to put here the calculation metod from BunkerCalc class
"""

import db_editing
import vol_coorection

from main import def_temp
from main import BunkerCalc

from main import Tab

from main import TabScreen


class Calcuation(BunkerCalc):
    def __init__(self):
        super().__init__()

    def temp_dens_extraction(self):
        try:

            if len(self.slider_value) !=0 :
                self.temperature = str(self.slider_value[str(self.tank_name.text.removesuffix('mdo')).strip(' ')])
            else:
                self.temperature = def_temp

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
            print("eror string 490" + str(self.temperature))
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


        try:
            self.converted_density = ((float(self.def_dens)/2)*1000)*2       
            vol_coorection.vol_correction_factor_calc(self.converted_density, self.result.text, self.temperature)
            self.real_volume = vol_coorection.result
        except Exception as e:
            print(e)
            print("eror string 511")

        return self.temperature, self.def_dens, self.real_volume

