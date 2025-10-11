import customtkinter as tk

class Frames(tk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color="transparent")
        self.place(relx=0.5, rely=0.5, anchor="center")  # Centres the frame

class FrameManager(tk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color="transparent")
        self.place(relx=0.5, rely=0.5, anchor="center")

        self.components = []

    def create_component(self, component_type, **kwargs):
        component = component_type(self, **kwargs)
        self.components.append(component)
        return component
    
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