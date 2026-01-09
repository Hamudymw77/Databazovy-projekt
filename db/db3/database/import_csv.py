import mysql.connector
from mysql.connector import Error
import csv
import os

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'employee_management_db'
}

def create_tables_and_import():
    conn = None
    try:
        print("--- ZAČÍNÁM PŘÍPRAVU DATABÁZE ---")
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        print("Mazání starých tabulek a pohledů...")
        cursor.execute("DROP VIEW IF EXISTS View_Employee_Details")
        cursor.execute("DROP VIEW IF EXISTS View_Active_Projects")
        
        cursor.execute("DROP TABLE IF EXISTS Project_Assignments")
        cursor.execute("DROP TABLE IF EXISTS Documents")
        cursor.execute("DROP TABLE IF EXISTS Employees")
        cursor.execute("DROP TABLE IF EXISTS Projects")
        cursor.execute("DROP TABLE IF EXISTS Departments")

        print("Vytvářím nové tabulky...")
        
        cursor.execute("""
        CREATE TABLE Departments (
            department_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            budget FLOAT DEFAULT 0.0,
            establishment_date DATE
        ) ENGINE=InnoDB;
        """)

        cursor.execute("""
        CREATE TABLE Projects (
            project_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            start_date DATE,
            end_date DATE,
            status ENUM('planned', 'running', 'finished') DEFAULT 'planned'
        ) ENGINE=InnoDB;
        """)

        cursor.execute("""
        CREATE TABLE Employees (
            employee_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            position VARCHAR(100),
            salary DECIMAL(10, 2) DEFAULT 0,
            is_manager BOOLEAN DEFAULT FALSE,
            department_id INT,
            FOREIGN KEY (department_id) REFERENCES Departments(department_id)
        ) ENGINE=InnoDB;
        """)

        cursor.execute("""
        CREATE TABLE Documents (
            document_id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            content TEXT,
            department_id INT,
            FOREIGN KEY (department_id) REFERENCES Departments(department_id)
        ) ENGINE=InnoDB;
        """)

        # Vazebni tabulka M:N
        cursor.execute("""
        CREATE TABLE Project_Assignments (
            assignment_id INT AUTO_INCREMENT PRIMARY KEY,
            project_id INT,
            employee_id INT,
            role VARCHAR(50) DEFAULT 'Member',
            assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES Projects(project_id) ON DELETE CASCADE,
            FOREIGN KEY (employee_id) REFERENCES Employees(employee_id) ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """)

        print("Vytvářím pohledy (Views)...")

        cursor.execute("""
        CREATE VIEW View_Employee_Details AS
        SELECT e.employee_id, e.name, e.position, e.salary, d.name as department_name
        FROM Employees e
        LEFT JOIN Departments d ON e.department_id = d.department_id
        """)

        cursor.execute("""
        CREATE VIEW View_Active_Projects AS
        SELECT p.name, p.end_date, COUNT(pa.employee_id) as team_size
        FROM Projects p
        LEFT JOIN Project_Assignments pa ON p.project_id = pa.project_id
        WHERE p.status = 'running'
        GROUP BY p.project_id
        """)

        conn.commit()
        print("Struktura databáze vytvořena.")

        # Import dat z CSV
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(base_dir, 'data.csv')

        if os.path.exists(csv_path):
            print(f"Načítám data z: {csv_path}")
            with open(csv_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if 'department_name' in row:
                        cursor.execute("INSERT INTO Departments (name, budget, establishment_date) VALUES (%s, %s, %s)", 
                                       (row['department_name'], row.get('budget', 0), '2023-01-01'))
                    
                    if 'employee_name' in row:
                        cursor.execute("SELECT department_id FROM Departments LIMIT 1")
                        dept_res = cursor.fetchone()
                        dept_id = dept_res[0] if dept_res else None

                        cursor.execute("INSERT INTO Employees (name, position, salary, department_id, is_manager) VALUES (%s, %s, %s, %s, %s)",
                                       (row['employee_name'], row['position'], row['salary'], dept_id, 0))
                
                conn.commit()
                print("Data importována.")
        else:
            print("VAROVÁNÍ: data.csv nenalezen, vkládám testovací data.")
            cursor.execute("INSERT INTO Departments (name, budget, establishment_date) VALUES ('IT', 100000.0, '2020-01-01')")
            conn.commit()

    except Error as err:
        print(f"CHYBA MySQL: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    create_tables_and_import()