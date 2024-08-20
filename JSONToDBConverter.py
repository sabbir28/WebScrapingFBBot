import json
import sqlite3
from datetime import datetime

class JSONToDBConverter:
    def __init__(self, json_file, db_file):
        self.json_file = json_file
        self.db_file = db_file

    def convert_date_format(self, date_str):
        """Converts date from 'dd mmm yyyy' to 'dd/mm/yyyy'."""
        return datetime.strptime(date_str, '%d %b %Y').strftime('%d/%m/%Y')

    def read_json(self):
        """Reads JSON data from the file."""
        with open(self.json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def create_db(self):
        """Creates a SQLite database and a table."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                last_updated TEXT,
                download_link TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def insert_data(self, data):
        """Inserts data into the SQLite table."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        for item in data:
            cursor.execute('''
                INSERT INTO notifications (title, last_updated, download_link)
                VALUES (?, ?, ?)
            ''', (item['title'], item['last_updated'], item['download_link']))

        conn.commit()
        conn.close()

    def convert_and_save(self):
        """Main method to convert JSON data and save it into a .db file."""
        data = self.read_json()
        
        # Convert date formats
        for item in data:
            item['last_updated'] = self.convert_date_format(item['last_updated'])
        
        self.create_db()
        self.insert_data(data)

# Usage
if __name__ == "__main__":
    converter = JSONToDBConverter('data.json', 'data.db')
    converter.convert_and_save()
