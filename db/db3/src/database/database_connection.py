import mysql.connector
from mysql.connector import Error
import configparser
import os

class DatabaseConnection:
    def __init__(self, db_file=None):
        self.config = configparser.ConfigParser()
        
        base_path = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_path, '..', 'settings', 'config.ini')
        
        self.config.read(config_path)

    def connect(self):
        """Vytvoří a vrátí připojení k MySQL databázi."""
        connection = None
        try:
            if 'Database' not in self.config:
                 print("CHYBA: V config.ini chybí sekce [Database]!")
                 return None

            db_config = self.config['Database']
            
            connection = mysql.connector.connect(
                host=db_config.get('host', 'localhost'),
                user=db_config.get('user', 'root'),
                password=db_config.get('password', ''),
                database=db_config.get('database', 'employee_management_db')
            )
        except Error as e:
            print(f"Chyba při připojování k MySQL: {e}")
            raise e

        return connection