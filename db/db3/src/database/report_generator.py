import csv
import datetime
from database.database_connection import DatabaseConnection
import os

class ReportGenerator:
    def __init__(self, db_path=None, reports_dir='reports'):
        self.reports_dir = reports_dir

    def generate_report(self):
        db = DatabaseConnection() 
        conn = db.connect()
        
        if not conn:
            print("Chyba: Nepodařilo se připojit k DB pro report.")
            return None

        cursor = conn.cursor()

     
        query = """
            SELECT 
                e.name AS Employee, 
                e.position AS Position, 
                d.name AS Department, 
                p.name AS Project,
                pa.role AS Role_In_Project
            FROM Employees e
            LEFT JOIN Departments d ON e.department_id = d.department_id
            LEFT JOIN Project_Assignments pa ON e.employee_id = pa.employee_id
            LEFT JOIN Projects p ON pa.project_id = p.project_id
            ORDER BY d.name, e.name
        """
        
        cursor.execute(query)
        data = cursor.fetchall()
        
        column_names = [i[0] for i in cursor.description]

        cursor.close()
        conn.close()

        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)

        filename = f'report_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv'
        filepath = os.path.join(self.reports_dir, filename)

        with open(filepath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            writer.writerow(["COMPLEX REPORT"])
            writer.writerow(["Generated at:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            writer.writerow([]) 
            writer.writerow(column_names)  

            for row in data:
                writer.writerow(row)

            writer.writerow([])
            writer.writerow(["End of Report"])

        print(f"Report vygenerován: {filepath}")

        return filepath
