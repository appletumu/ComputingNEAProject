import customtkinter as tk

class Window(tk.CTk):
    def __init__(self, title):
        super().__init__()

        self.title(title)
        self.geometry("800x600")
        tk.set_appearance_mode("light") 

    def display_the_shit(self):
        frame = tk.CTkFrame(self, fg_color="transparent")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        label = tk.CTkLabel(frame, text="Recallr", font=("Arial", 68))
        label.pack(pady=(15, 5))

        label = tk.CTkLabel(frame, text="Please fill in your login details!", font=("Arial", 16))
        label.pack(pady=(5, 15))

        textbox = tk.CTkEntry(frame, placeholder_text="Username", font=("Arial", 14), width=200, height=40)
        textbox.pack(pady=(15, 5))

        textbox = tk.CTkEntry(frame, placeholder_text="Password", font=("Arial", 14), width=200, height=40)
        textbox.pack(pady=(5, 15))

        label = tk.CTkButton(frame, text="Login", font=("Arial", 14), width=200, height=40)
        label.pack(pady=(15, 5))

        label = tk.CTkButton(frame, text="Create account", font=("Arial", 16), width=200, height=40)
        label.pack(pady=(5, 15))

    def display_screen(self):
        components = Components(self)
        components.create_frame()

        components.title("Recallr")
        components.content("Please fill in your login details!")
        components.entry_field("Username")
        components.entry_field("Password")
        components.button("Login")
        components.button("Create account")

class Components():
    def __init__(self, window):
        self.window = window
        self.frame = None

    def create_frame(self):
        self.frame = tk.CTkFrame(self.window, fg_color="transparent")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

    def title(self, text="Title"):
        component = tk.CTkLabel(self.frame, text=text, font=("Arial", 68))
        component.pack(pady=(15, 5))

    def content(self, text="Content"):
        component = tk.CTkLabel(self.frame, text=text, font=("Arial", 16))
        component.pack(pady=(5, 15))

    def entry_field(self, text="Fill in details"):
        component = tk.CTkEntry(self.frame, placeholder_text=text + "...", font=("Arial", 14), width=200, height=40)
        component.pack(pady=(15, 5))

    def button(self, text="Button"):
        component = tk.CTkButton(self.frame, text=text, font=("Arial", 16), width=200, height=40)
        component.pack(pady=(5, 15))