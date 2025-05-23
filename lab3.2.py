import customtkinter as ctk
from tkinter import END
import spinbox as sb
import json
import os

class Model():
    def __init__(self):
        self.__low_limit = 0
        self.__up_limit = 100
        self.settings_path = "settings.json"
        if os.path.exists(self.settings_path): # Если файл существует, подгрузит значения из него
            with open(self.settings_path, "r") as f:
                self.__a, self.__b, self.__c = json.load(f)
        else:
            self.__a, self.__b, self.__c = 0, 50, 100

    def start(self, numbers: list):
        if len(numbers) != 3:
            raise ValueError("Not valid amount of numbers")
        if (self.__a, self.__b, self.__c) != numbers:
                self.__a, self.__b, self.__c = numbers[0], numbers[1], numbers[2]
                self.process_numbers()

    def pass_numbers(self) -> list: # Возвращает значения из модели
        return (self.__a, self.__b, self.__c)

    def process_numbers(self): # Подгоняет все числа под правила
        self.__a = self.__low_limit if self.__a < self.__low_limit else self.__a
        self.__a = self.__up_limit if self.__a > self.__up_limit else self.__a

        self.__c = self.__up_limit if self.__c > self.__up_limit else self.__c
        self.__c = self.__low_limit if self.__c < self.__low_limit else self.__c

        if not(self.__a <= self.__b <= self.__c):
            if self.__a > self.__b:
                if self.__a > self.__c:
                    self.__c = self.__a
                self.__b = self.__a
            if self.__c < self.__b:
                if self.__a > self.__c:
                    self.__a = self.__c
                self.__b = self.__c
    
    def __del__(self): # деструктор
        with open(self.settings_path, "w") as f:
            json.dump((self.__a, self.__b, self.__c), f)

class Controller(ctk.CTkFrame):
    def __init__(self, master, model):
        super().__init__(master)

        self.rowconfigure((0,1,2,3), weight=1)
        self.columnconfigure((0,1,2), weight=1)

        self.model = model

        self.__valid = self.register(self.__validate)

        self.__create_widgets()

        self.set_numbers(self.model.pass_numbers())
   
    def __create_widgets(self): # Создание виджетов и подключение событий к функциям
        self.label = ctk.CTkLabel(master=self, text="A <= B <= C", fg_color="transparent", font=("Times New Roman", 95))
        self.label.grid(row=0, column=0, sticky="nsew", columnspan=3)

        self.A_entry = ctk.CTkEntry(master=self, height=40, validate="all", validatecommand=(self.__valid, "%P"))
        self.A_entry.grid(row=1, column=0, padx=15, pady=15, sticky="new")
        self.A_entry.bind("<FocusOut>", self.get_numbers)
        self.A_entry.bind("<Return>", self.get_numbers)

        self.B_entry = ctk.CTkEntry(master=self, height=40, validate="all", validatecommand=(self.__valid, "%P"))
        self.B_entry.grid(row=1, column=1, padx=15, pady=15, sticky="new")
        self.B_entry.bind("<FocusOut>", self.get_numbers)
        self.B_entry.bind("<Return>", self.get_numbers)

        self.C_entry = ctk.CTkEntry(master=self, height=40, validate="all", validatecommand=(self.__valid, "%P"))
        self.C_entry.grid(row=1, column=2, padx=15, pady=15, sticky="new")
        self.C_entry.bind("<FocusOut>", self.get_numbers)
        self.C_entry.bind("<Return>", self.get_numbers)

        self.A_spinbox = sb.Spinbox(master=self, width=150, step_size=1, validate_registration=self.__valid)
        self.A_spinbox.grid(row=2, column=0, padx=15, pady=15, sticky="new")
        self.A_spinbox.entry.bind("<FocusOut>", self.get_numbers)
        self.A_spinbox.entry.bind("<Return>", self.get_numbers)
        self.A_spinbox.add_button.bind("<Button-1>", self.get_numbers)
        self.A_spinbox.subtract_button.bind("<Button-1>", self.get_numbers)

        self.B_spinbox = sb.Spinbox(master=self, width=150, step_size=1, validate_registration=self.__valid)
        self.B_spinbox.grid(row=2, column=1, padx=15, pady=15, sticky="new")
        self.B_spinbox.entry.bind("<FocusOut>", self.get_numbers)
        self.B_spinbox.entry.bind("<Return>", self.get_numbers)
        self.B_spinbox.add_button.bind("<Button-1>", self.get_numbers)
        self.B_spinbox.subtract_button.bind("<Button-1>", self.get_numbers)

        self.C_spinbox = sb.Spinbox(master=self, width=150, step_size=1, validate_registration=self.__valid)
        self.C_spinbox.grid(row=2, column=2, padx=15, pady=15, sticky="new")
        self.C_spinbox.entry.bind("<FocusOut>", self.get_numbers)
        self.C_spinbox.entry.bind("<Return>", self.get_numbers)
        self.C_spinbox.add_button.bind("<Button-1>", self.get_numbers)
        self.C_spinbox.subtract_button.bind("<Button-1>", self.get_numbers)

        self.A_slider = ctk.CTkSlider(master=self, from_=0, to=100, number_of_steps=100)
        self.A_slider.grid(row=3, column=0, padx=15, pady=15, sticky="new")
        self.A_slider.bind("<Button-1>", self.get_numbers)
        self.A_slider.bind("<B1-Motion>", self.get_numbers)

        self.B_slider = ctk.CTkSlider(master=self, from_=0, to=100, number_of_steps=100)
        self.B_slider.grid(row=3, column=1, padx=15, pady=15, sticky="new")
        self.B_slider.bind("<Button-1>", self.get_numbers)
        self.B_slider.bind("<B1-Motion>", self.get_numbers)

        self.C_slider = ctk.CTkSlider(master=self, from_=0, to=100, number_of_steps=100)
        self.C_slider.grid(row=3, column=2, padx=15, pady=15, sticky="new")
        self.C_slider.bind("<Button-1>", self.get_numbers)
        self.C_slider.bind("<B1-Motion>", self.get_numbers)

    def set_numbers(self, numbers: list): # Вставляет значения a, b, c в виджеты
        self.A_entry.delete(0, END)
        self.A_entry.insert(0, str(numbers[0]))

        self.B_entry.delete(0, END)
        self.B_entry.insert(0, str(numbers[1]))

        self.C_entry.delete(0, END)
        self.C_entry.insert(0, str(numbers[2]))

        self.A_spinbox.set(numbers[0])
        self.B_spinbox.set(numbers[1])
        self.C_spinbox.set(numbers[2])

        self.A_slider.set(numbers[0])
        self.B_slider.set(numbers[1])
        self.C_slider.set(numbers[2])

    def get_numbers(self, *args) -> None: # Получает значения a, b, c из виджетов и отправляет их на обработку в Model

        # Если какая либо строка удалена, восстанавливает значения
        if "" in [self.A_entry.get(), self.B_entry.get(), self.C_entry.get(), self.A_spinbox.entry.get(),
                  self.B_spinbox.entry.get(), self.C_spinbox.entry.get()]:
            self.model.reset_numbers()
            return
        
        # Ищет нововведённое значение из всех полей ввода (если такого нет, то вставляет первое попавшееся)
        a = [int(self.A_entry.get()), int(self.A_spinbox.get()), int(self.A_slider.get())]
        unique_a = list(set(filter(lambda x: a.count(x) == 1, a)))
        final_a = unique_a[0] if len(unique_a) > 0 else a[0]

        b = [int(self.B_entry.get()), int(self.B_spinbox.get()), int(self.B_slider.get())]
        unique_b = list(set(filter(lambda x: b.count(x) == 1, b)))
        final_b = unique_b[0] if len(unique_b) > 0 else b[0]

        c = [int(self.C_entry.get()), int(self.C_spinbox.get()), int(self.C_slider.get())]
        unique_c = list(set(filter(lambda x: c.count(x) == 1, c)))
        final_c = unique_c[0] if len(unique_c) > 0 else c[0]

        self.model.start([final_a, final_b, final_c])

        self.set_numbers(self.model.pass_numbers())

    def __validate(self, P: str): # Проверяет, что введённое значение является числом
        return str.isdigit(P) or P == "" or (P == ("-"+P[1:]) and str.isdigit(P[1:]))

class App(ctk.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.geometry("600x350")
        self.title("Лабораторная работа №3.2")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.model = Model()

        self.controller = Controller(master=self, model=self.model)
        self.controller.grid(row=0, column=0, sticky="nsew")
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.model.__del__()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()