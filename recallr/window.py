import customtkinter as tk
from recallr.screens import ScreenManager
from recallr.components import Components
from recallr.backend import DatabaseManager, JsonManager

class WindowManager(tk.CTk):
    def __init__(self, title):
        super().__init__()

        # Sets up the main window
        self.title(title)
        self.geometry("800x600")
        self.minsize(1336, 768)
        tk.set_appearance_mode("light")

        self.screens = []

    def startup(self):
        print("🪟 WindowManager is starting up...")
        print("-"*30)

        screen_manager = ScreenManager(self)
        db_manager = DatabaseManager()

        db_manager.startup()

        # Check to see if the user is logged in
        json_manager = JsonManager("settings/app_settings.json")
        account = json_manager.read_json("account")
        try:
            stored_username = db_manager.query("SELECT username FROM accounts WHERE username = ?", (account['username'],))[0][0]
        except IndexError:
            stored_username = None

        # Displays the seleccted screen
        if account['username'] == stored_username and account['username'] != None:
            screen_manager.show_screen("main_menu")
        elif account['username'] != stored_username and account['username'] != None:
            screen_manager.show_screen("login")

            component = Components(screen_manager, None)
            component.default.message_box(message_box_type="error", message="Your account details have changed. Please log in again.")
        else:
            screen_manager.show_screen("login")

        print("🪟 WindowManager sucessfully started up.")
        print("-"*30)

        # Forces the window to be at the very top
        self.focus_force()

        self.mainloop()
        print("🪟 WindowManager loop has been broken.")
    