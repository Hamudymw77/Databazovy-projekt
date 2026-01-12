import tkinter as tk
from tkinter import ttk, messagebox
from database.database_connection import DatabaseConnection
from mysql.connector import Error

class EmployeeProjectView:
    def __init__(self, parent):
        self.parent = parent
        self.db = DatabaseConnection()
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(padx=10, pady=10)
        self.selected_employee_id = None
        self.selected_project_id = None
        self.create_widgets()

    def create_widgets(self):
        # Layout
        self.employee_label = ttk.Label(self.frame, text="Zaměstnanci:")
        self.employee_label.grid(row=0, column=0, pady=(10, 5))
        self.employee_listbox = tk.Listbox(self.frame, exportselection=False)
        self.employee_listbox.grid(row=1, column=0, pady=(0, 5))
        self.employee_listbox.bind('<<ListboxSelect>>', self.on_employee_select)

        self.project_label = ttk.Label(self.frame, text="Projekty:")
        self.project_label.grid(row=0, column=1, pady=(10, 5))
        self.project_listbox = tk.Listbox(self.frame, exportselection=False)
        self.project_listbox.grid(row=1, column=1, pady=(0, 5))
        self.project_listbox.bind('<<ListboxSelect>>', self.on_project_select)

        self.add_button = ttk.Button(self.frame, text="Přiřadit (M:N)", command=self.add_employee_to_project)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        self.remove_button = ttk.Button(self.frame, text="Odebrat vazbu", command=self.remove_employee_from_project)
        self.remove_button.grid(row=3, column=0, columnspan=2, pady=(10, 0))

        self.refresh_lists()

    def refresh_lists(self):
        self.employee_listbox.delete(0, tk.END)
        self.project_listbox.delete(0, tk.END)
        
        conn = self.db.connect()
        if not conn: return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT employee_id, name FROM Employees")
            for emp in cursor.fetchall():
                self.employee_listbox.insert(tk.END, f"{emp[0]}: {emp[1]}")
            
            cursor.execute("SELECT project_id, name FROM Projects")
            for proj in cursor.fetchall():
                self.project_listbox.insert(tk.END, f"{proj[0]}: {proj[1]}")
        except Error as e:
            messagebox.showerror("Chyba DB", str(e))
        finally:
            conn.close()

    def on_employee_select(self, event):
        if self.employee_listbox.curselection():
            entry = self.employee_listbox.get(self.employee_listbox.curselection()[0])
            self.selected_employee_id = int(entry.split(":")[0])

    def on_project_select(self, event):
        if self.project_listbox.curselection():
            entry = self.project_listbox.get(self.project_listbox.curselection()[0])
            self.selected_project_id = int(entry.split(":")[0])

    def add_employee_to_project(self):
        if self.selected_employee_id and self.selected_project_id:
            conn = self.db.connect()
            try:
                cursor = conn.cursor()
                sql = "INSERT INTO Project_Assignments (employee_id, project_id, role) VALUES (%s, %s, 'Member')"
                cursor.execute(sql, (self.selected_employee_id, self.selected_project_id))
                conn.commit()
                messagebox.showinfo("Úspěch", "Vazba vytvořena.")
            except Error as e:
                messagebox.showerror("Chyba", f"Nelze přiřadit (možná duplicita?):\n{e}")
            finally:
                conn.close()
        else:
            messagebox.showwarning("Varování", "Vyberte zaměstnance i projekt.")

    def remove_employee_from_project(self):
        if self.selected_employee_id and self.selected_project_id:
            conn = self.db.connect()
            try:
                cursor = conn.cursor()
                sql = "DELETE FROM Project_Assignments WHERE employee_id=%s AND project_id=%s"
                cursor.execute(sql, (self.selected_employee_id, self.selected_project_id))
                conn.commit()
                messagebox.showinfo("Úspěch", "Vazba odstraněna.")
            except Error as e:
                messagebox.showerror("Chyba", str(e))
            finally:
                conn.close()
        else:
            messagebox.showwarning("Varování", "Vyberte zaměstnance i projekt.")
