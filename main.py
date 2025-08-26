import tkinter as tk
from window import *

window = Window("Quiz Game")

question_label = tk.Label(window, text="What is the capital of France?", font=("Arial", 14))
question_label.pack(pady=10)

# Answer options
answer_var = tk.StringVar()

options = ["Paris", "London", "Berlin", "Rome"]
for option in options:
    tk.Radiobutton(window, text=option, variable=answer_var, value=option).pack(anchor="w")

# Submit button
def check_answer():
    if answer_var.get() == "Paris":
        result_label.config(text="Correct!", fg="green")
    else:
        result_label.config(text="Wrong!", fg="red")

submit_btn = tk.Button(window, text="Submit", command=check_answer)
submit_btn.pack(pady=10)

# Result
result_label = tk.Label(window, text="")
result_label.pack()

window.mainloop()
