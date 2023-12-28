import os
import sqlite3


class DBManager:
    def __init__(self, database_path=os.path.join(os.getcwd(), 'database\mouse_data.db')):
        self.database_path = database_path
        self.con = None
        self.cursor = None

    def connect(self):
        if not os.path.exists(self.database_path):
            print(f"Creating SQLite file at: {self.database_path}")
            open(self.database_path, 'a').close()
        self.con = sqlite3.connect(self.database_path)
        self.cursor = self.con.cursor()

    def close(self):
        if self.con:
            self.con.close()

    def setup(self):
        self.connect()

        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS mouse_data(
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            coordinates TEXT UNIQUE, 
                            image BLOB NOT NULL)
                            ''')
        self.con.commit()

    def insert_query(self, coordinates: tuple, image: bytes):
        coordinates_str = str(coordinates)
        try:
            self.cursor.execute('''
                                INSERT INTO mouse_data (coordinates, image) 
                                VALUES (?, ?)''', (coordinates_str, image))
            self.con.commit()
            print("Successfully inserted the data.")
        except sqlite3.Error as e:
            print(f"Error inserting into database: {e}")
