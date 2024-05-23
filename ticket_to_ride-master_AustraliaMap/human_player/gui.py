# gui.py
import tkinter as tk
from tkinter import messagebox

class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Screen")

    def greeting_screen(self):
        self.clear_screen()
        greeting_label = tk.Label(self.root, text="Welcome to the App!", font=("Arial", 24))
        greeting_label.pack(pady=20)

        start_button = tk.Button(self.root, text="Start", command=self.selection_screen)
        start_button.pack(pady=10)

    def selection_screen(self):
        self.clear_screen()
        selection_label = tk.Label(self.root, text="Please make a selection:", font=("Arial", 16))
        selection_label.pack(pady=20)

        self.selection_var = tk.StringVar(value="Option1")

        option1 = tk.Radiobutton(self.root, text="Option 1", variable=self.selection_var, value="Option1")
        option1.pack(anchor='w')

        option2 = tk.Radiobutton(self.root, text="Option 2", variable=self.selection_var, value="Option2")
        option2.pack(anchor='w')

        option3 = tk.Radiobutton(self.root, text="Option 3", variable=self.selection_var, value="Option3")
        option3.pack(anchor='w')

        submit_button = tk.Button(self.root, text="Submit", command=self.return_selection)
        submit_button.pack(pady=20)

    def return_selection(self):
        selection = self.selection_var.get()
        messagebox.showinfo("Selection", f"You selected: {selection}")
        self.control_callback(selection)

    def set_control_callback(self, callback):
        self.control_callback = callback

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
