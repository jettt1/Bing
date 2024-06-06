import tkinter as tk

class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ticket To Ride Application")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        self.player_info = None

    def greeting_screen(self, callback):
        self.clear_screen()

        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(expand=True)

        greeting_label = tk.Label(frame, text="Welcome to Ticket To Ride!", font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#333")
        greeting_label.pack(pady=20)

        start_button = tk.Button(frame, text="Start", command=lambda: callback(), font=("Arial", 14), bg="#4CAF50", fg="white", relief="raised", bd=5)
        start_button.pack(pady=10)

    def starting_destination(self, options, callback):
        self.clear_screen()

        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(expand=True, fill=tk.BOTH)

        right_frame = tk.Frame(main_frame, bg="#f0f0f0")
        right_frame.pack(side="right", fill=tk.BOTH, expand=True, padx=10, pady=10)

        label = tk.Label(right_frame, text="Choose an option:", font=("Arial", 18), bg="#f0f0f0", fg="#333")
        label.pack(pady=10)

        for idx, option in enumerate(options):
            button = tk.Button(right_frame, text=option, command=lambda idx=idx: self.set_choice(callback, idx), font=("Arial", 14), bg="#2196F3", fg="white", relief="raised", bd=5)
            button.pack(pady=5)

    def selection_screen(self, player_info, options, callback, mapping=None):
        self.clear_screen()

        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Left frame
        left_frame = tk.Frame(main_frame, bg="#f0f0f0")
        left_frame.pack(side="left", fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Upper left frame
        upper_left_frame = tk.Frame(left_frame, bg="#f0f0f0")
        upper_left_frame.pack(fill=tk.BOTH, expand=True)

        # Displaying the player info in a nicely formatted box
        info_frame = tk.Frame(upper_left_frame, bg="#ffffff", bd=2, relief="solid")
        info_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        score_label = tk.Label(info_frame, text=f"Score: {player_info.score}", font=("Arial", 14), bg="#ffffff", fg="#333")
        score_label.pack(pady=5)

        hand_label = tk.Label(info_frame, text="Hand:", font=("Arial", 14), bg="#ffffff", fg="#333")
        hand_label.pack(pady=5)

        hand_text = self.format_hand(player_info.hand)
        hand_display = tk.Label(info_frame, text=hand_text, font=("Arial", 14), bg="#ffffff", fg="#333")
        hand_display.pack(pady=5)

        car_label = tk.Label(info_frame, text=f"Number of Cars left: {player_info.num_cars}", font=("Arial", 14), bg="#ffffff", fg="#333")
        car_label.pack(pady=5)

        # Lower left frame
        lower_left_frame = tk.Frame(left_frame, bg="#f0f0f0")
        lower_left_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        listbox = tk.Listbox(lower_left_frame, font=("Arial", 12))
        listbox.pack(side="left", fill=tk.BOTH, expand=True)

        for item in player_info.destinations:
            listbox.insert(tk.END, item)

        scrollbar_left = tk.Scrollbar(lower_left_frame, orient="vertical", command=listbox.yview)
        listbox.configure(yscrollcommand=scrollbar_left.set)
        scrollbar_left.pack(side="right", fill="y")

        # Right frame
        right_frame = tk.Frame(main_frame, bg="#f0f0f0")
        right_frame.pack(side="right", fill=tk.BOTH, expand=True, padx=10, pady=10)

        label = tk.Label(right_frame, text="Choose an option:", font=("Arial", 18), bg="#f0f0f0", fg="#333")
        label.pack(pady=10)

        canvas = tk.Canvas(right_frame, bg="#f0f0f0")
        scrollbar_right = tk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#f0f0f0")

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_right.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar_right.pack(side="right", fill="y")

        for idx, option in enumerate(options):
            mapped_idx = mapping[idx] if mapping else idx
            button = tk.Button(scroll_frame, text=option, command=lambda idx=mapped_idx: self.set_choice(callback, idx), font=("Arial", 14), bg="#2196F3", fg="white", relief="raised", bd=5)
            button.pack(pady=5, anchor="e", fill="x")  # Adjust the anchor and fill here

    def format_hand(self, hand):
        """
        
        Returns the player's cards formatted as a string

        """
        hand_str = hand.cards_str(hand.cards)
        hand_list = hand_str.strip("()").split(", ")

        from collections import Counter
        count = Counter(hand_list)

        # Format the output string
        hand_text = '\n'.join([f"{color}:{count}" for color, count in count.items()])

        return hand_text

    def set_choice(self, callback, choice):
        callback(choice)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
