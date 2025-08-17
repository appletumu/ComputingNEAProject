import tkinter as tk

class Window(tk.Tk):
    def __init__(self, title):
        super().__init__()

        self.title(title)