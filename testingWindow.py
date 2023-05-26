"""
Код работы с тестами
"""
import customtkinter as ctk
from collections import OrderedDict
from random import shuffle


class TestingFrame(ctk.CTkFrame):
    def __init__(self, master, quit_button, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(1, weight=1)

        self.move = 1
        self.case_answers = {}
        self.btn_list = []
        self.current_case_answer = None
        self.test_data = None
        self.case_data = None
        self.imageParser = None

        # Шрифты
        self.text_font = ctk.CTkFont(size=20, weight="bold")
        self.header_font = ctk.CTkFont(size=30, weight="bold")
        self.btn_font = ctk.CTkFont(size=15, weight="bold")

        self.quit_btn = quit_button

        # Переключение между кейсами
        self.prev_btn = ctk.CTkButton(master=self, text="◀", font=self.text_font, width=30, corner_radius=5,
                                      command=lambda: self.change_case_event("prev"))
        self.prev_btn.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.next_btn = ctk.CTkButton(master=self, text="▶", font=self.text_font, width=30, corner_radius=5,
                                      command=lambda: self.change_case_event("next"))
        self.next_btn.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        # Прогресс бар прохождения теста
        self.progress = ctk.CTkProgressBar(master=self, width=960)
        self.progress.set(0)
        self.progress.grid(row=0, column=1, padx=15)

        # Фрейм кейсов
        self.case_frame = ctk.CTkFrame(master=self, corner_radius=5)
        self.case_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5, columnspan=3, rowspan=3)

        # Фрейм с виджетами ответа
        self.answer_frame = ctk.CTkFrame(master=self, fg_color=("#b8b8b8", "#434343"))
        self.answer_frame.grid(row=3, column=0, columnspan=3, sticky="sew", padx=15, pady=15)

        # Картинка внутри кейса
        self.image_label = ctk.CTkLabel(master=self.case_frame, text="")

        # Имя кейса
        self.case_name = ctk.CTkLabel(master=self.case_frame, text="",
                                      font=self.header_font, corner_radius=7,
                                      fg_color=("#b8b8b8", "#434343"), anchor="center")
        self.case_name.grid(row=0, column=0, sticky="nw", padx=15, pady=15, ipadx=5, ipady=5, columnspan=2)

        # Описание кейса
        self.case_description = ctk.CTkLabel(master=self.case_frame, text="", font=self.text_font,
                                             wraplength=750, justify="left")

    def shuffle_cases(self):
        """Перемешивает рандомно кейсы"""
        keys = list(self.test_data["cases"].keys())
        shuffle(keys)
        shuffled = OrderedDict()
        for key in keys:
            shuffled[key] = self.test_data["cases"][key]
        self.case_data = shuffled

    def change_case_event(self, direction: str):
        """Перейти на другой кейс"""
        current_move = self.move
        self.save_case_answer(current_move, self.current_case_answer.get())

        if direction == "next":
            if self.move < len(self.case_data):
                self.move += 1
        if direction == "prev":
            if self.move > 1:
                self.move -= 1

        if current_move != self.move:
            self.draw_case(self.move - 1)

        if self.move == len(self.case_data):
            self.quit_btn.configure(state="normal")
            self.calculate_result()
        else:
            self.quit_btn.configure(state="disabled")

        self.progress.set((self.move - 1) / (len(self.case_data) - 1))

    def save_case_answer(self, move, answer):
        """Сохраняет ответы. В случае пустого значения сохраняет None"""
        if len(answer) >= 1:
            self.case_answers[move] = answer
        else:
            self.case_answers[move] = None

    def calculate_result(self):
        """Вычислить результат в %"""
        result = 0
        for elem in self.case_answers.items():
            if elem[1] == list(self.case_data.items())[elem[0]-1][1]["correct"]:
                result += 1
        return result / len(self.case_data) * 100

    def calculate_completed(self):
        """Вычисляет количество правильных ответов"""
        result = 0
        for elem in self.case_answers.items():
            if elem[1] == list(self.case_data.items())[elem[0]-1][1]["correct"]:
                result += 1
        return result, len(self.case_data)

    def draw_case(self, n: int):
        """Прорисовать конкретный кейс"""
        case = list(self.case_data.items())[n]
        if case[1]["type"] == "only one answer":
            self.draw_only_one_answer_case(case)
        if case[1]["type"] == "multiple answer":
            pass
        if case[1]["type"] == "text enter answer":
            pass

    def draw_case_top(self, case):
        """Прорисовать верхнюю часть кейса"""
        self.case_name.configure(text=f"Вопрос {self.move}")

        self.case_description.configure(text=case[1]["description"])

        if case[0] in self.imageParser.byteImages:
            image = ctk.CTkImage(self.imageParser.byteImages[case[0]], size=(230, 230))
            self.image_label.configure(image=image)
            self.image_label.grid(row=1, column=0, sticky="wn", padx=(15, 0), pady=(0, 15))
            self.case_description.grid(row=1, column=1, sticky="nw", padx=15, pady=(0, 15))
        else:
            self.image_label.grid_forget()
            self.case_description.grid(row=1, column=0, sticky="nw", padx=15, pady=(0, 15))

    def draw_case_answers(self, case, variable):
        """Прорисовать нижнюю часть кейса с ответами"""
        answers = list(case[1]["answers"].items())
        shuffle(answers)
        for btn in self.btn_list:
            btn.grid_forget()
        for i, answer in enumerate(answers):
            btn = ctk.CTkRadioButton(master=self.answer_frame, text=answer[1],
                                     font=self.text_font, value=answer[0], variable=variable)
            btn.grid(row=i, column=0, sticky="nsew", padx=15, pady=15)
            self.btn_list.append(btn)

    def draw_only_one_answer_case(self, case):
        """Прорисовать кейс с типом only one answer"""
        self.current_case_answer = ctk.StringVar()
        self.draw_case_top(case)
        self.draw_case_answers(case, self.current_case_answer)