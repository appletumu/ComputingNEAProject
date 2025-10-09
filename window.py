import customtkinter as tk

class Window(tk.CTk):
    def __init__(self, title="Window"):
        super().__init__()

        self.title(title)
        self.geometry("800x600")

    def display_screen(self):
        return

class Components():
    def __init__(self, window):
        self.window = window

    def display_title(self):
        label = tk.CTkLabel(self.window, text="Recallr", font=("Arial", 24))
        label.place(relx=0.5, rely=0.3, anchor="center")

        label = tk.CTkLabel(self.window, text="Please fill in your login details!", font=("Arial", 11))
        label.place(relx=0.5, rely=0.4, anchor="center")

        textbox = tk.CTkEntry(self.window, placeholder_text="Username", font=("Arial", 11))
        textbox.place(relx=0.5, rely=0.5, anchor="center")
        
        textbox = tk.CTkEntry(self.window, placeholder_text="Password", font=("Arial", 11))
        textbox.place(relx=0.5, rely=0.6, anchor="center")

        label = tk.CTkButton(self.window, text="Login", font=("Arial", 11))
        label.place(relx=0.5, rely=0.7, anchor="center")

        label = tk.CTkButton(self.window, text="Create account", font=("Arial", 11))
        label.place(relx=0.5, rely=0.8, anchor="center")