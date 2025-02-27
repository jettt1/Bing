from tkinter import messagebox
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

    #Getting deepcopy without tkinter incompatibilities
    def __deepcopy__(self, memo):
        """

        Parameters
        ----------
        memo : TYPE
            DESCRIPTION.

        Returns
        -------
        new_copy : TYPE
            DESCRIPTION.

        """
        # Create a shallow copy of the object
        new_copy = copy.copy(self)
        # Manually deepcopy all attributes except those related to tkinter GUI
        for attr, value in self.__dict__.items():
            if attr == 'gui':
                setattr(new_copy, attr, value)
            else:
                setattr(new_copy, attr, copy.deepcopy(value, memo))
        return new_copy

    #Setting the gui instance
    def set_gui(self, gui):
        self.gui = gui

    def take_turn(self, game):
        """

        Parameters
        ----------
        game : TYPE
            DESCRIPTION.

        Returns
        -------
        action : TYPE
            DESCRIPTION.

        """
        self._drew_card_from_deck = False
        action = None
        all_actions = game.get_available_actions(self)
        self.player_info = game.get_player_info(self)

        print ("Scores: %s" % game.get_visible_scores())
        print("BELOW IS THE PLAYER's INFORMATION")
        print(self.get_player_info())
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

                action_type = self.get_choice(["Draw Card", "Draw Tickets", "Connect Cities"])
                print(action_type)
            else:
                # If there is only one action left, just force the player to draw.
                action_type = 0

            if action_type == 0:
                # Pick from available cards
                face_up_cards = game.get_face_up_cards()

                print ("")
                print ("Choose draw:")
                print ("0: Draw from Deck")
                
                drawcardL = ["Draw from Deck"]
                mapping = {0: 0}
                index = 1
                for i in range(len(face_up_cards)):
                    # Make sure that the user does not have the option to draw wilds.
                    if face_up_cards[i] != Colors.none or game.get_remaining_actions(self) != 1:
                        drawcardL.append(Colors.str_card(face_up_cards[i]))
                        mapping[index] = i + 1
                        print ("%d: %s" % (i + 1, Colors.str_card(face_up_cards[i])))
                        index += 1

                if game.get_remaining_actions(self) != 1:
                    drawcardL.append("Cancel")
                    mapping[index] = len(face_up_cards) + 1
                    print ("%d: Cancel" % (len(face_up_cards) + 1))

                selection = self.get_choice(drawcardL, mapping)
                print(selection)

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
                    game.gui.show_destinations(self.player_info.destinations)
                    game.gui.show_edges(edges_seen)


                # Show options for selection to user.
                print ("")
                print ("Choose a route to claim:")
                claimrouteL = []

                for i in range(len(edges_seen)):
                    temp = [(i, str(edges_seen[i]))]
                    claimrouteL.append(temp)
                    print ("%d: %s" % (i, str(edges_seen[i])))

                print ("%d: Cancel" % (len(edges_seen)))
                claimrouteL.append("Cancel")

                selection = self.get_choice(claimrouteL)

                if 0 <= selection < len(edges_seen):
                    # Ask how the user would like to claim the edge.
                    possible_actions = Game.all_connection_actions(edges_seen[selection], self.player_info.hand.cards,self.player_info.num_cars)
                    routeCardL = []

                    print ("")
                    print ("Choose which cards to use:")
                    for i in range(len(possible_actions)):
                        print ("%d: %s" % (i, Hand.cards_str(possible_actions[i].cards)))
                        temp = [(i, Hand.cards_str(possible_actions[i].cards))]
                        routeCardL.append(temp)

                    routeCardL.append("Cancel")
                    print ("%d: Cancel" % (len(possible_actions)))

                    selection = self.get_choice(routeCardL)

                    if 0 <= selection < len(possible_actions):
                        action = possible_actions[selection]

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
                drawn_card_message = "Drew Card: %s" % Colors.str_card(card)
                messagebox.showinfo("Card Drawn", drawn_card_message)
                print ("")

    def select_destinations(self, game, destinations):
        """

        Parameters
        ----------
        game : TYPE
            DESCRIPTION.
        destinations : TYPE
            DESCRIPTION.

        Returns
        -------
        destinations : TYPE
            DESCRIPTION.

        """
        # Choice will indicate which destination the player chose to remove.
        selection = -1

        while not (0 <= selection <= len(destinations)) and len(destinations) > 1:
            startdestL = ["Keep all tickets"]

            print ("Choose a ticket to discard:")
            print ("0: Keep all tickets")
            for i in range(len(destinations)):
                temp = [i + 1, str(destinations[i])]
                startdestL.append(temp[1])
                print ("%d: %s" % (i + 1, str(destinations[i])))

            selection = self.get_choice(startdestL)

            if selection != 0:
                del destinations[selection - 1]
                selection = -1
            else:
                break

            print ("")

        return destinations

    def select_starting_destinations(self, game, destinations):
        """
        
        Returns the destination tickets selected by the user
        
        """
        selection = -1
        startdestL = ["Keep all tickets"]

        while not (0 <= selection <= len(destinations)):
            print("Choose a ticket to discard:")
            print("0: Keep all tickets")
            for i in range(len(destinations)):
                temp = [i + 1, str(destinations[i])]
                startdestL.append(temp[1])
                print("%d: %s" % (i + 1, str(destinations[i])))

            selection = self.get_initial(startdestL)

        if selection != 0:
            del destinations[selection - 1]

        return destinations


    def get_initial(self, options):
        """

        Returns the selected choice by the user

        """
        self.choice = None
        self.gui.starting_destination(options, self.set_choice)
        while self.choice is None:
            self.gui.root.update()  # Wait for user to make a selection
        return int(self.choice)

    def get_choice(self, options, mapping=None):
        """

        Returns the selected choice by the user

        """
        self.choice = None
        self.gui.selection_screen(self.player_info, options, self.set_choice, mapping)
        while self.choice is None:
            self.gui.root.update()  # Wait for user to make a selection
        return int(self.choice)

    def set_choice(self, choice):
        """

        Sets the choice received from the user

        """
        self.choice = choice

    def get_player_info(self):
        """
        
        Returns the player's information
        
        """
        return self.player_info
