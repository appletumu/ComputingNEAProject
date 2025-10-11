import customtkinter as tk

class ComponentManager:
    def __init__(self, screen_manager):
        self.screen_maanger = screen_manager

    def button_click(self, button):
        command_handler = ComponentCommandHandler(screen_manager=self.screen_maanger)

        func = getattr(command_handler, button.cget('text').lower().replace(" ", "_"), None)
        func(button)

class Components:
    def __init__(self, screen_manager, frame_manager):
        self.screen_manager = screen_manager
        self.frame_manager = frame_manager
        self.default = DefaultComponents(screen_manager, frame_manager)
        self.custom = CustomComponents(screen_manager, frame_manager)

class DefaultComponents:
    def __init__(self, screen_manager, frame_manager):
        self.screen_manager = screen_manager
        self.frame_manager = frame_manager

    def title(self, **kwargs):
        self.frame_manager.create_component(tk.CTkLabel, font=("Arial", 68), **kwargs)

    def content(self, **kwargs):
        self.frame_manager.create_component(tk.CTkLabel, font=("Arial", 16), **kwargs)

    def entry_field(self, **kwargs):
        self.frame_manager.create_component(tk.CTkEntry, font=("Arial", 14), width=200, height=40, **kwargs)

    def button(self, text="Button", button_type="primary", **kwargs):
        button_colors = {
            "primary": {"fg_color": "#104A99", "hover_color": "#1E90FF"},
            "green": {"fg_color": "#218c3a", "hover_color": "#27ae60"},
            "red": {"fg_color": "#FF3333", "hover_color": "#FF6666"},
            "grey": {"fg_color": "#666666", "hover_color": "#808080"},
        }

        if button_type not in button_colors:
            raise ValueError(f"Unknown button_type '{button_type}'. Available types: {list(button_colors.keys())}")

        button_instance = self.frame_manager.create_component(
            tk.CTkButton,
            text=text,
            font=("Arial", 16),
            width=200, height=40,
            fg_color=button_colors[button_type]['fg_color'],
            hover_color=button_colors[button_type]['hover_color'],
            **kwargs
        )

        component_manager = ComponentManager(screen_manager=self.screen_manager)
        button_instance.configure(command=lambda b=button_instance: component_manager.button_click(b))

class CustomComponents:
    def __init__(self, screen_manager, frame_manager):
        self.screen_manager = screen_manager
        self.frame_manager = frame_manager
    
    def sign_out_button(self, **kwargs):
        component = Components(self.screen_manager, self.frame_manager)

        component.default.button(text="Sign out", button_type="red")

class ComponentCommandHandler:
    def __init__(self, screen_manager):
        self.screen_maanger = screen_manager
    
    def login(self, component):
        self.screen_maanger.show_screen("main_menu")

    def create_account(self, component):
        self.screen_maanger.show_screen("create_account")

    def cancel(self, component):
        self.screen_maanger.show_screen("login")

    def sign_out(self, component):
        self.screen_maanger.show_screen("login")

    def notes(self, component):
        self.screen_maanger.show_screen("coming_soon")

    def test_yourself(self, component):
        self.screen_maanger.show_screen("coming_soon")

    def settings(self, component):
        self.screen_maanger.show_screen("coming_soon")

    def main_menu(self, component):
        self.screen_maanger.show_screen("main_menu")