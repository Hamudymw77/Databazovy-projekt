import tkinter as tk
from tkinter import ttk
import configparser


from views.department_view import DepartmentView
from views.documentDepartment_view import DocumentDepartmentView
from views.document_view import DocumentView
from views.employeeProject_view import EmployeeProjectView
from views.employee_view import EmployeeView
from views.project_view import ProjectView

class Alpha:
    def __init__(self, root):
        self.root = root
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

        self.tabControl.pack(expand=1, fill="both")

if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('settings\config.ini')
    root = tk.Tk()
    app = Alpha(root)
    root.mainloop()
