import tkinter as tk
from tkinter import ttk, messagebox
from gateways.employee_gateway import EmployeeGateway
from database.database_connection import DatabaseConnection

class EmployeeView:
    def __init__(self, parent):
        self.parent = parent
        self.db = DatabaseConnection()
        self.gateway = EmployeeGateway(self.db)
        
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(padx=10, pady=10)
        self.selected_employee_id = None
        
        self.is_manager_var = tk.BooleanVar()
        
        self.create_widgets()

    def create_widgets(self):
        self.employee_label = ttk.Label(self.frame, text="Seznam zaměstnanců")
        self.employee_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        self.employee_tree = ttk.Treeview(self.frame,
                                          columns=("employee_id", "name", "position", "salary", "is_manager"),
                                          show="headings")
        self.employee_tree.heading("employee_id", text="ID")
        self.employee_tree.heading("name", text="Jméno")
        self.employee_tree.heading("position", text="Pozice")
        self.employee_tree.heading("salary", text="Plat")
        self.employee_tree.heading("is_manager", text="Manažer")
        
        self.employee_tree.column("employee_id", width=50)
        self.employee_tree.column("name", width=150)
        self.employee_tree.column("position", width=150)
        self.employee_tree.column("salary", width=100)
        self.employee_tree.column("is_manager", width=80)
        
        self.employee_tree.grid(row=1, column=0, columnspan=3)
        self.employee_tree.bind('<ButtonRelease-1>', self.on_tree_select)

        tk.Label(self.frame, text="Jméno:").grid(row=2, column=0, sticky="e")
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.grid(row=2, column=1, sticky="w")

        tk.Label(self.frame, text="Pozice:").grid(row=3, column=0, sticky="e")
        self.position_entry = tk.Entry(self.frame)
        self.position_entry.grid(row=3, column=1, sticky="w")

        tk.Label(self.frame, text="Plat:").grid(row=4, column=0, sticky="e")
        self.salary_entry = tk.Entry(self.frame)
        self.salary_entry.grid(row=4, column=1, sticky="w")

        self.manager_check = tk.Checkbutton(self.frame, text="Je manažer", variable=self.is_manager_var)
        self.manager_check.grid(row=5, column=1, sticky="w")

        self.add_btn = tk.Button(self.frame, text="Přidat zaměstnance", command=self.insert_employee)
        self.add_btn.grid(row=6, column=0, pady=10)

        self.update_btn = tk.Button(self.frame, text="Upravit", command=self.update_employee)
        self.update_btn.grid(row=6, column=1, pady=10)

        self.delete_btn = tk.Button(self.frame, text="Smazat", command=self.delete_employee)
        self.delete_btn.grid(row=6, column=2, pady=10)
        
        self.clear_btn = tk.Button(self.frame, text="Vyčistit pole", command=self.clear_entries)
        self.clear_btn.grid(row=7, column=1, pady=5)

        self.refresh_employees()

    def refresh_employees(self):
        for i in self.employee_tree.get_children():
            self.employee_tree.delete(i)
        
        try:
            rows = self.gateway.fetch_all()
            
            for row in rows:
                display_row = list(row)
                if len(display_row) > 4:
                    display_row[4] = "Ano" if display_row[4] else "Ne"
                
                self.employee_tree.insert("", "end", values=display_row)
        except Exception as e:
            messagebox.showerror("Chyba", f"Nepodařilo se načíst data: {e}")

    def insert_employee(self):
        name = self.name_entry.get()
        position = self.position_entry.get()
        salary = self.salary_entry.get()
        is_manager = self.is_manager_var.get()

        if name and position and salary:
            try:
                # Konverze platu na číslo
                salary_float = float(salary)
                
                # Voláme Gateway
                self.gateway.insert(name, position, salary_float, is_manager)
                
                self.refresh_employees()
                self.clear_entries()
                messagebox.showinfo("Úspěch", "Zaměstnanec přidán")
            except ValueError:
                 messagebox.showerror("Chyba", "Plat musí být číslo!")
            except Exception as e:
                messagebox.showerror("Chyba", f"Chyba při ukládání: {e}")
        else:
            messagebox.showwarning("Varování", "Vyplňte jméno, pozici a plat")

    def update_employee(self):
        if self.selected_employee_id:
            name = self.name_entry.get()
            position = self.position_entry.get()
            salary = self.salary_entry.get()
            is_manager = self.is_manager_var.get()
            
            try:
                salary_float = float(salary)
                
                self.gateway.update(self.selected_employee_id, name, position, salary_float, is_manager)
                
                self.refresh_employees()
                self.clear_entries()
                messagebox.showinfo("Úspěch", "Zaměstnanec byl upraven")
            except ValueError:
                 messagebox.showerror("Chyba", "Plat musí být číslo!")
            except Exception as e:
                messagebox.showerror("Chyba", f"Chyba při úpravě: {e}")
        else:
            messagebox.showwarning("Varování", "Vyberte zaměstnance k úpravě")

    def delete_employee(self):
        if self.selected_employee_id:
            confirm = messagebox.askyesno("Potvrzení", "Opravdu smazat tohoto zaměstnance?")
            if confirm:
                try:
                    # Voláme Gateway
                    self.gateway.delete(self.selected_employee_id)
                    
                    self.refresh_employees()
                    self.clear_entries()
                    messagebox.showinfo("Úspěch", "Zaměstnanec smazán")
                except Exception as e:
                    messagebox.showerror("Chyba", f"Chyba při mazání: {e}")
        else:
             messagebox.showwarning("Varování", "Vyberte zaměstnance ke smazání")

    def on_tree_select(self, event):
        selected_item = self.employee_tree.selection()
        if selected_item:
            emp = self.employee_tree.item(selected_item, 'values')
            self.selected_employee_id = emp[0]
            
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, emp[1])
            
            self.position_entry.delete(0, tk.END)
            self.position_entry.insert(0, emp[2])
            
            self.salary_entry.delete(0, tk.END)
            self.salary_entry.insert(0, emp[3])
            
            is_man = True if emp[4] == "Ano" else False
            self.is_manager_var.set(is_man)

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.position_entry.delete(0, tk.END)
        self.salary_entry.delete(0, tk.END)
        self.is_manager_var.set(False)
        self.selected_employee_id = None