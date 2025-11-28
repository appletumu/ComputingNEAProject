import sqlite3
from recallr.backend import JsonManager, DatabaseManager
import re
import customtkinter as tk

class AppSettings:
    def __init__(self):
        json_manager = JsonManager("settings/app_settings.json")

        self.app_name = json_manager.read_json('appName')
        self.font = json_manager.read_json('font')
        self.text_sizes = json_manager.read_json('textSizes')
        self.component_configs = json_manager.read_json("componentConfigs")
        self.colors = json_manager.read_json("colors")
        self.blurting_recall_time_limit = json_manager.read_json("blurtingRecallNotesTimeLimit")

class UserSettings:
    def __init__(self):
        json_manager = JsonManager("settings/user_settings.json")

        self.db_manager = DatabaseManager()

        self.data = json_manager.read_file()  # returns a dict
        self.list = [{k: v} for k, v in self.data.items()]
    
    def get_current_setting_value(self, setting_id):
        setting = self.get_setting_data(setting_id)

        # Gets current setting value from database
        db_setting_value = self.get_user_setting_db_value(setting_id)

        if db_setting_value != None:
            current_setting_value = db_setting_value
        else:
            # Sets to default value if no value is found
            current_setting_value = setting['defaultValue']
        
        return current_setting_value

    def get_user_setting_db_value(self, setting_id):
        account = Account()
        result = self.db_manager.query(
            "SELECT settings_value FROM user_settings WHERE owner_username = ? AND setting_id = ?",
            (account.username, setting_id)
        )
        if result:
            return result[0][0]
        return None

    def get_setting_data(self, setting_id):
        for setting in self.list:
            if setting_id in setting:
                return setting[setting_id]
        return None
    
    def change_setting(self, setting_id, new_value):
        account = Account()
        # Either inserts a new setting or updates an existing one
        try:
            self.db_manager.query(
                """
                INSERT INTO user_settings (owner_username, setting_id, settings_value)
                VALUES (?, ?, ?)
                """,
                (account.username, setting_id, new_value)
            )
        except sqlite3.IntegrityError:
            # If the setting already exists, update it instead
            self.db_manager.query("""
                UPDATE user_settings 
                SET settings_value = ?
                WHERE owner_username = ? AND setting_id = ?
                """,
                (new_value, account.username, setting_id)
            )

    def reset_setting(self, setting_id):
        account = Account()
        self.db_manager.query(
            "DELETE FROM user_settings WHERE owner_username = ? AND setting_id = ?",
            (account.username, setting_id)
        )

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
            return {"success": False, "message": "Invalid login details"}

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

            # Only successful after the account info had been saved in the database / config
            return {"success": True, "message": ""}
        else:
            return {"success": False, "message": "Invalid login details"}
        

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
            return {"success": False, "message": "Passwords do not match"}
        elif not display_name or not new_username or not new_password:
            return {"success": False, "message": "None of the fields can be empty"}
        elif new_username in accounts:
            return {"success": False, "message": "Username already exists. Please choose a different one"}
        

        # Checks that the username is in lower case, only has letters/numbers, and no spaces
        # Examples of valid usernames: "testing_account", "123_yes", "okay_that_is_cool", "yesman_2"
        def is_valid_string(s: str) -> bool:
            return bool(re.fullmatch(r"[a-z0-9_]+", s))
        if is_valid_string(new_username) == False:
            return {"success": False, "message": "That is not a valid username. Must only have lowercases letters/numbers with underscores for spaces.\n\nExamples: 'username_123', 'valid_username'"}
        
        try:
            # successfully created an account
            self.db_manager.query("INSERT INTO accounts (username, display_name, password) VALUES (?, ?, ?)", (new_username, display_name, new_password))
            return {"success": True, "message": f"Succesfully created an account for '{new_username}'. Please log in again"}
        except sqlite3.IntegrityError:
            return {"success": False, "message": "This username is already taken"}
    
    def delete_account(self):
        self.db_manager.query("DELETE FROM accounts WHERE username = ?", (self.username,))

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
        self.json_manager = JsonManager("settings/app_settings.json")

    def create_note(self):
        account = Account()

        placeholder_text = self.json_manager.read_json('createNotePlaceholdertext')

        DatabaseManager().query(
            "INSERT INTO notes (owner_username, title, content) VALUES (?, ?, ?)",
            (account.username, placeholder_text['title'],  placeholder_text['content'])
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

    def get_notes(self, note_ids=[]):
        """
        Always returns a list.
        If note_ids is EMPTY, returns ALL user notes.
        If note_ids has items, returns the specific notes.
        If it can't find anything, returns an empty list.
        """
        
        notes_db_dump = self.db_manager.query("SELECT note_id, title, content FROM notes WHERE owner_username = ?", (Account().username,))

        notes = []

        for note in notes_db_dump:
            note_id, note_title, note_content = note

            if note_ids == [] or note_id in note_ids:
                notes.append({"id": note_id, "title": note_title, "content": note_content})

        return notes
    
    def save_note(self, note_id, note_title, note_content):
        account = Account()
        
        self.db_manager.query(
            "UPDATE notes SET title = ?, content = ? WHERE note_id = ? AND owner_username = ?",
            (note_title, note_content, note_id, account.username)
        )

        return True

    def get_note_ids(self):
         return self.db_manager.query("SELECT note_id FROM notes WHERE owner_username = ?", (Account().username,))

    def make_preview(self, text, max_chars=18):
        # Collapse newlines and repeated spaces for both title and content
        s = ' '.join(str(text).split())
        if len(s) > max_chars:
            return s[:max_chars].rstrip() + '...'
        return s
    
    def get_note_data_from_components(self, component, frame_manager):
        # Gets the note ID from the component ID
        note_id = component.component_id.split("_")[-1]

        title_component = frame_manager.find_component(f"notes_title_textbox_{note_id}")
        content_component = frame_manager.find_component(f"notes_content_textbox_{note_id}")

        note_title = title_component.get("0.0", "end").strip()
        note_content = content_component.get("0.0", "end").strip()

        return {"id": note_id, "title": note_title, "content": note_content}
    
    def select_notes_blurt(self, frame_manager, previous_selected_notes):
        notes_selected = []
        notes_not_selected = []
        for frame_component in frame_manager.components:
            if isinstance(frame_component, tk.CTkCheckBox) == False:
                continue

            # Skips the checkbox if it is disabled
            if frame_component.cget("state") == tk.DISABLED:
                continue
            
            # Checks if the CheckBox is checked, if so adds it to the list
            note_id = int(frame_component.component_id.split("_")[-1])
            if frame_component.get():
                notes_selected.append(note_id)
            else:
                notes_not_selected.append(note_id)

        # Combines notes_selected with previous_selected_notes (without having duplicates)
        for note_id in notes_selected:
            if note_id not in previous_selected_notes:
                previous_selected_notes.append(note_id)
        
        # Removes any unselected ntoes
        for note_id in notes_not_selected:
            if note_id in previous_selected_notes:
                previous_selected_notes.remove(note_id)
        
        return previous_selected_notes