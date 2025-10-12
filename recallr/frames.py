import customtkinter as tk

class FrameManager(tk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Sets up the frame
        self.configure(fg_color="transparent")
        self.place(relx=0.5, rely=0.5, anchor="center")

        self.components = []

    def create_component(self, component_type, component_id, **kwargs):
        component = component_type(self, **kwargs)

        if isinstance(component, tk.CTkLabel) and component_id == None:
            component.component_id = None
        elif isinstance(component, tk.CTkEntry) and component_id == None:
            component.component_id = component.cget("placeholder_text").lower().replace(" ", "_")
        elif component_id == None:
            component.component_id = component.cget("text").lower().replace(" ", "_")
        else:
            component.component_id = component_id

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
            
            print(f"'{component.component_id}' component has been packed.")

            previous_type = current_type
    
    def find_component(self, component_id):
        for component in self.components:
            if component.component_id == component_id:
                return component
        return None
    
    def clear_components(self):
        raise NotImplementedError("This method is not yet implemented.")
class Frames(tk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color="transparent")
        self.place(relx=0.5, rely=0.5, anchor="center")  # Centres the frame