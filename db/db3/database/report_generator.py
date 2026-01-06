# report_generator.py
import csv
import datetime
from database.database_connection import DatabaseConnection
import os

class ReportGenerator:
    def __init__(self, db_path, reports_dir='reports'):
        self.db_path = db_path
        self.reports_dir = reports_dir

    def generate_report(self):
        db = DatabaseConnection(self.db_path)
        conn = db.connect()
        cursor = conn.cursor()

        cursor.execute("""
             SELECT e.name, e.position, e.salary, d.name AS department_name, p.name AS project_name
            FROM Employees e
            LEFT JOIN EmployeeProjects ep ON e.employee_id = ep.employee_id
            LEFT JOIN Projects p ON ep.project_id = p.project_id
            LEFT JOIN DocumentDepartments dd ON e.employee_id = dd.department_id
            LEFT JOIN Departments d ON dd.department_id = d.department_id
        """)
        data = cursor.fetchall()

        conn.close()

        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)


        filename = f'report{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv'
        filepath = os.path.join(self.reports_dir, filename)

        with open(filepath, 'w', newline='') as file:
            writer = csv.writer(file)

            writer.writerow(["Report:"])
            writer.writerow(["Generated at:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            writer.writerow([])  # Empty line
            writer.writerow(["Employee Name", "Department Name", "Project Name"])  # Column headers

            for row in data:
                writer.writerow(row)

            writer.writerow([])  # Empty line
            writer.writerow(["End of Report"])

        return filepath
