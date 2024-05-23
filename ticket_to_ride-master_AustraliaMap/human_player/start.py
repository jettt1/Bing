# start.py
import tkinter as tk
from gui import AppGUI
from control import Control

def main():
    root = tk.Tk()
    app_gui = AppGUI(root)
    control = Control(app_gui)

    control.start()

    root.mainloop()

if __name__ == "__main__":
    main()
