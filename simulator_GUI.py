import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import ImageTk, Image
import random

class StartMenu(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)
        self.configure(bg="#36454f") 
        self.create_widgets()

    #Starting screen
    def create_widgets(self):
        title_label = tk.Label(self, text="Ticket-To-Ride Australia", font=("Helvetica", 24, "bold"), bg="#36454f", fg="#ffffff")
        title_label.pack(pady=(30, 20))

        start_button = StyledButton(self, text="Start Simulator", command=self.start_game)
        start_button.pack(pady=20, ipadx=20, ipady=10)

        quit_button = StyledButton(self, text="Quit", command=self.master.destroy)
        quit_button.pack(pady=20, ipadx=20, ipady=10)

    def start_game(self):
        # Destroy the current frame (start menu)
        self.destroy()

        # Create and display the game screen
        game_screen = TicketApp(self.master)
        game_screen.pack(fill=tk.BOTH, expand=True)


class TicketApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Ticket App")
        self.master.geometry("800x600")
        
        self.current_screen = None
        self.destination_screen()

    def switch_screen(self, new_screen):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = new_screen

    #Second window where you select destination tickets
    def destination_screen(self):
        destination_frame = tk.Frame(self.master, bg = "#36454f")
        destination_frame.pack(expand=True, fill='both')

        title_label = tk.Label(destination_frame, text="Choose Destination Ticket", font=("Helvetica", 24, "bold"), bg="#36454f", fg="#ffffff")
        title_label.pack(pady=(30, 20))

        # Variable to hold the selected ticket
        self.selected_ticket = tk.StringVar()

        # Create radiobuttons for destination ticket selection
        options = ["No Tickets", "Ticket 1", "Ticket 2", "Ticket 3"]

        for option in options:
            rb = tk.Radiobutton(destination_frame, text=option, variable=self.selected_ticket, value=option, font=("Helvetica", 12), bg="#36454f", fg="#ffffff", selectcolor="#007bff", activebackground="#36454f", activeforeground="#ffffff")
            rb.pack(anchor='center', pady=5)

        # "Next" button to proceed
        next_button = StyledButton(destination_frame, text="Next", command=self.save_and_main_screen)
        next_button.pack(pady=20, ipadx=20, ipady=10)

        self.switch_screen(destination_frame)

    #saves the selection and goes to the next screen
    def save_and_main_screen(self):
        selected_ticket = self.selected_ticket.get()

        if not selected_ticket:
            messagebox.showwarning("No Ticket Selected", "Please choose a ticket option.")
            return

        # Example of saving selected ticket (print for demonstration)
        print("Selected Ticket:", selected_ticket)

        # Proceed to main screen
        self.main_screen()

    #Main screen with image and key functionality
    def main_screen(self):
        main_frame = tk.Frame(self.master, bg="#36454f")
        main_frame.pack(expand=True, fill='both')

        # Load and display an image in the middle
        image_path = r"C:\Users\jetpr\OneDrive\Desktop\ACTUALFINALMAP.png"
        img = Image.open(image_path)
        img = img.resize((500, 400), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        img_label = tk.Label(main_frame, image=img, bg="#36454f")
        img_label.image = img
        img_label.grid(row=0, column=0, padx=20, pady=20)  # Centered image in column 0

        # Create button frame on the right
        button_frame = tk.Frame(main_frame, bg="#36454f")
        button_frame.grid(row=0, column=1, sticky='e', padx=20, pady=20)  # Align buttons to the middle right

        draw_card_button = StyledButton(button_frame, text="Draw Card", command=self.draw_card_popup)
        draw_card_button.pack(pady=10, fill=tk.X)

        draw_ticket_button = StyledButton(button_frame, text="Draw Ticket", command=self.draw_ticket_popup)
        draw_ticket_button.pack(pady=10, fill=tk.X)

        connect_cities_button = StyledButton(button_frame, text="Connect Cities", command=self.connect_cities_popup)
        connect_cities_button.pack(pady=10, fill=tk.X)

        quit_button = StyledButton(button_frame, text="Quit", command=self.master.destroy)
        quit_button.pack(pady=5, fill=tk.X)

        # Configure grid weights to center the image in the main_frame
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=0)  # Prevent button column from expanding vertically

        # Center the button frame vertically
        button_frame.grid_rowconfigure(0, weight=1)

        self.switch_screen(main_frame)

    #Draw cards button popup
    def draw_card_popup(self):

        # Create a pop-up window for drawing cards
        popup = tk.Toplevel(self.master)
        popup.title("Draw Card")
        popup.geometry("600x400")

        
        options = ["Blue", "Red", "Yellow", "Black", "Green", "Pink", "Wild Card"]

        self.checkbox_var = []

        # "Draw from Deck" button
        def draw_from_deck():
            selected_cards = random.sample(options, 3)  # Draw 3 random cards
            messagebox.showinfo("Draw Card", f"Drawn Cards: {', '.join(selected_cards)}")

        tk.Button(popup, text="Draw from Deck", command=draw_from_deck).pack(pady=5, fill=tk.X)

        # Create checkboxes
        tk.Label(popup, text="Select Card(s):").pack(pady=10)

        for option in options:
            var = tk.IntVar()
            checkbox = tk.Checkbutton(popup, text=option, variable=var)
            checkbox.pack()
            self.checkbox_var.append((var, option))
        
        # Limit maximum selections to 1 for Wild Card, and 2 for other
        def validate_checkbox():
            wild_card_selected = self.checkbox_var[-1][0].get()
            if wild_card_selected:
                for var, option in self.checkbox_var[:-1]:
                    if var.get() == 1:
                        var.set(0)
            else:
                selected_count = sum(var.get() for var, option in self.checkbox_var[:-1])
                if selected_count > 2:
                    # Deselect the last selected checkbox if not Wild Card
                    for var, option in self.checkbox_var[:-1]:
                        if var.get() == 1:
                            var.set(0)

        # Bind validation to checkbox selection
        for var, option in self.checkbox_var:
            var.trace_add('write', lambda *args, var=var: validate_checkbox())

         # "Confirm" button
        def confirm_selection():
            selected_cards = [option for var, option in self.checkbox_var if var.get() == 1]
            if len(selected_cards) > 2:
                messagebox.showwarning("Selection Limit Exceeded", "You can only select up to 2 cards.")
            elif len(selected_cards) == 0:
                messagebox.showwarning("No Selection", "Please select at least one card.")
            else:
                messagebox.showinfo("Confirmed Selection", f"Selected Cards: {', '.join(selected_cards)}")
        tk.Button(popup, text="Confirm", command=confirm_selection).pack(pady=10, fill=tk.X)

        # "Cancel" button
        tk.Button(popup, text="Cancel", command=popup.destroy).pack(pady=5, fill=tk.X)

    #Draw ticket button popup
    def draw_ticket_popup(self):
        # Create a pop-up window for drawing tickets
        popup = tk.Toplevel(self.master)
        popup.title("Draw Ticket")

        # Section 1: Keep Tickets Button
        keep_frame = tk.Frame(popup)
        keep_frame.pack(pady=10)

        tk.Button(keep_frame, text="Keep Tickets", command=popup.destroy).pack(pady=5, fill=tk.X)

        # Section 2: Ticket to Discard
        discard_frame = tk.Frame(popup)
        discard_frame.pack(pady=10)

        # Checkboxes for ticket selection
        tk.Label(discard_frame, text="Ticket to Discard:").pack(pady=5)

        ticket_options = ["Sydney-Melbourne", "Brisbane-Perth", "Adelaide-Darwin"]

        checkbox_vars = []
        selected_checkboxes = []  # To keep track of selected checkboxes

        def on_checkbox_click(var):
            # Ensure only up to two checkboxes are selected
            if var.get() == 1:
                if len(selected_checkboxes) >= 2:
                    var.set(0)  # If already 2 selected, deselect this one
                else:
                    selected_checkboxes.append(var)
            else:
                if var in selected_checkboxes:
                    selected_checkboxes.remove(var)

        for option in ticket_options:
            var = tk.IntVar()
            checkbox = tk.Checkbutton(discard_frame, text=option, variable=var, command=lambda v=var: on_checkbox_click(v))
            checkbox.pack(anchor="w")
            checkbox_vars.append(var)

        # Confirm button for ticket selection
        def confirm_discard():
            selected_tickets = [option for i, option in enumerate(ticket_options) if checkbox_vars[i].get() == 1]
            if len(selected_tickets) > 2:
                messagebox.showwarning("Selection Limit Exceeded", "You can only select up to 2 tickets to discard.")
            else:
                messagebox.showinfo("Confirmed Selection", f"Selected Cards: {', '.join(selected_tickets)}")
                popup.destroy()

        tk.Button(discard_frame, text="Confirm Discard", command=confirm_discard).pack(pady=10, fill=tk.X)

        # Place the pop-up window in the center of the screen
        popup.geometry("400x300+" + str(int(self.master.winfo_screenwidth()/2 - 200)) +
                    "+" + str(int(self.master.winfo_screenheight()/2 - 150)))

        # "Cancel" button
        tk.Button(popup, text="Cancel", command=popup.destroy).pack(pady=5, fill=tk.X)

    #Connect cities button popup
    def connect_cities_popup(self):
        # Define available routes between cities along with possible cards for each route
        routes = {
            ("Sydney", "Melbourne"): ["Blue", "Red", "Wild Card"],
            ("Brisbane", "Perth"): ["Yellow", "Black", "Wild Card"],
            ("Adelaide", "Darwin"): ["Green", "Pink", "Wild Card"]
        }

        # Create a pop-up window for connecting cities and selecting routes
        popup = tk.Toplevel(self.master)
        popup.title("Connect Cities - Select Route and Card")
        popup.geometry("400x300+" + str(int(self.master.winfo_screenwidth()/2 - 200)) +
                    "+" + str(int(self.master.winfo_screenheight()/2 - 150)))

        # Section 1: Route Selection (Dropdown Menu)
        selected_route = tk.StringVar()
        selected_route.set("")  # Set default selection

        tk.Label(popup, text="Routes").pack(pady=10)  # Title for route selection
        route_options = sorted(routes.keys())  # Get sorted route pairs

        # Dropdown menu for route selection
        route_menu = tk.OptionMenu(popup, selected_route, *route_options)
        route_menu.pack(pady=10)

        # Section 2: Card Selection (Dropdown Menu)
        def update_card_menu(selected):
            # Clear previous card menu
            card_menu['menu'].delete(0, 'end')

            # Create new card options based on selected route
            if selected:
                cards_for_route = routes[selected]
                for card in cards_for_route:
                    card_menu['menu'].add_command(label=card, command=tk._setit(selected_card, card))

                # Enable card selection menu
                card_menu.config(state="normal")

        tk.Label(popup, text="Card to Use").pack(pady=10)  # Title for card selection

        selected_card = tk.StringVar()
        selected_card.set("")  # Set default selection

        # Dropdown menu for card selection (initially disabled)
        card_menu = tk.OptionMenu(popup, selected_card, "")
        card_menu.pack(pady=10)

        # Confirm button for route and card selection
        def confirm_selection():
            route_selected = selected_route.get()
            card_selected = selected_card.get()

            if route_selected and card_selected:
                # Display confirmation message with selected route and card
                messagebox.showinfo("Selection Confirmed", f"Selected Route: {route_selected}, Selected Card: {card_selected}")
                popup.destroy()

        # Create and pack the "Confirm" button
        tk.Button(popup, text="Confirm", command=confirm_selection).pack(pady=10, fill=tk.X)

        # Update card menu when route selection changes
        selected_route.trace_add('write', lambda *args: update_card_menu(selected_route.get()))

        # Initialize card menu based on default (empty) route selection
        update_card_menu(selected_route.get())

#dont worry about this, just how the buttons are styled/designed
class StyledButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(font=("Helvetica", 14, "bold"), bg="#007bff", fg="#ffffff", activebackground="#0056b3", activeforeground="#ffffff")

def main():
    root = tk.Tk()
    root.title("Ticket To Ride Simulator")
    root.geometry("800x600")
    root.configure(bg="#f0f0f0")

    start_menu = StartMenu(root)
    start_menu.pack(fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()