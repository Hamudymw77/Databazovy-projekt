import tkinter as tk
from tkinter import ttk, messagebox
from database.database_connection import DatabaseConnection
from mysql.connector import Error

class DocumentDepartmentView:
    def __init__(self, parent):
        self.parent = parent
        self.db = DatabaseConnection() 
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(padx=10, pady=10)
        self.selected_doc_id = None
        self.selected_dep_id = None
        self.create_widgets()

    def create_widgets(self):
        self.doc_label = ttk.Label(self.frame, text="Dokumenty:")
        self.doc_label.grid(row=0, column=0, pady=(10, 5))
        self.doc_listbox = tk.Listbox(self.frame, exportselection=False)
        self.doc_listbox.grid(row=1, column=0, pady=(0, 5))
        self.doc_listbox.bind('<<ListboxSelect>>', self.on_doc_select)

        self.dep_label = ttk.Label(self.frame, text="Oddělení:")
        self.dep_label.grid(row=0, column=1, pady=(10, 5))
        self.dep_listbox = tk.Listbox(self.frame, exportselection=False)
        self.dep_listbox.grid(row=1, column=1, pady=(0, 5))
        self.dep_listbox.bind('<<ListboxSelect>>', self.on_dep_select)

        self.add_btn = ttk.Button(self.frame, text="Přiřadit (M:N)", command=self.add_link)
        self.add_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.refresh_lists()

    def refresh_lists(self):
        self.doc_listbox.delete(0, tk.END)
        self.dep_listbox.delete(0, tk.END)
        conn = self.db.connect()
        if not conn: return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT document_id, title FROM Documents")
            for row in cursor.fetchall():
                self.doc_listbox.insert(tk.END, f"{row[0]}: {row[1]}")
            
            cursor.execute("SELECT department_id, name FROM Departments")
            for row in cursor.fetchall():
                self.dep_listbox.insert(tk.END, f"{row[0]}: {row[1]}")
        except Error as e:
            messagebox.showerror("Chyba", str(e))
        finally:
            conn.close()

    def on_doc_select(self, event):
        if self.doc_listbox.curselection():
            entry = self.doc_listbox.get(self.doc_listbox.curselection()[0])
            self.selected_doc_id = int(entry.split(":")[0])

    def on_dep_select(self, event):
        if self.dep_listbox.curselection():
            entry = self.dep_listbox.get(self.dep_listbox.curselection()[0])
            self.selected_dep_id = int(entry.split(":")[0])

    def add_link(self):
        if self.selected_doc_id and self.selected_dep_id:
            conn = self.db.connect()
            try:
                cursor = conn.cursor()
                sql = "INSERT INTO DocumentDepartments (document_id, department_id) VALUES (%s, %s)"
                cursor.execute(sql, (self.selected_doc_id, self.selected_dep_id))
                conn.commit()
                messagebox.showinfo("Úspěch", "Dokument přiřazen k oddělení.")
            except Error as e:
                messagebox.showerror("Chyba", f"Chyba přiřazení:\n{e}")
            finally:
                conn.close()
        else:
            messagebox.showwarning("Varování", "Vyberte oboje.")
