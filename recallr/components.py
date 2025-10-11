import customtkinter as tk

class ComponentManager:
    def __init__(self):
        pass

    def button_click(self, button):
        command_handler = ComponentCommandHandler()

        func = getattr(command_handler, button.cget('text').lower().replace(" ", "_"), None)
        func(button)

class Components:
    def __init__(self, frame_manager):
        self.frame_manager = frame_manager
        self.default = DefaultComponents(frame_manager)
        self.custom = CustomComponents(frame_manager)

class DefaultComponents:
    def __init__(self, frame_manager):
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
            "red": {"fg_color": "#FF3333", "hover_color": "#FF6666"},
            "grey": {"fg_color": "#666666", "hover_color": "#808080"},  
        }

        button_instance = self.frame_manager.create_component(
                tk.CTkButton, 
                text=text, 
                font=("Arial", 16), 
                width=200, height=40, 
                fg_color=button_colors[button_type]['fg_color'], 
                hover_color=button_colors[button_type]['hover_color'],
                **kwargs
        )

        component_manager = ComponentManager()
        button_instance.configure(command=lambda b=button_instance: component_manager.button_click(b))

class CustomComponents:
    def __init__(self, frame_manager):
        self.frame_manager = frame_manager
    
    def sign_out_button(self, **kwargs):
        component = Components(self.frame_manager)

        component.default.button(text="Sign out", button_type="red")

class ComponentCommandHandler:
    def __init__(self):
        pass
    
    def login(self, component):
        print("Login button clicked!")