import tkinter as tk

class Window(tk.Tk):
    def __init__(self, title):
        super().__init__()

        self.title(title)

class Components(Window):
    def __init__(self, ):
        super().__init__()

        # Wil contain buttons, and stuff