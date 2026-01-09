from mysql.connector import Error

class ProjectGateway:
    def __init__(self, db):
        self.db = db

    def fetch_all(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT project_id, name, start_date, end_date FROM Projects")
        results = cursor.fetchall()
        conn.close()
        return results

    def insert(self, name, start_date, end_date):
        conn = self.db.connect()
        try:
            cursor = conn.cursor()
            query = "INSERT INTO Projects (name, start_date, end_date, status) VALUES (%s, %s, %s, 'planned')"
            cursor.execute(query, (name, start_date, end_date))
            conn.commit()
        except Error as e:
            raise e
        finally:
            conn.close()

    def update(self, project_id, name, start_date, end_date):
        conn = self.db.connect()
        try:
            cursor = conn.cursor()
            query = "UPDATE Projects SET name=%s, start_date=%s, end_date=%s WHERE project_id=%s"
            cursor.execute(query, (name, start_date, end_date, project_id))
            conn.commit()
        except Error as e:
            raise e
        finally:
            conn.close()

    def delete(self, project_id):
        conn = self.db.connect()
        try:
            cursor = conn.cursor()
            query = "DELETE FROM Projects WHERE project_id=%s"
            cursor.execute(query, (project_id,))
            conn.commit()
        except Error as e:
            raise e
        finally:
            conn.close()

    def create_project_with_manager(self, name, start_date, end_date, manager_id):
        conn = self.db.connect()
        try:
            conn.start_transaction()
            cursor = conn.cursor()
            
            query_proj = "INSERT INTO Projects (name, start_date, end_date, status) VALUES (%s, %s, %s, 'planned')"
            cursor.execute(query_proj, (name, start_date, end_date))
            new_project_id = cursor.lastrowid

            query_assign = "INSERT INTO Project_Assignments (project_id, employee_id, role) VALUES (%s, %s, 'Manager')"
            cursor.execute(query_assign, (new_project_id, manager_id))

            conn.commit()
            return new_project_id
        except Error as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def fetch_active_projects_stats(self):
        conn = self.db.connect()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM View_Active_Projects")
            results = cursor.fetchall()
            return results
        except Error as e:
            print(e)
            return []
        finally:
            conn.close()