import customtkinter as tk
from recallr.frames import FrameManager, Frames
from recallr.components import Components
from recallr.objects import Account

def setup_screen(screen_type="menu"):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            # create the default main frame for this screen and pass its
            # Components wrapper into the screen method as `component`.
            component = self.screen_manager.create_frame(relx=0.75, rely=0.5, anchor="center")

            # Call the decorated screen method
            func(self, component, *args, **kwargs)

            # Adds the frame to the screen
            # create_frame already registers the frame with screen_manager.frames
            # so nothing else to do here.
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

    def create_frame(self, relx=None, rely=0.5, anchor="center", place_kwargs=None):
        frame_manager = FrameManager(self)

        if place_kwargs is None:
            place_kwargs = {}
        if relx is not None:
            frame = Frames(frame_manager)

            name = "centred"
            func = getattr(frame, name, None)

            func()

        self.frames.append(frame_manager)
        return Components(self, frame_manager)
    
    def show_screen(self, function_name):
        # Clear any primary-button reference stored in the toplevel
        try:
            root = self.winfo_toplevel()
            if hasattr(root, '_primary_button'):
                try:
                    root._primary_button = None
                except Exception:
                    try:
                        delattr(root, '_primary_button')
                    except Exception:
                        pass
        except Exception:
            pass

        # Clears any content from the previous screen
        for frame in self.frames:
            frame.destroy()
        self.frames.clear() 
        
        frame_manager = FrameManager(self)

        screens = Screens(frame_manager)
        # Checking to see if the function is apart of the Screens class
        func = getattr(screens, function_name, None)
        if callable(func):
            func()
        else:
            raise NameError(f"Function '{function_name}' is not a valid subroutine for the '{screens.__class__.__name__}' class.")

        # If func is apart of the Screens class, loads the components
        for frame in self.frames:
            frame.load_components()

            print(f"🎞️ '{frame}' frame has been loaded.")
        
        print(f"🔲 '{function_name}' screen has been loaded.")
        print("-"*30)

class Screens:
    def __init__(self, frame_manager):
        self.screen_manager = frame_manager.master
        self.frame_manager = frame_manager

    @setup_screen(screen_type="menu")
    def login(self, component):
        component.default.title(text="Recallr")
        component.default.content(text="Please fill in your login details!")
        component.default.entry_field(placeholder_text="Username")
        component.custom.password_entry_field()
        component.default.button(text="Login", button_type="primary")
        component.default.button(text="Create account", button_type="grey", component_id="create_account_menu")

    @setup_screen(screen_type="menu")
    def create_account(self, component):
        component.default.title(text="Create Account")
        component.default.content(text="Please fill in the following details!")
        component.default.entry_field(placeholder_text="What is your name?", component_id="display_name")
        component.default.entry_field(placeholder_text="New Username")
        component.custom.password_entry_field(placeholder_text="New Password")
        component.custom.password_entry_field(placeholder_text="Confirm Password")
        component.default.button(text="Create account", button_type="primary", button_style="green", component_id="make_the_account")
        component.default.button(text="Cancel", button_type="red", component_id="cancel_create_account")

    @setup_screen(screen_type="menu")
    def main_menu(self, component):
        account = Account()
        component.default.title(text="Recallr")
        component.default.content(text=f"Hello, {account.display_name}!")
        component.default.button(text="Notes")
        component.default.button(text="Test yourself", component_id="quiz_menu")
        component.default.button(text="Settings", button_type="grey", component_id="coming_soon")
        component.custom.sign_out_button()

    @setup_screen(screen_type="menu")
    def quiz_menu(self, component):
        component.default.title(text="Quiz Menu")
        component.default.content(text="Please pick which mode you would like to do!")
        component.default.button(text="Flashcards", component_id="coming_soon")
        component.default.button(text="Multiple choice", component_id="coming_soon")
        component.default.button(text="Blurting", component_id="coming_soon")
        component.custom.main_menu_button()

    @setup_screen(screen_type="menu")
    def notes(self, component):
        component.default.title(text="Notes")
        component.default.content(text="Here are your notes!")
        component.custom.main_menu_button()

        sidebar = self.screen_manager.create_frame(relx=0.75, rely=0.5, anchor="center")
        sidebar.default.button(text="Useless button")

    @setup_screen(screen_type="menu")
    def coming_soon(self, component):
        component.default.title(text="Recallr")
        component.default.content(text="Coming Soon!")
        component.custom.main_menu_button()
        component.custom.sign_out_button()