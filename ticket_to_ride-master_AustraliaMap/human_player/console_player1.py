import tkinter as tk
from game import Player, Colors, DrawDeckAction, DrawFaceUpAction, DrawDestinationAction, Game, Hand, FailureCause

class ConsolePlayer(tk.Tk):
    def __init__(self, players):
        super().__init__()
        self.title("Ticket to Ride")  # Set the title of the window
        self.geometry("800x600")  # Set the initial size of the window
        self.players = players  # Store the list of players
        self.game = Game(players)  # Initialize your game instance
        self.create_widgets()  # Create GUI widgets

    def create_widgets(self):
        # Create GUI widgets
        self.info_label = tk.Label(self, text="Game Information:")
        self.info_label.pack()

        self.info_text = tk.Text(self, height=10, width=50)
        self.info_text.pack()

        self.message_label = tk.Label(self, text="Messages:")
        self.message_label.pack()

        self.message_text = tk.Text(self, height=5, width=50)
        self.message_text.pack()

        self.draw_deck_button = tk.Button(self, text="Draw Card from Deck", command=self.draw_card_from_deck)
        self.draw_deck_button.pack()

        self.draw_destination_button = tk.Button(self, text="Draw Destination Card", command=self.draw_destination_card)
        self.draw_destination_button.pack()

        # Buttons for face-up cards will be dynamically created based on the game state
        self.face_up_card_buttons = []

        self.update_game_info()

    def update_game_info(self):
        # Update the game information displayed in the GUI
        self.info_text.delete(1.0, tk.END)
        players_info = self.game.get_players_info()
        for player_info in players_info:
            self.info_text.insert(tk.END, f"{player_info.name}: {player_info.points} points\n")
        self.info_text.insert(tk.END, f"Remaining cards in deck: {len(self.game.deck)}")

    def display_message(self, message):
        # Display messages in the GUI
        self.message_text.insert(tk.END, message + "\n")
        
def take_turn(self):
    # Get the current player
    current_player = self.game.get_current_player()

    # Display player's scores and status
    self.display_message("Scores: %s" % self.game.get_visible_scores())
    self.display_message("Status: %s" % self.game.get_player_info(current_player))

    # Display available destinations if GUI is enabled
    if self.game.gui:
        self.game.gui.update(self.game)
        self.game.gui.show_destinations(self.game.get_player_info(current_player).destinations)

    # Loop until there is an action to take.
    action = None
    while action is None:
        # Ask the user to select a type of action if they have any options.
        remaining_actions = self.game.get_remaining_actions(current_player)
        if remaining_actions != 1:
            action_type = self.get_selection("Choose a type of action to take:\n0: Draw Card\n1: Draw Tickets\n2: Connect Cities")
        else:
            action_type = 0

        if action_type == 0:
            # Pick from available cards
            face_up_cards = self.game.get_face_up_cards()
            options = ["Draw from Deck"] + [Colors.str_card(card) for card in face_up_cards if card != Colors.none or remaining_actions != 1]

            # Display available draw options
            selection = self.get_selection("Choose draw:\n" + "\n".join(f"{i+1}: {option}" for i, option in enumerate(options)) + "\n" + f"{len(options)+1}: Cancel")

            if selection == 0:
                action = DrawDeckAction()
            elif 0 < selection <= len(face_up_cards):
                if face_up_cards[selection - 1] != Colors.none or remaining_actions != 1:
                    action = DrawFaceUpAction(selection - 1, face_up_cards[selection - 1])
        elif action_type == 1:
            # Draw a destination card
            action = DrawDestinationAction()
        elif action_type == 2:
            # Connect Edges
            edges_seen = set()
            all_actions = self.game.get_available_actions(current_player)

            # Find all edges that can be connected with the set of currently available actions.
            for action_iter in all_actions:
                if action_iter.is_connect():
                    edges_seen.add(action_iter.edge)

            edges_seen = sorted(edges_seen, key=lambda edge: (edge.color, edge.cost))
            if self.game.gui:
                self.game.gui.show_edges(edges_seen)

            # Show options for selection to user.
            options = [str(edge) for edge in edges_seen]
            options.append("Cancel")

            selection = self.get_selection("Choose a route to claim:\n" + "\n".join(f"{i}: {option}" for i, option in enumerate(options)))

            if 0 <= selection < len(edges_seen):
                # Ask how the user would like to claim the edge.
                possible_actions = Game.all_connection_actions(edges_seen[selection], self.game.get_player_info(current_player).hand.cards, self.game.get_player_info(current_player).num_cars)

                # Show options for card selection to user.
                card_options = [Hand.cards_str(action.cards) for action in possible_actions]
                card_options.append("Cancel")

                card_selection = self.get_selection("Choose which cards to use:\n" + "\n".join(f"{i}: {option}" for i, option in enumerate(card_options)))

                if 0 <= card_selection < len(possible_actions):
                    action = possible_actions[card_selection]

    return action
    def enable_face_up_card_buttons(self):
        # Enable buttons for drawing face-up cards
        for i in range(len(self.face_up_card_buttons)):
            self.face_up_card_buttons[i].config(state=tk.NORMAL)

    def disable_all_buttons(self):
        # Disable all buttons
        self.draw_deck_button.config(state=tk.DISABLED)
        self.draw_destination_button.config(state=tk.DISABLED)
        for button in self.face_up_card_buttons:
            button.config(state=tk.DISABLED)


    def draw_card_from_deck(self):
        # Draw a card from the deck
        current_player = self.game.get_current_player()
        action = DrawDeckAction()
        result = self.game.take_action(current_player, action)

        # Update game information and display message
        self.update_game_info()
        if result[0]:
            self.display_message(f"{current_player.name} drew a card from the deck")
        else:
            self.display_message(f"{current_player.name} attempted to draw a card from the deck, but failed: {FailureCause.str(result[1])}")

        # Check if the game has ended
        if self.game.is_game_over():
            self.display_message("Game Over!")
            # Implement game over logic here

        # Disable face-up card buttons
        self.disable_face_up_card_buttons()

    def draw_face_up_card(self, index):
        # Draw a face-up card
        current_player = self.game.get_current_player()
        face_up_cards = self.game.get_face_up_cards()

        if index < 0 or index >= len(face_up_cards):
            self.display_message("Invalid selection")
            return

        selected_card = face_up_cards[index]

        # Check if the selected card is a wild card
        if selected_card == Colors.none and self.game.get_remaining_actions(current_player) == 1:
            self.display_message("You cannot select a wild card with only one action left")
            return

        action = DrawFaceUpAction(index, selected_card)
        result = self.game.take_action(current_player, action)

        # Update game information and display message
        self.update_game_info()
        if result[0]:
            self.display_message(f"{current_player.name} drew a {Colors.str_card(selected_card)} card from the face-up cards")
        else:
            self.display_message(f"{current_player.name} attempted to draw a {Colors.str_card(selected_card)} card from the face-up cards, but failed: {FailureCause.str(result[1])}")

        # Check if the game has ended
        if self.game.is_game_over():
            self.display_message("Game Over!")
            # Implement game over logic here

        # Disable face-up card buttons
        self.disable_face_up_card_buttons()

    def draw_destination_card(self):
        # Draw a destination card
        current_player = self.game.get_current_player()
        action = DrawDestinationAction()
        result = self.game.take_action(current_player, action)

        # Update game information and display message
        self.update_game_info()
        if result[0]:
            self.display_message(f"{current_player.name} drew a destination card")
        else:
            self.display_message(f"{current_player.name} attempted to draw a destination card, but failed: {FailureCause.str(result[1])}")

        # Check if the game has ended
        if self.game.is_game_over():
            self.display_message("Game Over!")
            # Implement game over logic here

        # Disable face-up card buttons
        self.disable_face_up_card_buttons()

if __name__ == "__main__":
    app = TicketToRideGUI()
    app.mainloop()