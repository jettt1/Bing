import json
import configparser
from pathlib import Path
from game import Game

# Load configuration
config_path = Path(r'game\config_files\game_settings.json')
with config_path.open('r') as config_file:
    config = json.load(config_file)

# Create players list (example, adjust as needed)
players = []  # Populate this with actual player objects

# Initialize the Game with configuration parameters
game = Game(
    players=players,
    maximum_rounds=config.get("maximum_rounds"),
    print_debug=config.get("print_debug"),
    custom_settings=config.get("custom_settings"),
    city_edges=config.get("city_edges"),
    edges=config.get("edges"),
    deck=config.get("deck"),
    destinations=config.get("destinations"),
    num_cars=config.get("num_cars")
)

# def color_config(c_config):
#         global colors_list
#         with open(c_config, 'r') as c:
#             config = json.load(c)
            
#             # Load destinations from the config file and create Destination objects
#             colors_list = list(config["colors"])
#     # colors_list = list(color_config.keys())
#     # globals().update({color.lower(): index for index, color in enumerate(colors_list)})
#     # none = len(colors_list) 

# # red, blue, yellow, green, pink, black, none = range(7)
# color_config(r"C:\Users\jetpr\OneDrive\Documents\Jet\UNSW UNIVERSITY\YEAR 3 - Semester 1\3118 - IT Project 1\colours.json")
#     # colors_list = ['Red', 'Blue', 'Yellow', 'Green', 'Pink', 'Black']

# for i in colors_list:
#     colors_list[i] = i

# print(colors_list)

# class ColorEnum:
#     @classmethod
#     def load_enum(cls, config_file):
#         config = configparser.ConfigParser()
#         config.read(config_file)
#         colors = config['Colors']
#         for color_name, value in colors.items():
#             setattr(cls, color_name, int(value))

# # Example usage
# ColorEnum.load_enum("C:\Users\jetpr\OneDrive\Documents\Jet\UNSW UNIVERSITY\YEAR 3 - Semester 1\3118 - IT Project 1\colour_count.json")
# print()