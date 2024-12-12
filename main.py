import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime


class CafeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Учет кафе")
        self.root.geometry("800x600")

        # Загрузка данных
        self.load_data()

        # Интерфейс
        self.create_widgets()

    def load_data(self):
        try:
            with open('menu.json', 'r', encoding='utf-8') as f:
                self.menu = json.load(f)
        except FileNotFoundError:
            self.menu = []

        try:
            with open('orders.json', 'r', encoding='utf-8') as f:
                self.orders = json.load(f)
        except FileNotFoundError:
            self.orders = []

        try:
            with open('finances.json', 'r', encoding='utf-8') as f:
                self.finances = json.load(f)
        except FileNotFoundError:
            self.finances = {"income": 0, "expenses": 0}

        try:
            with open('employees.json', 'r', encoding='utf-8') as f:
                self.employees = json.load(f)
        except FileNotFoundError:
            self.employees = []

    def save_data(self):
        with open('menu.json', 'w', encoding='utf-8') as f:
            json.dump(self.menu, f, indent=4, ensure_ascii=False)

        with open('orders.json', 'w', encoding='utf-8') as f:
            json.dump(self.orders, f, indent=4, ensure_ascii=False)

        with open('finances.json', 'w', encoding='utf-8') as f:
            json.dump(self.finances, f, indent=4, ensure_ascii=False)

        with open('employees.json', 'w', encoding='utf-8') as f:
            json.dump(self.employees, f, indent=4, ensure_ascii=False)

    def create_widgets(self):
        # Табы
        tab_control = ttk.Notebook(self.root)

        # Таб с меню
        menu_tab = ttk.Frame(tab_control)
        tab_control.add(menu_tab, text="Меню")
        tab_control.pack(expand=1, fill="both")

        # Таб с заказами
        orders_tab = ttk.Frame(tab_control)
        tab_control.add(orders_tab, text="Заказы")
        tab_control.pack(expand=1, fill="both")

        # Таб с сотрудниками
        employees_tab = ttk.Frame(tab_control)
        tab_control.add(employees_tab, text="Сотрудники")
        tab_control.pack(expand=1, fill="both")

        # Таб с отчетностью
        finance_tab = ttk.Frame(tab_control)
        tab_control.add(finance_tab, text="Отчетность")
        tab_control.pack(expand=1, fill="both")

        # Меню
        self.menu_tree = ttk.Treeview(menu_tab, columns=("Название", "Описание", "Цена"), show="headings")
        self.menu_tree.heading("Название", text="Название")
        self.menu_tree.heading("Описание", text="Описание")
        self.menu_tree.heading("Цена", text="Цена")
        self.menu_tree.pack(fill="both", expand=1)

        # Кнопки для добавления и редактирования
        add_button = ttk.Button(menu_tab, text="Добавить блюдо", command=self.add_dish)
        add_button.pack(pady=10)

        edit_button = ttk.Button(menu_tab, text="Редактировать блюдо", command=self.edit_dish)
        edit_button.pack(pady=10)

        # Заполнение меню
        self.update_menu_tree()

        # Заказы
        self.orders_tree = ttk.Treeview(orders_tab, columns=("Дата", "Статус", "Блюда"), show="headings")
        self.orders_tree.heading("Дата", text="Дата")
        self.orders_tree.heading("Статус", text="Статус")
        self.orders_tree.heading("Блюда", text="Блюда")
        self.orders_tree.pack(fill="both", expand=1)

        # Кнопки для создания и изменения статуса заказов
        create_order_button = ttk.Button(orders_tab, text="Создать заказ", command=self.create_order)
        create_order_button.pack(pady=10)

        change_status_button = ttk.Button(orders_tab, text="Изменить статус", command=self.change_order_status)
        change_status_button.pack(pady=10)

        # Заполнение заказов
        self.update_orders_tree()

        # Таблица сотрудников
        self.employees_tree = ttk.Treeview(employees_tab, columns=("Имя", "Должность", "Оклад"), show="headings")
        self.employees_tree.heading("Имя", text="Имя")
        self.employees_tree.heading("Должность", text="Должность")
        self.employees_tree.heading("Оклад", text="Оклад")
        self.employees_tree.pack(fill="both", expand=1)

        # Кнопки для работы с сотрудниками
        add_employee_button = ttk.Button(employees_tab, text="Добавить сотрудника", command=self.add_employee)
        add_employee_button.pack(pady=10)

        edit_employee_button = ttk.Button(employees_tab, text="Редактировать сотрудника", command=self.edit_employee)
        edit_employee_button.pack(pady=10)

        delete_employee_button = ttk.Button(employees_tab, text="Удалить сотрудника", command=self.delete_employee)
        delete_employee_button.pack(pady=10)

        # Заполнение таблицы сотрудников
        self.update_employees_tree()

        # Финансовый отчет
        self.income_label = ttk.Label(finance_tab, text=f"Доход: {self.finances['income']} руб.")
        self.income_label.pack(pady=10)

        self.expenses_label = ttk.Label(finance_tab, text=f"Расходы: {self.finances['expenses']} руб.")
        self.expenses_label.pack(pady=10)

        self.profit_label = ttk.Label(finance_tab,
                                      text=f"Прибыль: {self.finances['income'] - self.finances['expenses']} руб.")
        self.profit_label.pack(pady=10)

    def update_menu_tree(self):
        for row in self.menu_tree.get_children():
            self.menu_tree.delete(row)
        for dish in self.menu:
            self.menu_tree.insert("", "end", values=(dish["name"], dish["description"], dish["price"]))

    def update_orders_tree(self):
        for row in self.orders_tree.get_children():
            self.orders_tree.delete(row)
        for order in self.orders:
            self.orders_tree.insert("", "end", values=(order["date"], order["status"], ", ".join(order["dishes"])))

    def update_finances_labels(self):
        self.income_label.config(text=f"Доход: {self.finances['income']} руб.")
        self.expenses_label.config(text=f"Расходы: {self.finances['expenses']} руб.")
        self.profit_label.config(text=f"Прибыль: {self.finances['income'] - self.finances['expenses']} руб.")

    def add_dish(self):
        self.dish_window("Добавить блюдо")

    def edit_dish(self):
        selected_item = self.menu_tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите блюдо для редактирования.")
            return
        selected_dish = self.menu_tree.item(selected_item)["values"]
        self.dish_window("Редактировать блюдо", selected_dish)

    def dish_window(self, title, selected_dish=None):
        window = tk.Toplevel(self.root)
        window.title(title)

        name_label = ttk.Label(window, text="Название:")
        name_label.grid(row=0, column=0)
        name_entry = ttk.Entry(window)
        name_entry.grid(row=0, column=1)
        if selected_dish:
            name_entry.insert(0, selected_dish[0])

        description_label = ttk.Label(window, text="Описание:")
        description_label.grid(row=1, column=0)
        description_entry = ttk.Entry(window)
        description_entry.grid(row=1, column=1)
        if selected_dish:
            description_entry.insert(0, selected_dish[1])

        price_label = ttk.Label(window, text="Цена:")
        price_label.grid(row=2, column=0)
        price_entry = ttk.Entry(window)
        price_entry.grid(row=2, column=1)
        if selected_dish:
            price_entry.insert(0, selected_dish[2])

        save_button = ttk.Button(window, text="Сохранить",
                                 command=lambda: self.save_dish(window, name_entry, description_entry, price_entry,
                                                                selected_dish))
        save_button.grid(row=3, column=1, pady=10)

    def save_dish(self, window, name_entry, description_entry, price_entry, selected_dish=None):
        name = name_entry.get()
        description = description_entry.get()
        price = price_entry.get()

        if not name or not description or not price:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
            return

        if selected_dish:
            index = self.menu.index(
                {"name": selected_dish[0], "description": selected_dish[1], "price": selected_dish[2]})
            self.menu[index] = {"name": name, "description": description, "price": float(price)}
        else:
            self.menu.append({"name": name, "description": description, "price": float(price)})

        self.save_data()
        self.update_menu_tree()
        window.destroy()

    def create_order(self):
        order_window = tk.Toplevel(self.root)
        order_window.title("Создание заказа")

        # Блюда
        dish_label = ttk.Label(order_window, text="Выберите блюдо:")
        dish_label.grid(row=0, column=0)

        # Listbox для добавления нескольких блюд
        self.dishes_listbox = tk.Listbox(order_window, selectmode=tk.MULTIPLE, height=10)
        for dish in self.menu:
            self.dishes_listbox.insert(tk.END, f"{dish['name']} - {dish['price']} руб")
        self.dishes_listbox.grid(row=1, column=0, columnspan=2)

        # Кнопка для добавления блюд в заказ
        add_button = ttk.Button(order_window, text="Добавить блюда в заказ", command=self.add_dishes_to_order)
        add_button.grid(row=2, column=0, pady=10)

        # Статус
        status_label = ttk.Label(order_window, text="Статус:")
        status_label.grid(row=3, column=0)
        status_combobox = ttk.Combobox(order_window, values=["в процессе", "готов", "отменен"])
        status_combobox.grid(row=3, column=1)

        save_button = ttk.Button(order_window, text="Сохранить заказ",
                                 command=lambda: self.save_order(order_window, status_combobox.get()))
        save_button.grid(row=4, column=1, pady=10)

    def add_dishes_to_order(self):
        selected_dishes = [self.menu[i] for i in self.dishes_listbox.curselection()]
        if not selected_dishes:
            messagebox.showerror("Ошибка", "Выберите хотя бы одно блюдо.")
            return
        self.selected_dishes = selected_dishes

    def save_order(self, window, status):
        if not hasattr(self, 'selected_dishes'):
            messagebox.showerror("Ошибка", "Не выбраны блюда для заказа.")
            return

        order = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": status,
            "dishes": [dish["name"] for dish in self.selected_dishes],
            "price": [dish["price"] for dish in self.selected_dishes]
        }
        self.orders.append(order)
        self.update_finances(order, status)  # Обновление финансов при создании заказа
        self.save_data()
        self.update_orders_tree()
        window.destroy()

    def change_order_status(self):
        selected_item = self.orders_tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите заказ для изменения статуса.")
            return
        selected_order = self.orders_tree.item(selected_item)["values"]
        self.status_window(selected_order)

    def status_window(self, selected_order):
        window = tk.Toplevel(self.root)
        window.title("Изменить статус")

        new_status_label = ttk.Label(window, text="Новый статус:")
        new_status_label.grid(row=0, column=0)
        new_status_combobox = ttk.Combobox(window, values=["в процессе", "готов", "отменен"])
        new_status_combobox.grid(row=0, column=1)
        new_status_combobox.set(selected_order[1])

        save_button = ttk.Button(window, text="Сохранить",
                                 command=lambda: self.save_status(window, selected_order[0], new_status_combobox.get()))
        save_button.grid(row=1, column=1, pady=10)

    def save_status(self, window, order_date, new_status):
        for order in self.orders:
            if order["date"] == order_date:
                old_status = order["status"]
                order["status"] = new_status
                self.update_finances(order, old_status, new_status)  # Обновление финансов при изменении статуса
                self.save_data()
                self.update_orders_tree()
                window.destroy()
                break

    def update_employees_tree(self):
        for row in self.employees_tree.get_children():
            self.employees_tree.delete(row)
        for employee in self.employees:
            self.employees_tree.insert("", "end", values=(employee["name"], employee["position"], employee["salary"]))

    def add_employee(self):
        self.employee_window("Добавить сотрудника")

    def edit_employee(self):
        selected_item = self.employees_tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите сотрудника для редактирования.")
            return
        selected_employee = self.employees_tree.item(selected_item)["values"]
        self.employee_window("Редактировать сотрудника", selected_employee)

    def delete_employee(self):
        selected_item = self.employees_tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите сотрудника для удаления.")
            return
        selected_employee = self.employees_tree.item(selected_item)["values"]
        self.employees = [employee for employee in self.employees if employee["name"] != selected_employee[0]]
        self.save_data()
        self.update_employees_tree()

    def employee_window(self, title, selected_employee=None):
        window = tk.Toplevel(self.root)
        window.title(title)

        name_label = ttk.Label(window, text="Имя:")
        name_label.grid(row=0, column=0)
        name_entry = ttk.Entry(window)
        name_entry.grid(row=0, column=1)
        if selected_employee:
            name_entry.insert(0, selected_employee[0])

        position_label = ttk.Label(window, text="Должность:")
        position_label.grid(row=1, column=0)
        position_entry = ttk.Entry(window)
        position_entry.grid(row=1, column=1)
        if selected_employee:
            position_entry.insert(0, selected_employee[1])

        salary_label = ttk.Label(window, text="Оклад:")
        salary_label.grid(row=2, column=0)
        salary_entry = ttk.Entry(window)
        salary_entry.grid(row=2, column=1)
        if selected_employee:
            salary_entry.insert(0, selected_employee[2])

        save_button = ttk.Button(window, text="Сохранить",
                                 command=lambda: self.save_employee(window, name_entry, position_entry, salary_entry,
                                                                    selected_employee))
        save_button.grid(row=3, column=1, pady=10)

    def save_employee(self, window, name_entry, position_entry, salary_entry, selected_employee=None):
        name = name_entry.get()
        position = position_entry.get()
        salary = salary_entry.get()

        if not name or not position or not salary:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
            return

        if selected_employee:
            index = next((i for i, emp in enumerate(self.employees) if emp["name"] == selected_employee[0]), None)
            if index is not None:
                self.employees[index] = {"name": name, "position": position, "salary": salary}
        else:
            self.employees.append({"name": name, "position": position, "salary": salary})

        self.save_data()
        self.update_employees_tree()
        window.destroy()

    def update_finances(self, order, old_status=None, new_status=None):
        if new_status == "готов" and old_status != "готов":
            self.finances['income'] += sum(order["price"])
        elif new_status == "в процессе" and old_status == "готов":
            self.finances['income'] -= sum(order["price"])
            self.finances['expenses'] += sum(order["price"])
        elif new_status == "отменен" and old_status == "готов":
            self.finances['income'] -= sum(order["price"])
        elif new_status == "отменен" and old_status == "в процессе":
            self.finances['expenses'] -= sum(order["price"])
        elif old_status is None and new_status == "готов":
            self.finances['income'] += sum(order["price"])
        elif old_status is None and new_status == "в процессе":
            self.finances['expenses'] += sum(order["price"])

        self.update_finances_labels()


if __name__ == "__main__":
    root = tk.Tk()
    app = CafeApp(root)
    root.mainloop()