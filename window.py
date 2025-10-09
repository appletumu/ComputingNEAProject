import customtkinter as tk

class Window(tk.CTk):
    def __init__(self, title):
        super().__init__()

        self.title(title)
        self.geometry("800x600")
        tk.set_appearance_mode("light") 

    def display_screen(self):
        return

class Components():
    def __init__(self, window):
        self.window = window

    def display_title(self):
        frame = tk.CTkFrame(self.window, fg_color="transparent")
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