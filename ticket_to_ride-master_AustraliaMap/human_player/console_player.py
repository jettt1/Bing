import tkinter as tk
from human_player.TicketToRideGUI import AppGUI
import copy

from game import Player, Colors, DrawDeckAction, DrawFaceUpAction, DrawDestinationAction, Game, Hand, FailureCause

class ConsolePlayer(Player):
    """
    A Human player that uses the console to play the game.
    """

    def __init__(self, name):
        Player.__init__(self, name)
        self._drew_card_from_deck = False
        self.player_info = None
        self.gui = None
        print("self.gui is set to NONE")
        print(self.gui)

    def __deepcopy__(self, memo):
        # Create a shallow copy of the object
        new_copy = copy.copy(self)
        # Manually deepcopy all attributes except those related to tkinter GUI
        for attr, value in self.__dict__.items():
            if attr == 'gui':
                setattr(new_copy, attr, value)
            else:
                setattr(new_copy, attr, copy.deepcopy(value, memo))
        return new_copy


    def set_gui(self, gui):
        self.gui = gui
        print(f"SET_GUI: GUI set in ConsolePlayer: {self.gui}")  # Debug print to confirm GUI is set
        print(id(self.gui))
        print(self.gui)


    def take_turn(self, game):
        self._drew_card_from_deck = False
        action = None
        all_actions = game.get_available_actions(self)
        self.player_info = game.get_player_info(self)

        print ("Scores: %s" % game.get_visible_scores())
        print ("Status: %s" % self.player_info)

        if game.gui:
            #print 'attempting to display edges'
            game.gui.update(game)
            game.gui.show_destinations(self.player_info.destinations)

        # Loop until there is an action to take.
        while action is None:
            # Ask the user to select a type of action if they have any options.
            if game.get_remaining_actions(self) != 1:
                print ("")
                print ("Choose a type of action to take:")
                print ("0: Draw Card")
                print ("1: Draw Tickets")
                print ("2: Connect Cities")

                action_type = choice = self.get_choice(["0", "1", "2"])
            else:
                # If there is only one action left, just force the player to draw.
                action_type = 0

            if action_type == 0:
                # Pick from available cards
                face_up_cards = game.get_face_up_cards()

                print ("")
                print ("Choose draw:")
                print ("0: Draw from Deck")

                for i in range(len(face_up_cards)):
                    # Make sure that the user does not have the option to draw wilds.
                    if face_up_cards[i] != Colors.none or game.get_remaining_actions(self) != 1:
                        print ("%d: %s" % (i + 1, Colors.str_card(face_up_cards[i])))

                if game.get_remaining_actions(self) != 1:
                    print ("%d: Cancel" % (len(face_up_cards) + 1))

                selection = ConsolePlayer.get_selection()

                if selection == 0:
                    action = DrawDeckAction()
                    self._drew_card_from_deck = True
                elif 0 < selection <= len(face_up_cards):
                    if face_up_cards[selection - 1] != Colors.none or game.get_remaining_actions(self) != 1:
                        action = DrawFaceUpAction(selection - 1, face_up_cards[selection - 1])
            elif action_type == 1:
                # Draw a destination card
                action = DrawDestinationAction()
            elif action_type == 2:
                # Connect Edges
                edges_seen = set()

                # Find all edges that can be connected with the set of currently available actions.
                for action_iter in all_actions:
                    if action_iter.is_connect():
                        edges_seen.add(action_iter.edge)

                edges_seen = list(edges_seen)
                edges_seen.sort(key=lambda edge: (edge.color, edge.cost))
                if game.gui:
                    #print 'attempting to display edges'
                    game.gui.show_destinations(self.player_info.destinations)
                    game.gui.show_edges(edges_seen)


                # Show options for selection to user.
                print ("")
                print ("Choose a route to claim:")
                for i in range(len(edges_seen)):
                    print ("%d: %s" % (i, str(edges_seen[i])))

                print ("%d: Cancel" % (len(edges_seen)))

                selection = ConsolePlayer.get_selection()

                if 0 <= selection < len(edges_seen):
                    # Ask how the user would like to claim the edge.
                    possible_actions = Game.all_connection_actions(edges_seen[selection], self.player_info.hand.cards,self.player_info.num_cars)

                    print ("")
                    print ("Choose which cards to use:")
                    for i in range(len(possible_actions)):
                        print ("%d: %s" % (i, Hand.cards_str(possible_actions[i].cards)))

                    print ("%d: Cancel" % (len(possible_actions)))

                    selection = ConsolePlayer.get_selection()

                    if 0 <= selection < len(possible_actions):
                        action = possible_actions[selection]

        print ("")
        return action

    def game_ended(self, game):
        pass

    def on_action_complete(self, game, result):
        if not result[0]:
            # Print action failure, which should never happen.
            print ("Action failed: %s" % FailureCause.str(result[1]))
            print ("")
        elif self._drew_card_from_deck:
            # If the player just drew a card from the deck, then figure out what the new card is and output the result.
            if game.gui:
                game.gui.update(game)

            old_cards = self.player_info.hand.cards
            new_cards = game.get_player_info(self).hand.cards

            new_cards.subtract(old_cards)

            # There should only be one card in the counter that results from the difference of the new hand with the
            # old one.
            for card in new_cards.elements():
                print ("Drew Card: %s" % Colors.str_card(card))
                print ("")

    def select_destinations(self, game, destinations):
        # Choice will indicate which destination the player chose to remove.
        selection = -1

        while not (0 <= selection <= len(destinations)) and len(destinations) > 1:
            print ("Choose a ticket to discard:")
            print ("0: Keep all tickets")
            for i in range(len(destinations)):
                print ("%d: %s" % (i + 1, str(destinations[i])))

            selection = ConsolePlayer.take_turn(self, game).selected_index

            if selection != 0:
                del destinations[selection - 1]
                selection = -1
            else:
                break

            print ("")

        return destinations

    def select_starting_destinations(self, game, destinations):
        selection = -1
        tempL = []

        #self.gui.greeting_screen(self._dummy_callback)

        while not (0 <= selection <= len(destinations)):
            print("Choose a ticket to discard:")
            print("0: Keep all tickets")
            for i in range(len(destinations)):
                temp = [i + 1, str(destinations[i])]
                tempL.append(temp)
                print("%d: %s" % (i + 1, str(destinations[i])))

            choice = self.get_choice(["Keep all tickets", tempL[0], tempL[1], tempL[2]])

            # Call starting_destination_screen and pass the list of starting tickets
            selection = choice

        if selection != 0:
            del destinations[selection - 1]

        return destinations

    def _dummy_callback(self):
        # Dummy callback function for GUI actions
        print("dummy called")
        pass

    def get_choice(self, options):
        self.choice = None
        self.gui.selection_screen(options, self.set_choice)
        while self.choice is None:
            self.gui.root.update()  # Wait for user to make a selection
        return int(self.choice)

    def set_choice(self, choice):
        self.choice = choice

    def get_selection():
        """
        Get a user's selection for the next move.

        :return: An integer indicating what the user selected, or -1 if the user made an invalid selection.
        """
        selection = input("Selection: ")

        if not selection.isdigit():
            return -1
        else:
            return int(selection)