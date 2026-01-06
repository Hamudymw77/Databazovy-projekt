import csv
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database.database_connection import DatabaseConnection
from database.report_generator import ReportGenerator


class EmployeeView:
    def __init__(self, root):
        self.root = root
        self.db = DatabaseConnection('employeeManagement.db')
        self.report_generator = ReportGenerator('employeeManagement.db')
        self.create_widgets()

    def create_widgets(self):
        self.frame = ttk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)
        self.tabControl = ttk.Notebook(self.root)

        self.employee_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.employee_tab, text="Zaměstnanci")

        self.tabControl.pack(expand=1, fill="both")


        self.employee_frame = ttk.Frame(self.employee_tab)
        self.employee_frame.pack(padx=10, pady=10)

        self.employee_label = ttk.Label(self.employee_frame, text="Seznam zaměstnanců")
        self.employee_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        self.employee_tree = ttk.Treeview(self.employee_frame,
                                          columns=("employee_id", "name", "position", "salary", "is_manager"),
                                          show="headings")
        self.employee_tree.heading("employee_id", text="ID")
        self.employee_tree.heading("name", text="Jméno")
        self.employee_tree.heading("position", text="Pozice")
        self.employee_tree.heading("salary", text="Plat")
        self.employee_tree.heading("is_manager", text="Manažer")
        self.employee_tree.grid(row=1, column=0, columnspan=3)

        self.import_button = ttk.Button(self.frame, text="Importovat CSV", command=self.import_csv)
        self.import_button.grid(row=10, column=0, columnspan=2, pady=(10, 0))

        self.refresh_employees()

        self.name_label = ttk.Label(self.employee_frame, text="Jméno:")
        self.name_label.grid(row=2, column=0, pady=(10, 5))

        self.name_entry = ttk.Entry(self.employee_frame)
        self.name_entry.grid(row=2, column=1, pady=(10, 5))

        self.position_label = ttk.Label(self.employee_frame, text="Pozice:")
        self.position_label.grid(row=3, column=0, pady=(0, 5))

        self.position_entry = ttk.Entry(self.employee_frame)
        self.position_entry.grid(row=3, column=1, pady=(0, 5))

        self.salary_label = ttk.Label(self.employee_frame, text="Plat:")
        self.salary_label.grid(row=4, column=0, pady=(0, 5))

        self.salary_entry = ttk.Entry(self.employee_frame)
        self.salary_entry.grid(row=4, column=1, pady=(0, 5))

        self.is_manager_label = ttk.Label(self.employee_frame, text="Manažer:")
        self.is_manager_label.grid(row=5, column=0, pady=(0, 5))

        self.is_manager_var = tk.BooleanVar()
        self.is_manager_checkbox = ttk.Checkbutton(self.employee_frame, variable=self.is_manager_var)
        self.is_manager_checkbox.grid(row=5, column=1, pady=(0, 5))

        self.insert_employee_button = ttk.Button(self.employee_frame, text="Vložit zaměstnance",
                                                 command=self.insert_employee)
        self.insert_employee_button.grid(row=6, column=0, columnspan=2, pady=(10, 0))

        self.selected_employee_id = None

        self.update_employee_button = ttk.Button(self.employee_frame, text="Upravit zaměstnance",
                                                 command=self.update_employee)
        self.update_employee_button.grid(row=7, column=0, columnspan=2, pady=(10, 0))

        self.delete_employee_button = ttk.Button(self.employee_frame, text="Smazat zaměstnance",
                                                 command=self.delete_employee)
        self.delete_employee_button.grid(row=8, column=0, columnspan=2, pady=(10, 0))

        self.employee_tree.bind('<ButtonRelease-1>', self.on_tree_select)
        self.report_button = ttk.Button(self.frame, text="Vygenerovat Report",
                                        command=self.generate_report)
        self.report_button.grid(row=9, column=0, columnspan=2, pady=(10, 0))
    def refresh_employees(self):
        self.employee_tree.delete(*self.employee_tree.get_children())
        conn = sqlite3.connect('employeeManagement.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Employees')
        employees = cursor.fetchall()
        for employee in employees:
            self.employee_tree.insert("", "end", values=employee)
        conn.close()

    def insert_employee(self):
        name = self.name_entry.get()
        position = self.position_entry.get()
        salary = float(self.salary_entry.get())
        is_manager = self.is_manager_var.get()

        conn = sqlite3.connect('employeeManagement.db')
        cursor = conn.cursor()
        cursor.execute('''
               INSERT INTO Employees (name, position, salary, is_manager) 
               VALUES (?, ?, ?, ?)
           ''', (name, position, salary, is_manager))
        conn.commit()
        conn.close()

        self.refresh_employees()
        self.name_entry.delete(0, 'end')
        self.position_entry.delete(0, 'end')
        self.salary_entry.delete(0, 'end')
        self.is_manager_var.set(False)

    def on_tree_select(self, event):
        selected_item = self.employee_tree.selection()
        if selected_item:
            values = self.employee_tree.item(selected_item)['values']
            self.selected_employee_id = values[0]
            self.name_entry.delete(0, 'end')
            self.name_entry.insert(0, values[1])
            self.position_entry.delete(0, 'end')
            self.position_entry.insert(0, values[2])
            self.salary_entry.delete(0, 'end')
            self.salary_entry.insert(0, values[3])
            self.is_manager_var.set(values[4])

    def update_employee(self):
        if self.selected_employee_id:
            name = self.name_entry.get()
            position = self.position_entry.get()
            salary = float(self.salary_entry.get())
            is_manager = self.is_manager_var.get()

            conn = sqlite3.connect('employeeManagement.db')
            cursor = conn.cursor()
            cursor.execute('''
                   UPDATE Employees 
                   SET name=?, position=?, salary=?, is_manager=? 
                   WHERE employee_id=?
               ''', (name, position, salary, is_manager, self.selected_employee_id))
            conn.commit()
            conn.close()

            self.refresh_employees()
            self.selected_employee_id = None
            self.name_entry.delete(0, 'end')
            self.position_entry.delete(0, 'end')
            self.salary_entry.delete(0, 'end')
            self.is_manager_var.set(False)

    def delete_employee(self):
        if self.selected_employee_id:
            conn = sqlite3.connect('employeeManagement.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM Employees WHERE employee_id = ?', (self.selected_employee_id,))
            conn.commit()
            conn.close()

            self.refresh_employees()
            self.selected_employee_id = None
            self.name_entry.delete(0, 'end')
            self.position_entry.delete(0, 'end')
            self.salary_entry.delete(0, 'end')
            self.is_manager_var.set(False)

    def generate_report(self):
        try:
            file_path = self.report_generator.generate_report()
            messagebox.showinfo("Report Generated", f"Report was generated successfully. File: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                conn = sqlite3.connect('employeeManagement.db')
                cursor = conn.cursor()
                reader = csv.DictReader(file)  # Assuming the CSV has headers
                for row in reader:
                    cursor.execute('''
                           INSERT INTO Employees (name, position, salary, is_manager)
                           VALUES (?, ?, ?, ?)
                       ''', (row['name'], row['position'], row['salary'], row['is_manager']))
                conn.commit()
                conn.close()

            messagebox.showinfo("Import Successful", "Data was successfully imported from the CSV file.")
            self.refresh_employees()  # Refresh the UI to display the newly imported data
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during import: {e}")