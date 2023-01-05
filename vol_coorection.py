import math



def vol_correction_factor_calc(conv_dens, volume_value, temp):
    try:
        if float(conv_dens) <= 771 :
            b=346.4228
        else:
            if float(conv_dens) <= 787:
                b=2680.3206
            else:
                if float(conv_dens) <= 838.5:
                    b=594.5418
                else:
                    if float(conv_dens) <=1075:
                        b=186.9696
                    else:
                        pass
                        #need to make here an allert message
        if float(conv_dens) <= 771 :
            c=0.4388
        else:
            if float(conv_dens) <= 787 :
                c=-0.00336312
            else:
                if float(conv_dens) <= 838.5 :
                    c=0
                else:
                    if float(conv_dens) <= 1075 :
                        c=0.4862
                    else:
                        pass
                        #need to make an allert message
        if c >= 0 :
            d=((b)/conv_dens**2)+(c/conv_dens)
            d=round(d,7)
        else:
            d=(b/(conv_dens**2))+c

        # Volume correction factor formula

        if volume_value == 0 :
            temp_cor_factor=round(
                math.exp(
                    (-d*int((int(temp)*4+0.5)/4-15)*(1+0.8*float(d)*int((int(temp)*4+0.5)/4-15)))), 4
                    )
        else:
            try:
                if -1 <  float(temp) < 150:
                    try:
                        temp_cor_factor=round(
                            math.exp(
                                (-d*int((int(temp)*4+0.5)/4-15)*(1+0.8*float(d)*int((int(temp)*4+0.5)/4-15)))), 4
                                )

                    except ValueError:

                        # self.show_error=showinfo(
                        #     "Error", message=str(
                        #     "Введите правильно температуру или посчитает при : \n + 15 С\n"
                        #     ))
                        temp=15
                        temp_cor_factor=round(
                            math.exp(
                                (-d*int((int(temp)*4+0.5)/4-15)*(1+0.8*float(d)*int((int(temp)*4+0.5)/4-15)))), 4
                                )
                else:

                    temp=15
                    # self.show_error=showinfo(
                    #         "Error", message=str(
                    #         "Температура слишком низкая или слишком высокая \n"))

            except ValueError:

                temp=15

                temp_cor_factor=round(
                    math.exp(
                        (-d*int((int(temp)*4+0.5)/4-15)*(1+0.8*float(d)*int((int(temp)*4+0.5)/4-15)))), 4
                        )
                
        # Weight factor
        weight_cor_factor=float(conv_dens/1000-0.0011)

        # real volume is calculating:
        q=float(volume_value)*float(temp_cor_factor)
        real_vol=str(round((q*weight_cor_factor),2))
        global result
        result = real_vol
    except KeyError:
        print("error")

    