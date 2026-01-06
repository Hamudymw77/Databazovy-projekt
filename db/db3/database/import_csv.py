import csv
import sqlite3


def import_csv_to_table(db_path, csv_file_path, table_name):

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open(csv_file_path, 'r') as file:

        reader = csv.DictReader(file)


        for row in reader:
            placeholders = ', '.join(['?'] * len(row))
            columns = ', '.join(row.keys())
            sql = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'


            cursor.execute(sql, list(row.values()))

    conn.commit()
    conn.close()
