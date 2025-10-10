from recallr.ui_elements import Frame, Component


class Screens:
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager

    def login_screen(self):
        frame = Frame(self.screen_manager)
        component = Component(frame)

        component.title(text="Recallr")
        component.content(text="Please fill in your login details!")
        component.entry_field(placeholder_text="Username")
        component.entry_field(placeholder_text="Password")
        component.button(text="Login")
        component.button(text="Create account", button_type="grey")

        self.screen_manager.frames.append(frame)