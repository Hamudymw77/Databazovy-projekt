from mysql.connector import Error

class EmployeeGateway:
    def __init__(self, db):
        self.db = db

    def fetch_all(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT employee_id, name, position, salary, is_manager FROM Employees")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def insert(self, name, position, salary, is_manager):
        conn = self.db.connect()
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO Employees (name, position, salary, is_manager) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (name, position, salary, is_manager))
            conn.commit()
            conn.close()
        except Error as e:
            print(e)
            raise e

    def update(self, employee_id, name, position, salary, is_manager):
        conn = self.db.connect()
        try:
            cursor = conn.cursor()
            sql = "UPDATE Employees SET name=%s, position=%s, salary=%s, is_manager=%s WHERE employee_id=%s"
            cursor.execute(sql, (name, position, salary, is_manager, employee_id))
            conn.commit()
            conn.close()
        except Error as e:
            print(e)
            raise e

    def delete(self, employee_id):
        conn = self.db.connect()
        try:
            cursor = conn.cursor()
            sql = "DELETE FROM Employees WHERE employee_id=%s"
            cursor.execute(sql, (employee_id,))
            conn.commit()
            conn.close()
        except Error as e:
            print(e)
            raise e