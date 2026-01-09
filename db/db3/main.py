import tkinter as tk
from tkinter import ttk, messagebox
import configparser
import datetime
import os

from views.department_view import DepartmentView
from views.documentDepartment_view import DocumentDepartmentView
from views.document_view import DocumentView
from views.employeeProject_view import EmployeeProjectView
from views.employee_view import EmployeeView
from views.project_view import ProjectView

from database.database_connection import DatabaseConnection
from gateways.project_gateway import ProjectGateway
from database.report_generator import ReportGenerator

class Alpha:
    def __init__(self, root, config):
        self.root = root
        self.config = config
        self.root.title(config['Window']['title'])
        self.root.geometry(f"{config['Window']['width']}x{config['Window']['height']}")

        self.tabControl = ttk.Notebook(self.root)

        self.employee_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.employee_tab, text="Zaměstnanci")
        EmployeeView(self.employee_tab)

        self.department_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.department_tab, text="Oddělení")
        DepartmentView(self.department_tab)

        self.project_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.project_tab, text="Projekty")
        ProjectView(self.project_tab)

        self.employee_project_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.employee_project_tab, text="Zaměstnanci a Projekty")
        EmployeeProjectView(self.employee_project_tab)

        self.document_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.document_tab, text="Dokumenty")
        DocumentView(self.document_tab)

        self.document_department_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.document_department_tab, text="Dokumenty a Oddělení")
        DocumentDepartmentView(self.document_department_tab)

        self.admin_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.admin_tab, text="Administrace")
        self.setup_admin_tab()

        self.tabControl.pack(expand=1, fill="both")

    def setup_admin_tab(self):
        frame = tk.Frame(self.admin_tab, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        btn_trans = tk.Button(frame, text="Test Transakce (Vytvořit projekt + Manažer)", height=2, command=self.run_transaction)
        btn_trans.pack(fill="x", pady=10)

        btn_rep = tk.Button(frame, text="Generovat Report (CSV)", height=2, command=self.run_report)
        btn_rep.pack(fill="x", pady=10)

        btn_view = tk.Button(frame, text="Zobrazit statistiku (z VIEW)", height=2, command=self.show_stats)
        btn_view.pack(fill="x", pady=10)

    def run_transaction(self):
        try:
            db = DatabaseConnection()
            gateway = ProjectGateway(db)
            
            nazev = f"Projekt {datetime.datetime.now().strftime('%H:%M:%S')}"
            start = datetime.date.today()
            konec = datetime.date.today() + datetime.timedelta(days=30)
            manager_id = 1 

            new_id = gateway.create_project_with_manager(nazev, start, konec, manager_id)
            messagebox.showinfo("Hotovo", f"Transakce úspěšná.\nProjekt ID: {new_id}")
        
        except Exception as e:
            messagebox.showerror("Chyba", str(e))

    def run_report(self):
        try:
            generator = ReportGenerator()
            file_path = generator.generate_report()
            path = os.path.abspath(file_path)
            messagebox.showinfo("Hotovo", f"Report uložen:\n{path}")
        except Exception as e:
            messagebox.showerror("Chyba", str(e))

    def show_stats(self):
        try:
            db = DatabaseConnection()
            gateway = ProjectGateway(db)
            data = gateway.fetch_active_projects_stats()
            
            if not data:
                messagebox.showinfo("Info", "Žádná data v pohledu.")
                return

            msg = "Statistika aktivních projektů (z VIEW):\n\n"
            for row in data:
                msg += f"{row[0]} (Konec: {row[1]}) - Počet lidí: {row[2]}\n"
            
            messagebox.showinfo("VIEW Data", msg)
        except Exception as e:
            messagebox.showerror("Chyba", str(e))

if __name__ == '__main__':
    config_path = os.path.join('settings', 'config.ini')
    config = configparser.ConfigParser()
    
    if not os.path.exists(config_path):
        if not os.path.exists('settings'):
            os.makedirs('settings')
        config['Window'] = {'title': 'IS Zamestnanci', 'width': '800', 'height': '600'}
        config['Database'] = {'host': 'localhost', 'user': 'root', 'password': '', 'database': 'employee_management_db'}
        with open(config_path, 'w') as f:
            config.write(f)
    else:
        config.read(config_path)

    root = tk.Tk()
    app = Alpha(root, config)
    root.mainloop()