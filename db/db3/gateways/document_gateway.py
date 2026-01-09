from mysql.connector import Error
import datetime

class DocumentGateway:
    def __init__(self, db):
        self.db = db

    def create_document_with_transaction(self, title, content, department_ids):
        conn = self.db.connect()
        try:
            cursor = conn.cursor()
            
            creation_date = datetime.datetime.now()
            sql_doc = "INSERT INTO Documents (title, content, creation_date) VALUES (%s, %s, %s)"
            cursor.execute(sql_doc, (title, content, creation_date))
            
            new_document_id = cursor.lastrowid
            
            sql_link = "INSERT INTO DocumentDepartments (document_id, department_id) VALUES (%s, %s)"
            for dep_id in department_ids:
                cursor.execute(sql_link, (new_document_id, dep_id))
            
            conn.commit()
            print("Transakce úspěšná.")
            
        except Error as e:
            conn.rollback()
            print(f"Chyba transakce: {e}")
            raise e
        finally:
            conn.close()