import tkinter as tk
from tkinter import ttk, messagebox
from database.database_connection import DatabaseConnection

class EmployeeProjectView:
    def __init__(self, parent):
        self.parent = parent
        self.db = DatabaseConnection('employeeManagement.db')
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(padx=10, pady=10)
        self.selected_employee_id = None
        self.selected_project_id = None
        self.create_widgets()

    def create_widgets(self):
        self.employee_label = ttk.Label(self.frame, text="Zaměstnanci:")
        self.employee_label.grid(row=0, column=0, pady=(10, 5))
        self.employee_listbox = tk.Listbox(self.frame)
        self.employee_listbox.grid(row=1, column=0, pady=(0, 5))
        self.employee_listbox.bind('<<ListboxSelect>>', self.on_employee_select)

        self.project_label = ttk.Label(self.frame, text="Projekty:")
        self.project_label.grid(row=0, column=1, pady=(10, 5))
        self.project_listbox = tk.Listbox(self.frame)
        self.project_listbox.grid(row=1, column=1, pady=(0, 5))
        self.project_listbox.bind('<<ListboxSelect>>', self.on_project_select)

        self.add_button = ttk.Button(self.frame, text="Přiřadit Zaměstnance k Projektu", command=self.add_employee_to_project)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        self.remove_button = ttk.Button(self.frame, text="Odebrat Zaměstnance z Projektu", command=self.remove_employee_from_project)
        self.remove_button.grid(row=3, column=0, columnspan=2, pady=(10, 0))

        self.refresh_employee_list()
        self.refresh_project_list()

    def on_employee_select(self, event):
            selection = self.employee_listbox.curselection()
            if selection:
                entry = self.employee_listbox.get(selection[0])
                self.selected_employee_id = int(entry.split(":")[0])

    def on_project_select(self, event):
            selection = self.project_listbox.curselection()
            if selection:
                entry = self.project_listbox.get(selection[0])
                self.selected_project_id = int(entry.split(":")[0])

    def add_employee_to_project(self):
            if self.selected_employee_id is not None and self.selected_project_id is not None:
                conn = self.db.connect()
                cursor = conn.cursor()
                try:
                    cursor.execute("INSERT INTO EmployeeProjects (employee_id, project_id) VALUES (?, ?)",
                                   (self.selected_employee_id, self.selected_project_id))
                    conn.commit()
                    messagebox.showinfo("Úspěch", "Zaměstnanec byl přiřazen k projektu")
                except Exception:
                    messagebox.showerror("Chyba", "Tato vazba již existuje")
                finally:
                    conn.close()
            else:
                messagebox.showerror("Chyba", "Musíte vybrat zaměstnance a projekt")
            self.refresh_employee_list()
            self.refresh_project_list()
    def remove_employee_from_project(self):
            if self.selected_employee_id is not None and self.selected_project_id is not None:
                conn = self.db.connect()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM EmployeeProjects WHERE employee_id=? AND project_id=?",
                               (self.selected_employee_id, self.selected_project_id))
                conn.commit()
                conn.close()
                messagebox.showinfo("Úspěch", "Vazba byla odstraněna")
            else:
                messagebox.showerror("Chyba", "Musíte vybrat zaměstnance a projekt")
            self.refresh_employee_list()
            self.refresh_project_list()
    def refresh_employee_list(self):
            self.employee_listbox.delete(0, tk.END)
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT employee_id, name FROM Employees")
            for employee in cursor.fetchall():
                self.employee_listbox.insert(tk.END, f"{employee[0]}: {employee[1]}")
            conn.close()

    def refresh_project_list(self):
            self.project_listbox.delete(0, tk.END)
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT project_id, name FROM Projects")
            for project in cursor.fetchall():
                self.project_listbox.insert(tk.END, f"{project[0]}: {project[1]}")

            conn.close()
