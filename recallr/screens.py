import customtkinter as tk
from recallr.frames import FrameManager
from recallr.components import Components

def setup_screen(screen_type="menu"):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            component = Components(self.screen_manager, self.frame_manager)

            # Call the decorated screen method
            func(self, component, *args, **kwargs)

            self.screen_manager.frames.append(self.frame_manager)
        return wrapper
    return decorator

class ScreenManager(tk.CTkFrame):
    def __init__(self, window_manager, **kwargs):
        super().__init__(window_manager, **kwargs)

        # Sets up the screen
        self.configure(fg_color="transparent")
        self.pack(fill="both", expand=True)

        self.window_manager = window_manager

        self.frames = []
    
    def show_screen(self, function_name):
        # Clears any content from the previous screen
        for frame in self.frames:
            frame.destroy()
        self.frames.clear() 
        
        frame_manager = FrameManager(self)

        screens = Screens(frame_manager)
        func = getattr(screens, function_name, None)
        if callable(func):
            func()
        else:
            raise NameError(f"Function '{function_name}' is not a valid subroutine for the '{screens.__class__.__name__}' class.")

        for frame in self.frames:
            frame.load_components()

            print(f"'{frame}' frame has been loaded.")

class Screens:
    def __init__(self, frame_manager):
        self.screen_manager = frame_manager.master
        self.frame_manager = frame_manager

    @setup_screen(screen_type="menu")
    def login(self, component):
        component.default.title(text="Recallr")
        component.default.content(text="Please fill in your login details!")
        component.default.entry_field(placeholder_text="Username")
        component.default.entry_field(placeholder_text="Password")
        component.default.button(text="Login")
        component.default.button(text="Create account", button_type="grey")

    @setup_screen(screen_type="menu")
    def create_account(self, component):
        component.default.title(text="Create Account")
        component.default.content(text="Please fill in the following details!")
        component.default.entry_field(placeholder_text="New Username")
        component.default.entry_field(placeholder_text="New Password")
        component.default.entry_field(placeholder_text="Confirm Password")
        component.default.button(text="Create account")
        component.default.button(text="Cancel", button_type="red")

    @setup_screen(screen_type="menu")
    def main_menu(self, component):
        component.default.title(text="Recallr")
        component.default.content(text="Hello, {username}!")
        component.default.button(text="Notes")
        component.default.button(text="Test yourself")
        component.default.button(text="Settings", button_type="grey")
        component.custom.sign_out_button()

    @setup_screen(screen_type="menu")
    def coming_soon(self, component):
        component.default.title(text="Recallr")
        component.default.content(text="Coming Soon!")
        component.default.button(text="Main menu", button_type="grey")
        component.custom.sign_out_button()