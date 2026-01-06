import sqlite3

class DatabaseConnection:
    def __init__(self, db_file):
        self.db_file = db_file

    def connect(self):
        return sqlite3.connect(self.db_file)

    def init_db(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Employees (
                employee_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                position TEXT NOT NULL,
                salary REAL NOT NULL CHECK (salary >= 0),  
                is_manager BOOLEAN NOT NULL DEFAULT 0  
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Departments (
                department_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                budget REAL NOT NULL CHECK (budget >= 0)
                establishment_date DATETIME NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Projects (
                project_id INTEGER PRIMARY KEY,
                name TEXT,
                start_date DATETIME,
                end_date DATETIME
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS EmployeeProjects (
                employee_id INTEGER,
                project_id INTEGER,
                FOREIGN KEY (employee_id) REFERENCES Employees(employee_id),
                FOREIGN KEY (project_id) REFERENCES Projects(project_id),
                PRIMARY KEY (employee_id, project_id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Documents (
                document_id INTEGER PRIMARY KEY,
                title TEXT,
                content TEXT,
                creation_date DATETIME
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS DocumentDepartments (
                document_id INTEGER,
                department_id INTEGER,
                FOREIGN KEY (document_id) REFERENCES Documents(document_id),
                FOREIGN KEY (department_id) REFERENCES Departments(department_id),
                PRIMARY KEY (document_id, department_id)
            )
        ''')

        conn.commit()
        conn.close()
