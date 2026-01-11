
import tkinter as tk
from tkinter import ttk, messagebox
from database.database_connection import DatabaseConnection

class DocumentDepartmentView:
    def __init__(self, parent):
        self.parent = parent
        self.db = DatabaseConnection('employeeManagement.db')
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(padx=10, pady=10)
        self.selected_document_id = None
        self.selected_department_id = None
        self.create_widgets()

    def create_widgets(self):
        self.document_label = ttk.Label(self.frame, text="Dokumenty:")
        self.document_label.grid(row=0, column=0, pady=(10, 5))
        self.document_listbox = tk.Listbox(self.frame)
        self.document_listbox.grid(row=1, column=0, pady=(0, 5))
        self.document_listbox.bind('<<ListboxSelect>>', self.on_document_select)

        self.department_label = ttk.Label(self.frame, text="Oddělení:")
        self.department_label.grid(row=0, column=1, pady=(10, 5))
        self.department_listbox = tk.Listbox(self.frame)
        self.department_listbox.grid(row=1, column=1, pady=(0, 5))
        self.department_listbox.bind('<<ListboxSelect>>', self.on_department_select)

        self.add_button = ttk.Button(self.frame, text="Přiřadit Dokument k Oddělení", command=self.add_document_to_department)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        self.remove_button = ttk.Button(self.frame, text="Odebrat Dokument z Oddělení", command=self.remove_document_from_department)
        self.remove_button.grid(row=3, column=0, columnspan=2, pady=(10, 0))

        self.refresh_document_list()
        self.refresh_department_list()

    def on_document_select(self, event):
        selection = self.document_listbox.curselection()
        if selection:
            entry = self.document_listbox.get(selection[0])
            self.selected_document_id = int(entry.split(":")[0])

    def on_department_select(self, event):
        selection = self.department_listbox.curselection()
        if selection:
            entry = self.department_listbox.get(selection[0])
            self.selected_department_id = int(entry.split(":")[0])

    def add_document_to_department(self):
        if self.selected_document_id is not None and self.selected_department_id is not None:
            conn = self.db.connect()
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO DocumentDepartments (document_id, department_id) VALUES (?, ?)",
                               (self.selected_document_id, self.selected_department_id))
                conn.commit()
                messagebox.showinfo("Úspěch", "Dokument byl přiřazen k oddělení")
            except Exception:
                messagebox.showerror("Chyba", "Tato vazba již existuje")
            finally:
                conn.close()
        else:
            messagebox.showerror("Chyba", "Musíte vybrat dokument a oddělení")

    def remove_document_from_department(self):
        if self.selected_document_id is not None and self.selected_department_id is not None:
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM DocumentDepartments WHERE document_id=? AND department_id=?",
                           (self.selected_document_id, self.selected_department_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Úspěch", "Vazba byla odstraněna")
        else:
            messagebox.showerror("Chyba", "Musíte vybrat dokument a oddělení")

    def refresh_document_list(self):
        self.document_listbox.delete(0, tk.END)
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT document_id, title FROM Documents")
        for document in cursor.fetchall():
            self.document_listbox.insert(tk.END, f"{document[0]}: {document[1]}")
        conn.close()

    def refresh_department_list(self):
        self.department_listbox.delete(0, tk.END)
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT department_id, name FROM Departments")
        for department in cursor.fetchall():
            self.department_listbox.insert(tk.END, f"{department[0]}: {department[1]}")

        conn.close()
