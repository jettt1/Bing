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
Destination("Lower East Side","Wall Street",2),
Destination("Midtown West","Central Park",3),
Destination("Empire State Building","Greenwich Village",3),
Destination("Midtown West","United Nations",3),
Destination("Lincoln Center","Empire State Building",3),
Destination("Gramercy Park","Chinatown",4),
Destination("Soho","East Village",4),
Destination("Central Park","Gramercy Park",4),
Destination("Times Square","East Village",4),
Destination("Chelsea","Central Park",5),
Destination("Chelsea","Wall Street",6),
Destination("Times Square","Soho",6),
Destination("Lincoln Center","Greenwich Village",6),
Destination("Empire State Building","Brooklyn",7),
Destination("United Nations","Wall Street",8),
Destination("Central Park","Chinatown",8),
Destination("Times Square","Brooklyn",8),
Destination("Chelsea","Brooklyn",8)
    ]
    shuffle(destinations)
    return destinations


def shuffle_deck():
    # Initialize the deck to have 12 of each color and 14 wild cards (which are just cards colored "None").
    deck = [color for color in range(6)] * 6 + [6] * 8
    shuffle(deck)
    return deck
