import customtkinter as tk

class ComponentManager:
    def __init__(self, root):
        self.root = root
    
    def button_click(self, button):
        print(f"'{button.cget('text')}' Button clicked!")

class Components:
    def __init__(self, component_manager):
        self.component_manager = component_manager
        self.default = DefaultComponents(component_manager)

class DefaultComponents:
    def __init__(self, component_manager):
        self.component_manager = component_manager

    def title(self, **kwargs):
        self.component_manager.create_component(tk.CTkLabel, font=("Arial", 68), **kwargs)

    def content(self, **kwargs):
        self.component_manager.create_component(tk.CTkLabel, font=("Arial", 16), **kwargs)

    def entry_field(self, **kwargs):
        self.component_manager.create_component(tk.CTkEntry, font=("Arial", 14), width=200, height=40, **kwargs)

    def button(self, text="Button", button_type="primary", **kwargs):
        button_colors = {
            "primary": {"fg_color": "#104A99", "hover_color": "#1E90FF"},
            "red": {"fg_color": "#FF3333", "hover_color": "#FF6666"},
            "grey": {"fg_color": "#666666", "hover_color": "#808080"},  
        }

        button_instance = self.component_manager.create_component(
                tk.CTkButton, 
                text=text, 
                font=("Arial", 16), 
                width=200, height=40, 
                fg_color=button_colors[button_type]['fg_color'], 
                hover_color=button_colors[button_type]['hover_color'],
                **kwargs
        )
        button_instance.configure(command=lambda b=button_instance: self.button_click(b))