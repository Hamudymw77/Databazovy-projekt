import tkinter as tk
from tkinter import ttk, messagebox
from database.database_connection import DatabaseConnection

class ProjectView:
    def __init__(self, parent):
        self.parent = parent
        self.db = DatabaseConnection('employeeManagement.db')
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(padx=10, pady=10)
        self.selected_project_id = None
        self.create_widgets()

    def create_widgets(self):
        self.project_label = ttk.Label(self.frame, text="Seznam projektů")
        self.project_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        self.project_tree = ttk.Treeview(self.frame,
                                         columns=("project_id", "name", "start_date", "end_date"),
                                         show="headings")
        self.project_tree.heading("project_id", text="ID")
        self.project_tree.heading("name", text="Název projektu")
        self.project_tree.heading("start_date", text="Datum začátku")
        self.project_tree.heading("end_date", text="Datum konce")
        self.project_tree.grid(row=1, column=0, columnspan=3)
        self.project_tree.bind('<ButtonRelease-1>', self.on_tree_select)

        # Vstupní prvky pro vložení projektu
        self.name_label = ttk.Label(self.frame, text="Název projektu:")
        self.name_label.grid(row=2, column=0, pady=(10, 5))
        self.name_entry = ttk.Entry(self.frame)
        self.name_entry.grid(row=2, column=1, pady=(10, 5))

        self.start_date_label = ttk.Label(self.frame, text="Datum začátku:")
        self.start_date_label.grid(row=3, column=0, pady=(0, 5))
        self.start_date_entry = ttk.Entry(self.frame)
        self.start_date_entry.grid(row=3, column=1, pady=(0, 5))

        self.end_date_label = ttk.Label(self.frame, text="Datum konce:")
        self.end_date_label.grid(row=4, column=0, pady=(0, 5))
        self.end_date_entry = ttk.Entry(self.frame)
        self.end_date_entry.grid(row=4, column=1, pady=(0, 5))

        self.insert_button = ttk.Button(self.frame, text="Vložit Projekt", command=self.insert_project)
        self.insert_button.grid(row=5, column=0, columnspan=2, pady=(10, 0))

        self.update_button = ttk.Button(self.frame, text="Upravit Projekt", command=self.update_project)
        self.update_button.grid(row=6, column=0, columnspan=2, pady=(10, 0))

        self.delete_button = ttk.Button(self.frame, text="Smazat Projekt", command=self.delete_project)
        self.delete_button.grid(row=7, column=0, columnspan=2, pady=(10, 0))

        self.refresh_projects()

    def refresh_projects(self):
        for i in self.project_tree.get_children():
            self.project_tree.delete(i)
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Projects")
        rows = cursor.fetchall()
        for row in rows:
            self.project_tree.insert("", "end", values=row)
        conn.close()

    def insert_project(self):
        name = self.name_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        if not name or not start_date:
            messagebox.showerror("Chyba", "Název a datum začátku jsou povinné pole")
            return

        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Projects (name, start_date, end_date) VALUES (?, ?, ?)",
                       (name, start_date, end_date))
        conn.commit()
        conn.close()

        self.refresh_projects()
        self.name_entry.delete(0, tk.END)
        self.start_date_entry.delete(0, tk.END)
        self.end_date_entry.delete(0, tk.END)

    def update_project(self):
        selected_item = self.project_tree.selection()
        if selected_item:
            name = self.name_entry.get()
            start_date = self.start_date_entry.get()
            end_date = self.end_date_entry.get()
            if not name or not start_date:
                messagebox.showerror("Chyba", "Název a datum začátku jsou povinné pole")
                return

            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute('''UPDATE Projects 
                              SET name=?, start_date=?, end_date=? 
                              WHERE project_id=?''',
                           (name, start_date, end_date, self.selected_project_id))
            conn.commit()
            conn.close()

            self.refresh_projects()
            self.name_entry.delete(0, tk.END)
            self.start_date_entry.delete(0, tk.END)
            self.end_date_entry.delete(0, tk.END)

    def delete_project(self):
        selected_item = self.project_tree.selection()
        if selected_item:
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Projects WHERE project_id=?", (self.selected_project_id,))
            conn.commit()
            conn.close()

            self.refresh_projects()
            self.name_entry.delete(0, tk.END)
            self.start_date_entry.delete(0, tk.END)
            self.end_date_entry.delete(0, tk.END)

    def on_tree_select(self, event):
        selected_item = self.project_tree.selection()
        if selected_item:
            project = self.project_tree.item(selected_item, 'values')
            self.selected_project_id = project[0]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, project[1])
            self.start_date_entry.delete(0, tk.END)
            self.start_date_entry.insert(0, project[2])
            self.end_date_entry.delete(0, tk.END)
            self.end_date_entry.insert(0, project[3])