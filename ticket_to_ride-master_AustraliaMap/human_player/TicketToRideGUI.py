import tkinter as tk
from tkinter import messagebox

class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Screen")

    def greeting_screen(self, callback):
        self.clear_screen()
        greeting_label = tk.Label(self.root, text="Welcome to the App!", font=("Arial", 24))
        greeting_label.pack(pady=20)

        start_button = tk.Button(self.root, text="Start", command=lambda: callback())
        start_button.pack(pady=10)

    def selection_screen(self, options, callback):
        self.clear_screen()
        selection_label = tk.Label(self.root, text="Make a selection:", font=("Arial", 16))
        selection_label.pack(pady=20)

        self.selection_var = tk.StringVar(value=options[0])

        for index, option in enumerate(options):
            rb = tk.Radiobutton(self.root, text=option, variable=self.selection_var, value=index)
            rb.pack(anchor='w')

        submit_button = tk.Button(self.root, text="Submit", command=lambda: callback(self.selection_var.get()))
        submit_button.pack(pady=20)



    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
