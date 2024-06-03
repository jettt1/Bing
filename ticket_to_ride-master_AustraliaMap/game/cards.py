from random import shuffle
import json
from .classes import Destination

destinations = list()

def destinations_config(destination_config):
    global destinations
    with open(destination_config, 'r') as e:
        config = json.load(e)
        
        # Load destinations from the config file and create Destination objects
        destinations = [Destination(dest["city1"], dest["city2"], dest["points"]) for dest in config["destinations"]]

def init_decks():
    """
    Initializes all decks
    """
    shuffled_destinations = shuffle_destinations()
    deck = shuffle_deck()

    return deck, shuffled_destinations

def shuffle_destinations():

    #Copy and paste this for New York destinations: "game\config_files\NewYork\NY_destinations.json"
    #Copy and paste this for Australia destinations: "game\config_files\Australia\destinations.json"
    try:
        destinations_config(r"game\config_files\Australia\destinations.json")
    
    except Exception as e:
       print(f"An error occurred while loading destinations, look for formatting or data entry mistakes: {e}") 
    
    shuffle(destinations)
    return destinations

def shuffle_deck():
    # Initialize the deck to have 12 of each color and 14 wild cards (which are just cards colored "None").
    deck = [color for color in range(6)] * 6 + [6] * 8
    shuffle(deck)
    return deck