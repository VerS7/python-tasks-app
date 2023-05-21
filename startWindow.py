"""
Основной код приложения
"""
import fileParser
import tkinter.messagebox
import customtkinter as ctk
from tkinter import filedialog
from testsScrollableFrame import TestsScrollableList
from testingWindow import TestingFrame
from imageParser import ImageParser
from resultWindow import ResultsMessage
from PIL import Image

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.iconbitmap("assets/icon.ico")
        self.geometry("1080x640")
        self.title("Универсальное тестирование")

        self.grid_rowconfigure(0, weight=1)

        # Шрифты
        self.btn_font = ctk.CTkFont(size=15, weight="bold")
        self.lbl_font = ctk.CTkFont(size=20, weight="bold")

        # Кнопка начала и фрейм описания
        self.tests_description_frame = ctk.CTkFrame(master=self, width=500)
        self.start_btn = ctk.CTkButton(master=self.tests_description_frame, text="Начать",
                                       font=self.btn_font, command=self.start_testing_event)

        self.quit_btn = ctk.CTkButton(master=self, text="Завершить тест", command=self.complete_event,
                                      font=self.btn_font, anchor="center", state="disabled")

        # Фреймы тестов
        self.tests_list = TestsScrollableList(master=self, width=300, start_btn=self.start_btn,
                                              description_frame=self.tests_description_frame)
        self.testing_frame = TestingFrame(master=self, quit_button=self.quit_btn, width=1080)
        self.tests_description_frame.grid_columnconfigure(0, minsize=500)

        # Фрейм меню
        self.menu_frame = ctk.CTkFrame(master=self)
        self.menu_frame.grid(row=0, column=0, sticky="nsew", pady=5, padx=5)
        self.menu_frame.grid_rowconfigure(4, weight=1)

        # Меню лейбл
        self.menu_label = ctk.CTkLabel(master=self.menu_frame, text="Меню", font=self.lbl_font)
        self.menu_label.grid(row=0, column=0, padx=20, pady=5)

        # Кнопки
        self.teacher_mode_btn = ctk.CTkButton(master=self.menu_frame, text="Конвертировать",
                                              command=self.start_redacting_event, anchor="center", width=200,
                                              font=self.btn_font, corner_radius=7)
        self.teacher_mode_btn.grid(row=2, column=0, padx=15, pady=5)

        self.user_mode_btn = ctk.CTkButton(master=self.menu_frame, text="Пройти тестирование",
                                           command=self.choice_tests_event, anchor="center", width=200,
                                           font=self.btn_font, corner_radius=7)
        self.user_mode_btn.grid(row=1, column=0, padx=15, pady=5)

        # Лейбл вступительного описания
        self.intro_image = ctk.CTkImage(Image.open("assets/intro.ico"), size=(150, 150))
        self.intro_label = ctk.CTkLabel(master=self, text="Добро пожаловать в программу Универсальное Тестирование!\n"
                                                          "Для прохождения тестов нажмите \"Пройти тестирование\"\n",
                                        anchor="e", font=self.lbl_font, justify="left", wraplength=700,
                                        image=self.intro_image, compound="bottom")
        self.intro_label.grid(row=0, column=2, padx=100, pady=0, sticky="nsew")

        # Выбор цвета темы
        self.theme_selector = ctk.CTkOptionMenu(master=self.menu_frame, values=["Светлая", "Тёмная", "Системная"],
                                                command=self.change_theme_event, font=self.btn_font,
                                                width=200, corner_radius=7)
        self.theme_selector.grid(row=5, column=0, padx=15, pady=15)

    def change_theme_event(self, theme: str):
        """Ивент изменения цвета темы приложения"""
        themes = {"Тёмная": "dark", "Светлая": "light", "Системная": "system"}
        ctk.set_appearance_mode(themes[theme])

    def choice_tests_event(self):
        """Перейти в режим выбора теста"""
        self.intro_label.grid_forget()
        self.tests_list.add_tests_from_path()
        self.tests_list.grid(row=0, column=3, padx=5, pady=5, sticky="nws")
        self.tests_description_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

    def start_testing_event(self):
        """Перейти в режим тестирования"""
        self.menu_frame.grid_forget()
        self.tests_description_frame.grid_forget()
        self.tests_list.grid_forget()
        self.testing_frame.test_data = self.tests_list.get_test_data()
        self.testing_frame.imageParser = ImageParser(self.tests_list.get_test_data())
        self.testing_frame.draw_case(0)
        self.testing_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.testing_frame.quit_btn.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="nsw")

    def start_redacting_event(self):
        """Открыть конвертацию .json в .tdata"""
        try:
            fileParser.encode_file(filedialog.askopenfilename(), outpath="tests")
            tkinter.messagebox.showinfo("Успешно", ".json успешно конвертирован в .tdata")
        except Exception:
            tkinter.messagebox.showerror("Ошибка", "Не удалось конвертировать файл в .tdata")

    def complete_event(self):
        """Завершить тест"""
        self.testing_frame.change_case_event("next")
        ResultsMessage(self, self.testing_frame.calculate_result(), self.testing_frame.calculate_completed())
        self.testing_frame.grid_forget()
        self.quit_btn.grid_forget()


if __name__ == '__main__':
    app = App()
    app.mainloop()
