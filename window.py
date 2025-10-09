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
        frame = Frame(self)

        frame.components.title("Recallr")
        frame.components.content("Please fill in your login details!")
        frame.components.entry_field("Username")
        frame.components.entry_field("Password")
        frame.components.button("Login")
        frame.components.button("Create account")

class Frame(tk.CTkFrame):
    def __init__(self, window, **kwargs):
        super().__init__(window, **kwargs)

        self.configure(fg_color="transparent")
        self.place(relx=0.5, rely=0.5, anchor="center") # Centres the frame

        self.components = Components(self)

class Components:
    def __init__(self, frame):
        self.frame = frame

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