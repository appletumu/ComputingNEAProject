import sqlite3
import json

class DatabaseManager:
    def __init__(self):
        pass

    def startup(self):
        try:
            self.connection = sqlite3.connect("recallr.db")
            self.cursor = self.connection.cursor()

            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                username TEXT PRIMARY KEY,
                display_name TEXT,
                password TEXT NOT NULL
            )
            """)

            self.connection.commit()
        except sqlite3.Error as e:
            raise e
        finally:
            self.cursor.close()
            self.connection.close()
    
    def query(self, query, params=()):
        try:
            self.connection = sqlite3.connect("recallr.db")
            self.cursor = self.connection.cursor()

            self.cursor.execute(query, params)
            results = self.cursor.fetchall()

            self.connection.commit()
        except sqlite3.Error as e:
            raise e
        finally:
            self.cursor.close()
            self.connection.close()

        return results

class JsonManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self):
        try: 
            with open(self.file_path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}
        except json.JSONDecodeError:
            data = {}

        return data
    
    def read_json(self, key):
        data = self.read_file()
        return data[key] if key in data else None

    def write_json(self, updates, section=None):
        data = self.read_file()

        if section == None:
            data.update(updates)
        else:
            if section not in data or not isinstance(data[section], dict):
                data[section] = {}
            data[section].update(updates)

        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)