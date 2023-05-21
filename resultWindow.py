"""
Код финального сообщения после выполнения теста
"""
import math
import sys
import customtkinter as ctk
from PIL import Image


class ResultsMessage:
    def __init__(self, master, result_prc: float, result_tuple: tuple):

        # Шрифты
        self.text_font = ctk.CTkFont(size=20, weight="bold")
        self.header_font = ctk.CTkFont(size=40, weight="bold")
        self.btn_font = ctk.CTkFont(size=30, weight="bold")

        # Результаты
        self.res_prc = result_prc
        self.res_tup = result_tuple

        # Изображения
        self.a_img = ctk.CTkImage(Image.open("assets/5.ico"), size=(100, 100))
        self.b_img = ctk.CTkImage(Image.open("assets/4.ico"), size=(100, 100))
        self.c_img = ctk.CTkImage(Image.open("assets/3.ico"), size=(100, 100))
        self.d_img = ctk.CTkImage(Image.open("assets/2.ico"), size=(100, 100))
        self.f_img = ctk.CTkImage(Image.open("assets/1.ico"), size=(100, 100))

        self.header_lbl = ctk.CTkLabel(master=master, font=self.header_font, compound="top", justify="center")
        self.header_lbl.place(relx=0.5, rely=0.2, anchor="center")

        self.text_lbl = ctk.CTkLabel(master=master, font=self.text_font,
                                     text=f"Ты выполнил {self.res_tup[0]} из {self.res_tup[1]} заданий, что составляет"
                                          f" {math.floor(self.res_prc)}%")
        self.text_lbl.place(relx=0.5, rely=0.4, anchor="center")

        self.quit_btn = ctk.CTkButton(master=master, command=sys.exit, text="Выйти",
                                      font=self.btn_font, width=200, height=50, corner_radius=15)
        self.quit_btn.place(relx=0.5, rely=0.7, anchor="center")

        self.final_message()

    def final_message(self):
        if self.res_prc >= 75:
            self.header_lbl.configure(image=self.a_img)
            self.header_lbl.configure(text="Поздравляем!")

        elif self.res_prc >= 50:
            self.header_lbl.configure(image=self.b_img)
            self.header_lbl.configure(text="Хорошо!")

        elif self.res_prc >= 25:
            self.header_lbl.configure(image=self.c_img)
            self.header_lbl.configure(text="Неплохо.")

        elif self.res_prc >= 1:
            self.header_lbl.configure(image=self.d_img)
            self.header_lbl.configure(text="Плохо.")

        elif self.res_prc < 1:
            self.header_lbl.configure(image=self.f_img)
            self.header_lbl.configure(text="Попробуй ещё раз...")
