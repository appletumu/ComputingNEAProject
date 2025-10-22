import customtkinter as tk
from recallr.frames import FrameManager, Frames
from recallr.components import Components
from recallr.objects import Account, AppSettings
from recallr.backend import DatabaseManager

def setup_screen(screen_type="menu"):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            # Call the decorated screen method
            func(self, *args, **kwargs)
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

    def create_frame(self, frame_name="centred"):
        frame_manager = FrameManager(self)

        frame = Frames(frame_manager)

        func = getattr(frame, frame_name, None)

        # Runs the code within the Frames class
        func()

        self.frames.append(frame_manager)
        return Components(self, frame_manager)
    
    def show_screen(self, function_name, **kwargs):
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
            func(**kwargs)
        else:
            raise NameError(f"Function '{function_name}' is not a valid subroutine for the '{screens.__class__.__name__}' class.")

        print("-"*30)
        # If func is apart of the Screens class, loads the components
        for frame in self.frames:
            frame.load_components()

            print(f"🎞️ '{frame}' frame has been loaded.")
        
        print(f"🔲 '{function_name}' screen has been loaded.")

class Screens:
    def __init__(self, frame_manager):
        self.screen_manager = frame_manager.master
        self.frame_manager = frame_manager

    @setup_screen(screen_type="menu")
    def login(self):
        main = self.screen_manager.create_frame()
        main.default.title()
        main.default.content(text="Please fill in your login details!")
        main.default.entry_field(placeholder_text="Username")
        main.custom.password_entry_field()
        main.default.button(text="Login", button_type="primary")
        main.default.button(text="Create account", button_type="grey", component_id="create_account_menu")

    @setup_screen(screen_type="menu")
    def create_account(self):
        main = self.screen_manager.create_frame() 
        main.default.title(text="Create Account")
        main.default.content(text="Please fill in the following details!")
        main.default.entry_field(placeholder_text="What is your name?", component_id="display_name")
        main.default.entry_field(placeholder_text="New Username")
        main.custom.password_entry_field(placeholder_text="New Password")
        main.custom.password_entry_field(placeholder_text="Confirm Password")
        main.default.button(text="Create account", button_type="primary", button_style="green", component_id="make_the_account")
        main.default.button(text="Cancel", button_type="red", component_id="cancel_create_account")

    @setup_screen(screen_type="menu")
    def main_menu(self):
        account = Account()

        main = self.screen_manager.create_frame()
        main.default.title()
        main.default.content(text=f"Hello, {account.display_name}!")
        main.default.button(text="Notes")
        main.default.button(text="Test yourself", component_id="quiz_menu")
        main.default.button(text="Settings", button_type="grey", component_id="coming_soon")
        main.custom.sign_out_button()

    @setup_screen(screen_type="menu")
    def quiz_menu(self):
        main = self.screen_manager.create_frame()
        main.default.title(text="Quiz Menu")
        main.default.content(text="Please pick which mode you would like to do!")
        main.default.button(text="Flashcards", component_id="coming_soon")
        main.default.button(text="Multiple choice", component_id="coming_soon")
        main.default.button(text="Blurting", component_id="coming_soon")
        main.custom.main_menu_button()

    @setup_screen(screen_type="menu")
    def notes(self, **kwargs):
        view_note_id = kwargs.get("view_note_id", None)
        main = self.screen_manager.create_frame()

        # Checks if a note is being viewed
        if view_note_id == None:
            main.default.title()
            main.default.content(text="Select a note from the sidebar!")
            main.custom.main_menu_button()
        else:
            main.custom.view_note_textbox(note_id=view_note_id)

        database_manager = DatabaseManager()

        sidebar = self.screen_manager.create_frame("sidebar")
        all_notes = database_manager.query("SELECT note_id FROM notes WHERE owner_username = ?", (Account().username,))

        # Checks if a note is being viewed
        selected_note_id = None
        if view_note_id != None:
            selected_note_id = int(view_note_id)

        for note in all_notes:
            note_id = note[0]

            # If the button is selected, then it greys it out
            button_state = "normal"
            if note_id == selected_note_id:
                button_state = "disabled"

            sidebar.custom.view_note_button(note_id=note_id, component_id=f"view_note_{note_id}", command="view_note", state=button_state)
        sidebar.default.button(text="Create note")

    @setup_screen(screen_type="menu")
    def coming_soon(self):
        main = self.screen_manager.create_frame()
        main.default.title()
        main.default.content(text="Coming Soon!")
        main.custom.main_menu_button()
        main.custom.sign_out_button()