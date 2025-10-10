from recallr.ui_elements import Frame, Component

def setup_screen(func, screen_type="menu"):
    def wrapper(self, *args, **kwargs):
        frame = Frame(self.screen_manager)
        component = Component(frame)

        # Call the decorated screen method
        func(self, component, *args, **kwargs)

        self.screen_manager.frames.append(frame)
    return wrapper

class Screens:
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager

    @setup_screen(screen_type="menu")
    def login(self, component):
        component.title(text="Recallr")
        component.content(text="Please fill in your login details!")
        component.entry_field(placeholder_text="Username")
        component.entry_field(placeholder_text="Password")
        component.button(text="Login")
        component.button(text="Create account", button_type="grey")

    @setup_screen(screen_type="menu")
    def create_account(self, component):
        component.title(text="Create Account")
        component.content(text="Please fill in the following details!")
        component.entry_field(placeholder_text="New Username")
        component.entry_field(placeholder_text="New Password")
        component.entry_field(placeholder_text="Confirm Password")
        component.button(text="Create account")
        component.button(text="Cancel", button_type="red")

    @setup_screen(screen_type="menu")
    def main_menu(self, component):
        component.title(text="Recallr")
        component.content(text="Hello, {username}!")
        component.button(text="Notes")
        component.button(text="Test yourself")
        component.button(text="Settings", button_type="grey")
        component.button(text="Sign out", button_type="red")