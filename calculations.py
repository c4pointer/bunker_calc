# import sqlite3
# conn = sqlite3.connect('bunker_calc.db')
# cur = conn.cursor()

# def vol_correction_factor_calc(conv_dens, volume_value, temp):
#     try:
#         if float(conv_dens) <= 771 :
#             self.b=346.4228
#         else:
#             if float(conv_dens) <= 787:
#                 self.b=2680.3206
#             else:
#                 if float(conv_dens) <= 838.5:
#                     self.b=594.5418
#                 else:
#                     if float(conv_dens) <=1075:
#                         self.b=186.9696
#                     else:
#                         pass
#                         #need to make here an allert message
#         if float(conv_dens) <= 771 :
#             self.c=0.4388
#         else:
#             if float(conv_dens) <= 787 :
#                 self.c=-0.00336312
#             else:
#                 if float(conv_dens) <= 838.5 :
#                     self.c=0
#                 else:
#                     if float(conv_dens) <= 1075 :
#                         self.c=0.4862
#                     else:
#                         pass
#                         #need to make an allert message
#         if self.c >= 0 :
#             self.d=((self.b)/conv_dens**2)+(self.c/conv_dens)
#             self.d=round(self.d,7)
#         else:
#             self.d=(self.b/(conv_dens**2))+self.c

#         # Volume correction factor formula

#         if volume_value == 0 :
#             self.temp_cor_factor=round(
#                 math.exp(
#                     (-self.d*int((int(temp)*4+0.5)/4-15)*(1+0.8*float(self.d)*int((int(temp)*4+0.5)/4-15)))), 4
#                     )
#         else:
#             try:
#                 if -1 <  float(temp) < 150:
#                     try:
#                         self.temp_cor_factor=round(
#                             math.exp(
#                                 (-self.d*int((int(temp)*4+0.5)/4-15)*(1+0.8*float(self.d)*int((int(temp)*4+0.5)/4-15)))), 4
#                                 )

#                     except ValueError:

#                         # self.show_error=showinfo(
#                         #     "Error", message=str(
#                         #     "Введите правильно температуру или посчитает при : \n + 15 С\n"
#                         #     ))
#                         temp=15
#                         self.temp_cor_factor=round(
#                             math.exp(
#                                 (-self.d*int((int(temp)*4+0.5)/4-15)*(1+0.8*float(self.d)*int((int(temp)*4+0.5)/4-15)))), 4
#                                 )
#                 else:

#                     temp=15
#                     # self.show_error=showinfo(
#                     #         "Error", message=str(
#                     #         "Температура слишком низкая или слишком высокая \n"))

#             except ValueError:

#                 temp=15

#                 self.temp_cor_factor=round(
#                     math.exp(
#                         (-self.d*int((int(temp)*4+0.5)/4-15)*(1+0.8*float(self.d)*int((int(temp)*4+0.5)/4-15)))), 4
#                         )
                
#         # Weight factor
#         self.weight_cor_factor=float(conv_dens/1000-0.0011)

#         # real volume is calculating:
#         self.q=float(volume_value)*float(self.temp_cor_factor)
#         self.real_vol=str(round((self.q*self.weight_cor_factor),2))
#         self.res.append(self.real_vol)
