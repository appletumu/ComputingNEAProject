import customtkinter as tk
from recallr.screens import ScreenManager
from recallr.backend import DatabaseManager

class WindowManager(tk.CTk):
    def __init__(self, title):
        super().__init__()

        # Sets up the main window
        self.title(title)
        self.geometry("800x600")
        self.minsize(1336, 768)
        tk.set_appearance_mode("light")

        self.screens = []

    def startup(self, show_screen):
        print("WindowManager is starting up...")

        screen_manager = ScreenManager(self)

        # Displays the seleccted screen
        screen_manager.show_screen(show_screen)

        db_manager = DatabaseManager()
        db_manager.startup()

        print("WindowManager sucessfully started up.")
        self.focus_force()
        self.mainloop()
        print("WindowManager loop has been broken.")
    