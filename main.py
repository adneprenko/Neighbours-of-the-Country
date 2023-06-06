from geo_code import *
import tkinter as tk
from tkinter import Canvas, PhotoImage, Button, messagebox

def process_country(country):
    # Код для обработки выбранной страны
    country_and_neighbours.append(country)

    if len(country_and_neighbours) == 1:
        print("Выбранная страна:", country)
        # print(get_neighboring_countries(country))
        tk.Label(root, text="А теперь Выберите страны, которые соседствуют с " + country_and_neighbours[0], font= 15).pack()
        tk.Label(root, text="Для удаления ошибочно выбранной страны, используйте двойной клик").pack()
        listbox.pack()
        btn = Button(root, text="Проверим Ваш ответ?")
        btn.config(command=lambda: check_result())
        btn.pack(side='bottom')
        btn1 = Button(root, text="Выход")
        btn1.config(command=lambda: on_close())
        btn1.pack(side='bottom')

    else:
        listbox.insert(tk.END, country)
        print(list(listbox.get(0, tk.END)))

def delete_country():
    # Получение индекса выбранной страны
    selected_index = listbox.curselection()
    if selected_index:
        index = selected_index[0]
        # Удаление выбранной страны из Listbox
        listbox.delete(index)

class CountrySelectionFrame(tk.Frame):
    def __init__(self, master, countries):
        super().__init__(master)

        self.countries = countries
        self.filter_label = tk.Label(self, text="Фильтр:")
        self.filter_label.pack()
        self.filter_entry = tk.Entry(self)
        self.filter_entry.pack()

        # Создание прокрутки для списка стран
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.country_listbox = tk.Listbox(self, yscrollcommand=scrollbar.set)
        self.country_listbox.pack()

        # Привязка прокрутки к списку стран
        scrollbar.config(command=self.country_listbox.yview)

        self.filter_entry.bind("<KeyRelease>", lambda event: self.filter_countries())
        self.country_listbox.bind("<Double-Button-1>", self.select_country)

        self.populate_countries()

    def filter_countries(self):
        filter_text = self.filter_entry.get().lower()
        self.country_listbox.delete(0, tk.END)
        filtered_countries = [country for country in self.countries if country.lower().startswith(filter_text)]
        for country in filtered_countries:
            self.country_listbox.insert(tk.END, country)

    def select_country(self, event):
        selected_country = self.country_listbox.get(self.country_listbox.curselection())
        process_country(selected_country)

    def populate_countries(self):
        for country in self.countries:
            self.country_listbox.insert(tk.END, country)

def check_result():
    print(list(listbox.get(0, tk.END)))
    if get_neighboring_countries(country_and_neighbours[0]) == '' or sorted(get_neighboring_countries(country_and_neighbours[0])) == sorted(list(listbox.get(0, tk.END))):
        print('Victory')
        plot_country_border(country_and_neighbours[0], 'WIN!! Congratulations')
        root.destroy()
    else:
        print('You loose')
        plot_country_border(country_and_neighbours[0], 'loose')
        root.destroy()



def on_close():
    if messagebox.askokcancel('Выход', 'Действительно хотите закрыть окно?'):
        root.destroy()
        global game
        game = False


# Список стран
countries = list_of_all_countries()
game = True
while game:
    country_and_neighbours = []
    # Создание главного окна
    root = tk.Tk()
    root.title("Игра для Александра Днепренко")
    canvas = Canvas(root, bg='white', height=200, width=700)
    canvas.pack()
    test = PhotoImage(file='wellcome.png')
    canvas.create_image(300, 100, image=test)
    listbox = tk.Listbox(root)
    listbox.bind('<Double-Button-1>', lambda event: delete_country())
    CountrySelectionFrame(root, countries).pack(side=tk.LEFT, padx=10, pady=10)
    root.protocol('WM_DELETE_WINDOW', on_close)
    root.mainloop()

