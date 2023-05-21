"""
Код работы виджета с тестами, описания и вхождения в режим тестирования
"""
import customtkinter as ctk
import os
from fileParser import *


default_tests_path = "tests"


def get_file_paths(directory: str):
    """Возвращает пути к файлам из директории"""
    file_paths = []
    for root, directories, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    return file_paths


class TestsScrollableList(ctk.CTkScrollableFrame):
    def __init__(self, master, description_frame: ctk.CTkFrame, start_btn: ctk.CTkButton, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.lbl_font = ctk.CTkFont(size=20)
        self.text_font = ctk.CTkFont(size=20, weight="bold")
        self.header_font = ctk.CTkFont(size=30, weight="bold")

        self.description_frame = description_frame

        self.description_text = ctk.CTkLabel(master=self.description_frame, font=self.text_font,
                                             justify="left", wraplength=490, text="")
        self.description_text.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.description_header = ctk.CTkLabel(master=self.description_frame, font=self.header_font,
                                               justify="center", text="")
        self.description_header.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.description_frame.grid_rowconfigure(2, weight=1)

        self.start_btn = start_btn

        self.data = []
        self.label_list = []

    def add_item(self, item: dict):
        """Добавляет тест в список тестов"""
        btn_label = ctk.CTkButton(self, text=item["test_name"], anchor="nw",
                                  command=lambda: self.load_description(item),
                                  font=self.lbl_font, corner_radius=5, bg_color="transparent")
        btn_label.grid(row=len(self.label_list), column=0, padx=5, pady=5, sticky="nsew")
        self.label_list.append(btn_label)

    def get_test_data(self):
        """Возвращает dict с текущим тестом"""
        for elem in self.data:
            if elem["test_name"] == self.description_header.cget("text"):
                return elem
        return None

    def load_description(self, item):
        """Добавляет описание теста"""
        self.description_text.configure(text=item["description"])
        self.description_header.configure(text=item["test_name"])
        self.start_btn.grid(row=2, column=0, sticky="sw", padx=10, pady=15)

    def add_tests_from_path(self):
        """добавляет все тесты из директории"""
        for label in self.label_list:
            label.grid_forget()
        for tfile in get_file_paths(default_tests_path):
            if tfile is not None:
                self.data.append(read_tdata(tfile))
                self.add_item(read_tdata(tfile))
