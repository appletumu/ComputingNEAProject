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

        # Sets the component's ID. Currently makes text labels as None (may change in the future)
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

            # Similar componets are grouped together.
            # It does this by checking if the previous component is the same type as the current one.
            if current_type == previous_type:
                component.pack(pady=(0, 15))
            else:
                component.pack(pady=(15, 15))
            
            print(f"⚙️ '{component.component_id}' component has been packed.")

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
    
    def centred(self, **kwargs):
        self.configure(fg_color="transparent")
        self.place(relx=0.5, rely=0.5, anchor="center")
    
    def sidebar(self, **kwargs):
        self.configure(fg_color="transparent")
        self.pack(side="left", fill="y", padx=20, pady=20)
    
    def note_taking(self, **kwargs):
        self.configure(fg_color="transparent")
        self.pack(fill="both", expand=True, padx=20, pady=20)