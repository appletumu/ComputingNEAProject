import customtkinter as tk

class Window(tk.CTk):
    def __init__(self, title):
        super().__init__()

        self.title(title)
        self.geometry("800x600")
        tk.set_appearance_mode("light") 

    def startup(self):
        print("Window started up.")
        frame = Frame(self)
        component = Component(frame)

        component.title(text="Recallr")
        component.content(text="Please fill in your login details!")
        component.entry_field(placeholder_text="Username")
        component.entry_field(placeholder_text="Password")
        component.button(text="Login")
        component.button(text="Create account", button_type="grey")

        frame.load_components()
        print("Window sucessfully started up.")

class Frame(tk.CTkFrame):
    def __init__(self, window, **kwargs):
        super().__init__(window, **kwargs)

        self.configure(fg_color="transparent")
        self.place(relx=0.5, rely=0.5, anchor="center") # Centres the frame

        self.components = []
    
    def load_components(self):
        previous_type = None

        for component in self.components:
            current_type = type(component)

            if current_type == previous_type:
                component.pack(pady=(0, 15))
            else:
                component.pack(pady=(15, 15))
            
            print(f"{component} has been packed.")

            previous_type = current_type
    
    def clear_components(self):
        raise NotImplementedError("This method is not yet implemented.")

class Component:
    def __init__(self, root):
        self.root = root
    
    def button_click(self, button):
        print(f"'{button.cget('text')}' Button clicked!")
    
    def create_component(self, component_type, **kwargs):
        component = component_type(self.root, **kwargs)
        self.root.components.append(component)
        return component

    def title(self, **kwargs):
        self.create_component(tk.CTkLabel, font=("Arial", 68), **kwargs)

    def content(self, **kwargs):
        self.create_component(tk.CTkLabel, font=("Arial", 16), **kwargs)

    def entry_field(self, **kwargs):
        self.create_component(tk.CTkEntry, font=("Arial", 14), width=200, height=40, **kwargs)

    def button(self, text="Button", button_type="primary", **kwargs):
        if button_type == "primary":
            fg_color = "#1E90FF"  # Blue
            hover_color = "#66B2FF"  # Lighter blue
        elif button_type == "red":
            fg_color = "#FF0000"  # Red
            hover_color = "#FF6666"  # Lighter red
        elif button_type == "grey":
            fg_color = "#808080"  # Grey
            hover_color = "#D3D3D3"  # Ligher grey

        button_instance = self.create_component(tk.CTkButton, text=text, font=("Arial", 16), width=200, height=40, fg_color=fg_color, hover_color=hover_color, **kwargs)
        button_instance.configure(command=lambda b=button_instance: self.button_click(b))