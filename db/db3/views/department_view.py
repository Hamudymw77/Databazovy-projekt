# department_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from database.database_connection import DatabaseConnection

class DepartmentView:
    def __init__(self, parent):
        self.parent = parent
        self.db = DatabaseConnection('employeeManagement.db')
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(padx=10, pady=10)
        self.selected_department_id = None
        self.create_widgets()

    def create_widgets(self):
        self.department_label = ttk.Label(self.frame, text="Seznam oddělení")
        self.department_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        self.department_tree = ttk.Treeview(self.frame,
                                            columns=("department_id", "name", "budget", "establishment_date"),
                                            show="headings")
        self.department_tree.heading("department_id", text="ID")
        self.department_tree.heading("name", text="Název")
        self.department_tree.heading("budget", text="Rozpočet")
        self.department_tree.heading("establishment_date", text="Datum Vzniku")
        self.department_tree.grid(row=1, column=0, columnspan=3)
        self.department_tree.bind('<ButtonRelease-1>', self.on_tree_select)

        # Vstupní prvky pro vložení oddělení
        self.name_label = ttk.Label(self.frame, text="Název:")
        self.name_label.grid(row=2, column=0, pady=(10, 5))

        self.name_entry = ttk.Entry(self.frame)
        self.name_entry.grid(row=2, column=1, pady=(10, 5))

        self.budget_label = ttk.Label(self.frame, text="Rozpočet:")
        self.budget_label.grid(row=3, column=0, pady=(0, 5))

        self.budget_entry = ttk.Entry(self.frame)
        self.budget_entry.grid(row=3, column=1, pady=(0, 5))

        self.establishment_date_label = ttk.Label(self.frame, text="Datum Vzniku:")
        self.establishment_date_label.grid(row=4, column=0, pady=(0, 5))

        self.establishment_date_entry = ttk.Entry(self.frame)
        self.establishment_date_entry.grid(row=4, column=1, pady=(0, 5))

        self.insert_button = ttk.Button(self.frame, text="Vložit Oddělení",
                                        command=self.insert_department)
        self.insert_button.grid(row=5, column=0, columnspan=2, pady=(10, 0))

        self.update_button = ttk.Button(self.frame, text="Upravit Oddělení",
                                        command=self.update_department)
        self.update_button.grid(row=6, column=0, columnspan=2, pady=(10, 0))

        self.delete_button = ttk.Button(self.frame, text="Smazat Oddělení",
                                        command=self.delete_department)
        self.delete_button.grid(row=7, column=0, columnspan=2, pady=(10, 0))

        self.refresh_departments()


    def refresh_departments(self):
        for i in self.department_tree.get_children():
            self.department_tree.delete(i)
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Departments")
        rows = cursor.fetchall()
        for row in rows:
            self.department_tree.insert("", "end", values=row)
        conn.close()

    def insert_department(self):
        name = self.name_entry.get()
        budget = self.budget_entry.get()
        establishment_date = self.establishment_date_entry.get()
        if not name or not budget or not establishment_date:
            messagebox.showerror("Chyba", "Všechna pole jsou povinná")
            return

        try:
            budget = float(budget)
        except ValueError:
            messagebox.showerror("Chyba", "Rozpočet musí být číslo")
            return

        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Departments (name, budget, establishment_date) VALUES (?, ?, ?)", 
                       (name, budget, establishment_date))
        conn.commit()
        conn.close()

        self.refresh_departments()
        self.name_entry.delete(0, tk.END)
        self.budget_entry.delete(0, tk.END)
        self.establishment_date_entry.delete(0, tk.END)

    def update_department(self):
        selected_item = self.department_tree.selection()
        if selected_item:
            name = self.name_entry.get()
            budget = self.budget_entry.get()
            establishment_date = self.establishment_date_entry.get()
            if not name or not budget or not establishment_date:
                messagebox.showerror("Chyba", "Všechna pole jsou povinná")
                return

            try:
                budget = float(budget)
            except ValueError:
                messagebox.showerror("Chyba", "Rozpočet musí být číslo")
                return

            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute('''UPDATE Departments 
                              SET name=?, budget=?, establishment_date=? 
                              WHERE department_id=?''',
                           (name, budget, establishment_date, self.selected_department_id))
            conn.commit()
            conn.close()

            self.refresh_departments()
            self.name_entry.delete(0, tk.END)
            self.budget_entry.delete(0, tk.END)
            self.establishment_date_entry.delete(0, tk.END)

    def delete_department(self):
        selected_item = self.department_tree.selection()
        if selected_item:
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Departments WHERE department_id=?", (self.selected_department_id,))
            conn.commit()
            conn.close()

            self.refresh_departments()
            self.name_entry.delete(0, tk.END)
            self.budget_entry.delete(0, tk.END)
            self.establishment_date_entry.delete(0, tk.END)

    def on_tree_select(self, event):
        selected_item = self.department_tree.selection()
        if selected_item:
            department = self.department_tree.item(selected_item, 'values')
            self.selected_department_id = department[0]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, department[1])
            self.budget_entry.delete(0, tk.END)
            self.budget_entry.insert(0, department[2])
            self.establishment_date_entry.delete(0, tk.END)
            self.establishment_date_entry.insert(0, department[3])
