import tkinter as tk
from tkinter import ttk, messagebox
from gateways.project_gateway import ProjectGateway 
from database.database_connection import DatabaseConnection

class ProjectView:
    def __init__(self, parent):
        self.parent = parent
        self.db = DatabaseConnection() 
        self.gateway = ProjectGateway(self.db)
        
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

        # Vstupní prvky
        tk.Label(self.frame, text="Název projektu").grid(row=2, column=0)
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.grid(row=2, column=1)

        tk.Label(self.frame, text="Datum začátku (RRRR-MM-DD)").grid(row=3, column=0)
        self.start_date_entry = tk.Entry(self.frame)
        self.start_date_entry.grid(row=3, column=1)

        tk.Label(self.frame, text="Datum konce (RRRR-MM-DD)").grid(row=4, column=0)
        self.end_date_entry = tk.Entry(self.frame)
        self.end_date_entry.grid(row=4, column=1)

        # Tlačítka
        self.add_btn = tk.Button(self.frame, text="Přidat projekt", command=self.insert_project)
        self.add_btn.grid(row=5, column=0, pady=10)

        self.update_btn = tk.Button(self.frame, text="Upravit projekt", command=self.update_project)
        self.update_btn.grid(row=5, column=1, pady=10)

        self.delete_btn = tk.Button(self.frame, text="Smazat projekt", command=self.delete_project)
        self.delete_btn.grid(row=5, column=2, pady=10)

        self.refresh_projects()

    def refresh_projects(self):
        for i in self.project_tree.get_children():
            self.project_tree.delete(i)
        
        try:
            projects = self.gateway.fetch_all()
            for row in projects:
                self.project_tree.insert("", "end", values=row)
        except Exception as e:
            print(f"Chyba načítání: {e}")

    def insert_project(self):
        name = self.name_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        if name and start_date and end_date:
            try:
                self.gateway.insert(name, start_date, end_date)
                
                self.refresh_projects()
                self.clear_entries()
                messagebox.showinfo("Úspěch", "Projekt byl přidán")
            except Exception as e:
                messagebox.showerror("Chyba", f"Chyba při ukládání: {e}")
        else:
            messagebox.showwarning("Varování", "Všechna pole musí být vyplněna")

    def update_project(self):
        name = self.name_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        if self.selected_project_id and name and start_date and end_date:
            try:
                self.gateway.update(self.selected_project_id, name, start_date, end_date)
                
                self.refresh_projects()
                self.clear_entries()
                messagebox.showinfo("Úspěch", "Projekt byl aktualizován")
            except Exception as e:
                messagebox.showerror("Chyba", f"Chyba při aktualizaci: {e}")
        else:
             messagebox.showwarning("Varování", "Vyberte projekt a vyplňte údaje")

    def delete_project(self):
        if self.selected_project_id:
            try:
                self.gateway.delete(self.selected_project_id)
                
                self.refresh_projects()
                self.clear_entries()
                messagebox.showinfo("Úspěch", "Projekt byl smazán")
            except Exception as e:
                messagebox.showerror("Chyba", f"Chyba při mazání: {e}")
        else:
            messagebox.showwarning("Varování", "Vyberte projekt ke smazání")

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

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.start_date_entry.delete(0, tk.END)
        self.end_date_entry.delete(0, tk.END)
        self.selected_project_id = None