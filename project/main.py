import tkinter as tk
from tkinter import ttk
import sqlite3

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__()
        self.init_main()
        self.db = db
        self.view_records()
    
    # Основной интерфейс программы
    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e9', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Кнопка добавления записи
        self.add_img = tk.PhotoImage(file='./img/add.png')
        btn_open_dialog = tk.Button(toolbar, bg ='#d7d8e0', bd=0,
                                    image=self.add_img, command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'tel', 'email', 'salary'),
                                  height=45, show='headings')
        
        # Настройка колонок таблицы
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=190, anchor=tk.CENTER)
        self.tree.column('tel', width=110, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('salary', width=80, anchor=tk.CENTER)

        # Создание заголовок колонок
        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('tel', text='Номер телефона')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('salary', text='Зарплата')

        self.tree.pack(side=tk.LEFT)

        # Кнопка редактирования записи
        self.update_img = tk.PhotoImage(file='./img/update.png')
        btn_edit_dialog = tk.Button(toolbar, bg='#d7d8e0',
                                    bd=0, image=self.update_img,
                                    command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        # Кнопка удаления записи
        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        btn_delete = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                               image=self.delete_img, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        # Кнопка поиска записи
        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                               image=self.search_img, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        # Кнопка перезагрузки записей
        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                               image=self.refresh_img, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        # Создание скроллбара
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # Метод поиска записей по имени
    def search_records(self, name):
        name = ('%' + name + '%',)
        self.db.c.execute('''SELECT * FROM db WHERE name LIKE ?''', name)

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    # Открытие окна для поиска записи
    def open_search_dialog(self):
        Search()    

    # Метод удаления выбранной записи
    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''
        DELETE FROM db WHERE id = ?''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    # Метод редактирования выбранной записи
    def update_record(self, name, tel, email, salary):
        self.db.c.execute('''
        UPDATE db SET name=?, tel=?, email=?, salary=? WHERE id=?
    ''', (name, tel, email, salary,
          self.tree.set(self.tree.selection()[0], '#1'),))
        self.db.conn.commit()
        self.view_records()
    
    # Открытие окна для редактирования записи
    def open_update_dialog(self):
        Update()

    # Открытие окна для добавления записи
    def open_dialog(self):
        Child()

    # Метод добавления записи в БД
    def records(self, name, tel, email, salary):
        self.db.insert_data(name, tel, email, salary)
        self.view_records()

    # Отображение всех записей в виде таблицы
    def view_records(self):
        self.db.c.execute('''
        SELECT * FROM db''')

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

# Диалоговое окно добавления записи
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app
    
    def init_child(self):
        self.title('Добавить')
        self.geometry('400x220')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=50, y=50)
        label_tel = tk.Label(self, text='Телефон')
        label_tel.place(x=50, y=80)
        label_email = tk.Label(self, text='E-mail')
        label_email.place(x=50, y=110)
        label_salary = tk.Label(self, text='Зарплата')
        label_salary.place(x=50, y=140)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=80)

        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)

        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=140)

        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=210, y=170)

        self.btn_ok.bind('<Button-1>', lambda event:
                self.view.records(self.entry_name.get(),
                                self.entry_tel.get(),
                                self.entry_email.get(),
                                self.entry_salary.get()))

# Диалоговое окно редактирования записи
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event:
                      self.view.update_record(self.entry_name.get(),
                                              self.entry_tel.get(),
                                              self.entry_email.get(),
                                              self.entry_salary.get()))
        btn_edit.bind('<Button-1>', lambda event:
                      self.destroy(), add='+')
        self.btn_ok.destroy()

    # Заполняет поля уже имеющими записями
    def default_data(self):
        self.db.c.execute('''
        SELECT * FROM db WHERE id = ?
        ''',
        (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_tel.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])

# Диалоговое окно поиска записи
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app
    
    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть',
                                command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event:
                        self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event:
                        self.destroy(), add='+')

# Класс для взаимодействия с БД SQlite
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
        self.c = self.conn.cursor()
        self.c.execute('''
CREATE TABLE IF NOT EXISTS db(
id INTEGER PRIMARY KEY,
name TEXT,
tel TEXT,
email TEXT,
salary INTEGER)''')
        self.conn.commit()

    # Метод для добавления данных в базу данных
    def insert_data(self, name, tel, email, salary):
        self.c.execute('''
INSERT INTO db(name, tel, email, salary) VALUES (?, ?, ?, ?)''', (name, tel, email, salary))
        self.conn.commit()



if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Список сотрудников компании')
    root.geometry('665x450')
    root.resizable(False, False)
    root.mainloop()