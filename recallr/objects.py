import sqlite3
from recallr.backend import JsonManager, DatabaseManager

class AppSettings:
    def __init__(self):
        json_manager = JsonManager("settings/app_settings.json")

        self.app_name = json_manager.read_json('appName')
        self.font = json_manager.read_json('font')
        self.text_sizes = json_manager.read_json('textSizes')
        self.component_configs = json_manager.read_json("componentConfigs")
        self.colors = json_manager.read_json("colors")
class Account:
    def __init__(self):
        json_manager = JsonManager("settings/app_settings.json")
        account = json_manager.read_json("account") 

        self.db_manager = DatabaseManager()

        self.display_name = account.get('displayName')
        self.username = account.get('username')

    def login(self, username, password):
        accounts = self.db_manager.query("SELECT username FROM accounts")
        accounts = [account[0] for account in accounts]  # Unpack tuples to get a list of usernames

        if username in accounts:
            stored_password = self.db_manager.query("SELECT password FROM accounts WHERE username = ?", (username,))[0][0]
        else:
            return {"sucess": False, "message": "Invalid login details"}

        if password == stored_password:
            # Adds user account to the settings file
            display_name = self.db_manager.query("SELECT display_name FROM accounts WHERE username = ?", (username,))[0][0]

            json_manager = JsonManager("settings/app_settings.json")
            json_manager.write_json({
                'account': {
                    'username': username,
                    'displayName': display_name
                }
            })

            # Only sucessful after the account info had been saved in the database / config
            return {"sucess": True, "message": ""}
        else:
            return {"sucess": False, "message": "Invalid login details"}
        

    def sign_out(self):
        json_manager = JsonManager("settings/app_settings.json")
        json_manager.write_json({
            'account': {
                'username': None,
                'displayName': None
            }
        })

    def create_account(self, display_name, new_username, new_password, confirm_password=None):
        accounts = self.db_manager.query("SELECT username FROM accounts")

        if confirm_password != None and new_password != confirm_password:
            return {"sucess": False, "message": "Passwords do not match"}
        elif not display_name or not new_username or not new_password:
            return {"sucess": False, "message": "None of the fields can be empty"}
        elif new_username in accounts:
            return {"sucess": False, "message": "Username already exists. Please choose a different one"}
        
        try:
            # Sucessfully created an account
            self.db_manager.query("INSERT INTO accounts (username, display_name, password) VALUES (?, ?, ?)", (new_username, display_name, new_password))
            return {"sucess": True, "message": f"Succesfully created an account for '{new_username}'. Please log in again"}
        except sqlite3.IntegrityError:
            return {"sucess": False, "message": "This username is already taken"}
    
    def delete_account(self):
        db_manager = DatabaseManager()
        db_manager.execute("DELETE FROM accounts WHERE username = ?", (self.username,))

        json_manager = JsonManager("settings/app_settings.json")
        json_manager.write_json({
            'account': {
                'username': None,
                'displayName': None
            }
        })

class Notes:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def create_note(self):
        account = Account()

        DatabaseManager().query(
            "INSERT INTO notes (owner_username, title, content) VALUES (?, ?, ?)",
            (account.username, "New Note", "- This is a new note!\n- You can write your content here.\n- Test your knowledge by using the Blurting feature.")
        )

        get_note_id = DatabaseManager().query(
            "SELECT MAX(note_id) FROM notes WHERE owner_username = ?",
            (account.username,)
        )

        return get_note_id[0][0]

    def delete_note(self, note_id):
        account = Account()

        note = DatabaseManager().query(
            "SELECT title, content FROM notes WHERE note_id = ? AND owner_username = ?",
            (note_id, account.username)
        )

        note_information = {
            "id": note_id,
            "title": note[0][0],
            "content": note[0][1]
        }

        DatabaseManager().query(
            "DELETE FROM notes WHERE note_id = ? AND owner_username = ?",
            (note_id, account.username)
        )

        return note_information

        def get_notes(note_ids=[]):
            """
            Always returns a list.
            If note_ids is EMPTY, returns ALL user notes.
            If note_ids has items, returns the specific notes.
            If it cant find anything, returns an empty list.
            """
            return

    def get_note_ids(self):
         return self.db_manager.query("SELECT note_id FROM notes WHERE owner_username = ?", (Account().username,))
