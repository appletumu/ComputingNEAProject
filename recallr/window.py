import customtkinter as tk
from recallr.screens import Screens

class WindowManager(tk.CTk):
    def __init__(self, title):
        super().__init__()

        self.title(title)
        self.geometry("800x600")
        self.minsize(1336, 768)
        tk.set_appearance_mode("light") 

    def startup(self):
        print("WindowManager is starting up...")

        screen_manager = ScreenManager(self)
        screen_manager.show_screen("login_screen")

        print("WindowManager sucessfully started up.")
        self.mainloop()
        print("WindowManager loop has been broken.")

class ScreenManager(tk.CTkFrame):
    def __init__(self, window_manager, **kwargs):
        super().__init__(window_manager, **kwargs)

        self.window_manager = window_manager
        self.frames = []

        self.configure(fg_color="transparent")
        self.pack(fill="both", expand=True)
    
    def show_screen(self, function_name):
        screens = Screens(self)
        func = getattr(screens, function_name, None)
        if callable(func):
            func()
        else:
            raise NameError(f"Function '{function_name}' is not a valid subroutine for the '{screens.__class__.__name__}' class.")

        for frame in self.frames:
            frame.load_components()

            print(f"'{frame}' frame has been loaded.")