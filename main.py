import tkinter as tk
import random
from window import *

window = Window("Quiz Game")

# Variables
answer_var = tk.StringVar()
index = 0
radio_buttons = []  # To store option widgets so we can remove them later

questions = [
    {
        "question": "What is 1+1?",
        "correctAnswer": "2",
        "extraOptions": ["3", "4", "100000"]
    },
    {
        "question": "What is the capital of France?",
        "correctAnswer": "Paris",
        "extraOptions": ["London", "Berlin", "Madrid"]
    }
]

# Result label
result_label = tk.Label(window, text="")
result_label.pack()

# Question label
question_label = tk.Label(window, text="", font=("Arial", 14))
question_label.pack(pady=10)

# Function to display a question
def load_question():
    global answer_var, radio_buttons
    answer_var.set("")  # Clear selection
    question = questions[index]
    question_label.config(text=question["question"])

    # Remove previous options
    for rb in radio_buttons:
        rb.destroy()
    radio_buttons.clear()

    # Shuffle and display new options
    options = question["extraOptions"] + [question["correctAnswer"]]
    random.shuffle(options)
    for option in options:
        rb = tk.Radiobutton(window, text=option, variable=answer_var, value=option)
        rb.pack(anchor="w")
        radio_buttons.append(rb)

    # Repack the submit button below the new radio buttons
    submit_btn.pack_forget()
    submit_btn.pack(pady=10)

def set_options_state(state):
    for rb in radio_buttons:
        rb.config(state=state)

def check_answer():
    global index

    submit_btn.config(state="disabled")
    set_options_state("disabled")

    if answer_var.get() == questions[index]["correctAnswer"]:
        result_label.config(text="Correct!", fg="green")
        index += 1

        if index < len(questions):
            window.after(2000, load_question)
            window.after(2000, lambda: result_label.config(text=""))
            window.after(2000, lambda: submit_btn.config(state="normal"))
            window.after(2000, lambda: set_options_state("normal"))
        else:
            window.after(2000, lambda: result_label.config(text="You've completed the quiz!", fg="blue"))
            # Optionally disable submit permanently
            # submit_btn.config(state="disabled")
    else:
        result_label.config(text="Wrong! - Try again", fg="red")
        window.after(2000, lambda: result_label.config(text=""))
        window.after(2000, lambda: submit_btn.config(state="normal"))
        window.after(2000, lambda: set_options_state("normal"))



# Submit button
submit_btn = tk.Button(window, text="Submit", command=check_answer)
submit_btn.pack(pady=10)

# Load the first question
load_question()

window.mainloop()
