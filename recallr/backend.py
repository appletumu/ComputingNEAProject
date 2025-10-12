import sqlite3

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