# control.py
class Control:
    def __init__(self, gui):
        self.gui = gui
        self.gui.set_control_callback(self.return_selection)

    def start(self):
        self.gui.greeting_screen()

    def return_selection(self, selection):
        print(f"Control received the selection: {selection}")
        # Add your logic here based on the selection
        return selection

    def test(self):
        selection = self.gui.set_control_callback(self.return_selection)
        print("this is working", selection)


