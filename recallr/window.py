import customtkinter as tk
from recallr.screens import ScreenManager

class WindowManager(tk.CTk):
    def __init__(self, title):
        super().__init__()

        self.title(title)
        self.geometry("800x600")
        self.minsize(1336, 768)
        tk.set_appearance_mode("light")

        self.screens = []

    def startup(self, show_screen):
        print("WindowManager is starting up...")

        screen_manager = ScreenManager(self)

        screen_manager.show_screen(show_screen)

        print("WindowManager sucessfully started up.")
        self.mainloop()
        print("WindowManager loop has been broken.")