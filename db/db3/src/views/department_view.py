import tkinter as tk
from tkinter import ttk, messagebox
from gateways.department_gateway import DepartmentGateway
from database.database_connection import DatabaseConnection

class DepartmentView:
    def __init__(self, parent):
        self.parent = parent
        self.db = DatabaseConnection()
        self.gateway = DepartmentGateway(self.db)
        
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

        tk.Label(self.frame, text="Název oddělení:").grid(row=2, column=0, sticky="e")
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.grid(row=2, column=1, sticky="w")

        tk.Label(self.frame, text="Rozpočet:").grid(row=3, column=0, sticky="e")
        self.budget_entry = tk.Entry(self.frame)
        self.budget_entry.grid(row=3, column=1, sticky="w")

        tk.Label(self.frame, text="Datum vzniku (RRRR-MM-DD):").grid(row=4, column=0, sticky="e")
        self.establishment_date_entry = tk.Entry(self.frame)
        self.establishment_date_entry.grid(row=4, column=1, sticky="w")

        self.add_btn = tk.Button(self.frame, text="Přidat oddělení", command=self.insert_department)
        self.add_btn.grid(row=5, column=0, pady=10)

        self.update_btn = tk.Button(self.frame, text="Upravit oddělení", command=self.update_department)
        self.update_btn.grid(row=5, column=1, pady=10)

        self.delete_btn = tk.Button(self.frame, text="Smazat oddělení", command=self.delete_department)
        self.delete_btn.grid(row=5, column=2, pady=10)

        self.refresh_departments()

    def refresh_departments(self):
        for i in self.department_tree.get_children():
            self.department_tree.delete(i)
        
        try:
            rows = self.gateway.fetch_all()
            for row in rows:
                self.department_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Chyba", f"Chyba načítání: {e}")

    def insert_department(self):
        name = self.name_entry.get()
        budget = self.budget_entry.get()
        establishment_date = self.establishment_date_entry.get()

        if name and budget and establishment_date:
            try:
                self.gateway.insert(name, float(budget), establishment_date)
                
                self.refresh_departments()
                self.clear_entries()
                messagebox.showinfo("Úspěch", "Oddělení přidáno")
            except ValueError:
                messagebox.showerror("Chyba", "Rozpočet musí být číslo")
            except Exception as e:
                messagebox.showerror("Chyba", f"Chyba při ukládání: {e}")
        else:
            messagebox.showwarning("Varování", "Všechna pole musí být vyplněna")

    def update_department(self):
        if self.selected_department_id:
            name = self.name_entry.get()
            budget = self.budget_entry.get()
            establishment_date = self.establishment_date_entry.get()
            
            try:
                self.gateway.update(self.selected_department_id, name, float(budget), establishment_date)
                
                self.refresh_departments()
                self.clear_entries()
                messagebox.showinfo("Úspěch", "Oddělení upraveno")
            except ValueError:
                messagebox.showerror("Chyba", "Rozpočet musí být číslo")
            except Exception as e:
                messagebox.showerror("Chyba", f"Chyba při úpravě: {e}")
        else:
            messagebox.showwarning("Varování", "Vyberte oddělení")

    def delete_department(self):
        if self.selected_department_id:
            try:
                self.gateway.delete(self.selected_department_id)
                
                self.refresh_departments()
                self.clear_entries()
                messagebox.showinfo("Úspěch", "Oddělení smazáno")
            except Exception as e:
                messagebox.showerror("Chyba", f"Chyba při mazání: {e}")
        else:
             messagebox.showwarning("Varování", "Vyberte oddělení ke smazání")

    def on_tree_select(self, event):
        selected_item = self.department_tree.selection()
        if selected_item:
            dep = self.department_tree.item(selected_item, 'values')
            self.selected_department_id = dep[0]
            
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, dep[1])
            self.budget_entry.delete(0, tk.END)
            self.budget_entry.insert(0, dep[2])
            self.establishment_date_entry.delete(0, tk.END)
            self.establishment_date_entry.insert(0, dep[3])

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.budget_entry.delete(0, tk.END)
        self.establishment_date_entry.delete(0, tk.END)

        self.selected_department_id = None
