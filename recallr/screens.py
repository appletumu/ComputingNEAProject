from recallr.ui_elements import Frame, Component


class Screens:
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager

    def login(self):
        frame = Frame(self.screen_manager)
        component = Component(frame)

        component.title(text="Recallr")
        component.content(text="Please fill in your login details!")
        component.entry_field(placeholder_text="Username")
        component.entry_field(placeholder_text="Password")
        component.button(text="Login")
        component.button(text="Create account", button_type="grey")

        self.screen_manager.frames.append(frame)

    def create_account(self):
        frame = Frame(self.screen_manager)
        component = Component(frame)

        component.title(text="Create Account")
        component.content(text="Please fill in the following details!")
        component.entry_field(placeholder_text="New Username")
        component.entry_field(placeholder_text="New Password")
        component.entry_field(placeholder_text="Confirm Password")
        component.button(text="Create account")
        component.button(text="Cancel", button_type="red")

        self.screen_manager.frames.append(frame)

    def main_menu(self):
        frame = Frame(self.screen_manager)
        component = Component(frame)

        component.title(text="Recallr")
        component.content(text="Hello, {username}!")
        component.button(text="Notes")
        component.button(text="Test yourself")
        component.button(text="Settings", button_type="grey")
        component.button(text="Sign out", button_type="red")

        self.screen_manager.frames.append(frame)