from mysql.connector import Error

class DepartmentGateway:
    def __init__(self, db):
        self.db = db

    def fetch_all(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        # V MySQL používáme %s místo ?
        cursor.execute("SELECT department_id, name, budget, establishment_date FROM Departments")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def insert(self, name, budget, establishment_date):
        conn = self.db.connect()
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO Departments (name, budget, establishment_date) VALUES (%s, %s, %s)"
            cursor.execute(sql, (name, budget, establishment_date))
            conn.commit()
            conn.close()
        except Error as e:
            print(e)
            raise e

    def update(self, dep_id, name, budget, establishment_date):
        conn = self.db.connect()
        try:
            cursor = conn.cursor()
            sql = "UPDATE Departments SET name=%s, budget=%s, establishment_date=%s WHERE department_id=%s"
            cursor.execute(sql, (name, budget, establishment_date, dep_id))
            conn.commit()
            conn.close()
        except Error as e:
            print(e)
            raise e

    def delete(self, dep_id):
        conn = self.db.connect()
        try:
            cursor = conn.cursor()
            sql = "DELETE FROM Departments WHERE department_id=%s"
            cursor.execute(sql, (dep_id,))
            conn.commit()
            conn.close()
        except Error as e:
            print(e)
            raise e