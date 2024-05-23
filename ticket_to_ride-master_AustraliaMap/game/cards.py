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
<<<<<<< Updated upstream
Destination("Cloncurry","Darwin",7),
Destination("Longreach","Perth",18),
Destination("Warburton","Canberra",13),
Destination("Tennant Creek","Melbourne",12),
Destination("Broome","Hobart",25),
Destination("Hobart","Brisbane",10),
Destination("Albany","Sydney",17),
=======
        Destination("Cloncurry","Darwin",7),
        Destination("Longreach","Perth",18),
        Destination("Warburton","Canberra",13),
        Destination("Tennant Creek","Melbourne",12),
        Destination("Broome","Hobart",25),
        Destination("Hobart","Brisbane",10),
        Destination("Albany","Sydney",17),
>>>>>>> Stashed changes
        Destination("Cape York","Adelaide",15),
        Destination("Lake Disappointment","Broken Hill",15),
        Destination("Kalgoorlie","Alice Springs",8),
        Destination("Exmouth","Katherine",13),
        Destination("Halls Creek","Kalgoorlie",7),
        Destination("Adelaide","Cairns",13),
        Destination("Emerald","Albany",19),
        Destination("Darwin","Exmouth",12),
        Destination("Cairns","Halls Creek",14),
        Destination("Sydney","Longreach",10),
        Destination("Eucla","Wiluna",7),
        Destination("Thargomindah","Warburton",9),
        Destination("Geraldton","Cape York",23),
        Destination("Hobart","Emerald",13),
        Destination("Lake Disappointment","Coober Pedy",12),
        Destination("Canberra","Geraldton",19),
        Destination("Broken Hill","Cloncurry",8),
        Destination("Perth","Tennant Creek",13),
        Destination("Brisbane","Eucla",13),
        Destination("Darwin","Lake Disappointment",10),
        Destination("Cape York","Thargomindah",11),
        Destination("Coober Pedy","Broome",15),
    ]
    shuffle(destinations)
    return destinations


def shuffle_deck():
    # Initialize the deck to have 12 of each color and 14 wild cards (which are just cards colored "None").
    deck = [color for color in range(6)] * 6 + [6] * 8
    shuffle(deck)
    return deck
