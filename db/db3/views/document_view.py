import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from database.database_connection import DatabaseConnection
import datetime

class DocumentView:
    def __init__(self, parent):
        self.parent = parent
        self.db = DatabaseConnection('employeeManagement.db')
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(padx=10, pady=10)
        self.selected_document_id = None
        self.create_widgets()

    def create_widgets(self):
        self.title_label = ttk.Label(self.frame, text="Titulek:")
        self.title_label.grid(row=0, column=0, pady=(10, 5))
        self.title_entry = ttk.Entry(self.frame)
        self.title_entry.grid(row=0, column=1, pady=(10, 5))

        self.content_label = ttk.Label(self.frame, text="Obsah:")
        self.content_label.grid(row=1, column=0, pady=(0, 5))
        self.content_text = tk.Text(self.frame, height=10, width=50)
        self.content_text.grid(row=1, column=1, pady=(0, 5))

        self.insert_button = ttk.Button(self.frame, text="Vytvořit Dokument", command=self.create_document)
        self.insert_button.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        self.update_button = ttk.Button(self.frame, text="Upravit Dokument", command=self.update_document)
        self.update_button.grid(row=3, column=0, columnspan=2, pady=(10, 0))

        self.delete_button = ttk.Button(self.frame, text="Smazat Dokument", command=self.delete_document)
        self.delete_button.grid(row=4, column=0, columnspan=2, pady=(10, 0))

        self.document_tree = ttk.Treeview(self.frame, columns=("document_id", "title", "content", "creation_date"), show="headings")
        self.document_tree.heading("document_id", text="ID")
        self.document_tree.heading("title", text="Titulek")
        self.document_tree.heading("content", text="Obsah")
        self.document_tree.heading("creation_date", text="Datum Vytvoření")
        self.document_tree.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        self.document_tree.bind('<ButtonRelease-1>', self.on_tree_select)


        self.refresh_document_list()

    def refresh_document_list(self):
        self.document_tree.delete(*self.document_tree.get_children())
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Documents")
        for document in cursor.fetchall():
            self.document_tree.insert("", "end", values=document)
        conn.close()

    def on_tree_select(self, event):
        selection = self.document_tree.selection()
        if selection:
            document = self.document_tree.item(selection, 'values')
            self.selected_document_id = document[0]
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, document[1])
            self.content_text.delete(1.0, tk.END)
            self.content_text.insert(tk.END, document[2])

    def create_document(self):
        title = self.title_entry.get()
        content = self.content_text.get(1.0, tk.END)
        creation_date = datetime.datetime.now()  # Automatické nastavení aktuálního datumu
        if not title or not content:
            messagebox.showerror("Chyba", "Titulek a obsah jsou povinné položky")
            return

        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Documents (title, content, creation_date) VALUES (?, ?, ?)",
                       (title, content, creation_date))
        conn.commit()
        conn.close()
        self.refresh_document_list()

    def update_document(self):
        if self.selected_document_id:
            title = self.title_entry.get()
            content = self.content_text.get(1.0, tk.END)
            if not title or not content:
                messagebox.showerror("Chyba", "Titulek a obsah jsou povinné položky")
                return

            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute("UPDATE Documents SET title=?, content=? WHERE document_id=?",
                           (title, content, self.selected_document_id))
            conn.commit()
            conn.close()
            self.refresh_document_list()

    def delete_document(self):
        if self.selected_document_id:
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Documents WHERE document_id=?", (self.selected_document_id,))
            conn.commit()
            conn.close()
            self.refresh_document_list()

    def create_document(self):
        title = self.title_entry.get()
        content = self.content_text.get(1.0, tk.END)
        creation_date = datetime.datetime.now()  # Automatické nastavení aktuálního datumu
        selected_departments = [self.department_selection.get(idx) for idx in
                                self.department_selection.curselection()]  # Příklad: ID oddělení pro přiřazení

        if not title or not content or not selected_departments:
            messagebox.showerror("Chyba", "Titulek, obsah a výběr oddělení jsou povinné položky")
            return

        conn = self.db.connect()
        try:
            conn.execute('BEGIN TRANSACTION;')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Documents (title, content, creation_date) VALUES (?, ?, ?)",
                           (title, content, creation_date))
            document_id = cursor.lastrowid

            for department in selected_departments:
                department_id = int(department.split(":")[0])  # Opraveno, používáme proměnnou 'department'
                cursor.execute("INSERT INTO DocumentDepartments (document_id, department_id) VALUES (?, ?)",
                               (document_id, department_id))

            conn.commit()
            messagebox.showinfo("Úspěch", "Dokument byl vytvořen a přiřazen k oddělením")
        except sqlite3.Error as e:
            conn.rollback()
            messagebox.showerror("Chyba", f"Při vytváření dokumentu došlo k chybě: {e}")
        finally:
            conn.close()
            self.refresh_document_list()

