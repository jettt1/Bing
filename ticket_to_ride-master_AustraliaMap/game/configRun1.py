import json
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