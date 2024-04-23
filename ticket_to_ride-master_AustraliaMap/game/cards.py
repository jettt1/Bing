from random import shuffle

from .classes import Destination


def init_decks():
    """
    Initializes all decks
    """

    destinations = shuffle_destinations()
    deck = shuffle_deck()

    return deck, destinations


def shuffle_destinations():
    destinations = [
Destination("Sydney","Broome",2),
Destination("Canberra","Brisbane",3),
Destination("Brisbane","Eucla",3),
Destination("Albany","Cloncurry",3),
Destination("Exmouth","Kalgoorlie",3),
Destination("Broken Hill","Perth",4),
    ]
    shuffle(destinations)
    return destinations


def shuffle_deck():
    # Initialize the deck to have 12 of each color and 14 wild cards (which are just cards colored "None").
    deck = [color for color in range(6)] * 6 + [6] * 8
    shuffle(deck)
    return deck
