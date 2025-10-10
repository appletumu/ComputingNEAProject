import customtkinter as tk

class WindowManager(tk.CTk):
    def __init__(self, title):
        super().__init__()

        self.title(title)
        self.geometry("800x600")
        self.minsize(1336, 768)
        tk.set_appearance_mode("light") 

    def startup(self):
        print("WindowManager is starting up...")

        screen_manager = ScreenManager(self)
        screen_manager.show_screen("login_screen")

        print("WindowManager sucessfully started up.")
        self.mainloop()
        print("WindowManager loop has been broken.")

class ScreenManager(tk.CTkFrame):
    def __init__(self, window_manager, **kwargs):
        super().__init__(window_manager, **kwargs)

        self.window_manager = window_manager
        self.frames = []

        self.configure(fg_color="transparent")
        self.pack(fill="both", expand=True)
    
    def show_screen(self, function_name):
        func = getattr(self, function_name, None)
        if callable(func):
            func()
        else:
            raise NameError(f"Function '{function_name}' is not available.")

        for frame in self.frames:
            frame.load_components()

            print(f"'{frame}' frame has been loaded.")

    def login_screen(self):
        frame = Frame(self)
        component = Component(frame)

        component.title(text="Recallr")
        component.content(text="Please fill in your login details!")
        component.entry_field(placeholder_text="Username")
        component.entry_field(placeholder_text="Password")
        component.button(text="Login")
        component.button(text="Create account", button_type="grey")

        self.frames.append(frame)
    
class Frame(tk.CTkFrame):
    def __init__(self, window_manager, **kwargs):
        super().__init__(window_manager, **kwargs)

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
            
            print(f"'{component}' component has been packed.")

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
        button_colors = {
            "primary": {"fg_color": "#1E90FF", "hover_color": "#66B2FF"},
            "red": {"fg_color": "#FF0000", "hover_color": "#FF6666"},
            "grey": {"fg_color": "#808080", "hover_color": "#D3D3D3"},
        }

        button_instance = self.create_component(
                tk.CTkButton, 
                text=text, 
                font=("Arial", 16), 
                width=200, height=40, 
                fg_color=button_colors[button_type]['fg_color'], 
                hover_color=button_colors[button_type]['hover_color'],
                **kwargs
        )
        button_instance.configure(command=lambda b=button_instance: self.button_click(b))