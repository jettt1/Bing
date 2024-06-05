from .classes import Edge, Colors
import json

cities = tuple()
edges = list()

def cities_config(config_file):
    global cities
    
    with open(config_file, 'r') as f:
        config = json.load(f)
        
        # Load cities from the config file
        cities = tuple(config["cities"])

def edge_config(edges_config):
    global edges
    with open(edges_config, 'r') as e:
        config1 = json.load(e)
        
        # Convert the edges from dictionaries to Edge objects
        edges = [Edge(edge["city1"], edge["city2"], edge["cost"], getattr(Colors, edge["color"])) for edge in config1["edges"]]

def create_board():
    """
    Initializes the entirety of the board state.
    """

    #New York map cities:
    #cities_config(r"game\config_files\NewYork\NY_cities.json")

    #Australia map cities:
    #cities_config(r"game\config_files\Australia\cities.json")

    try:
        cities_config(r"game\config_files\NewYork\NY_cities.json")

    except Exception as e:
        print(f"An error occurred while loading cities, look for formatting or data entry mistakes: {e}")
    
    #New York map edges
    #edge_config(r"game\config_files\NewYork\NY_edges.json")

    #Australia map edges:
    #edge_config(r"game\config_files\Australia\edges.json")
    try:
        edge_config(r"game\config_files\NewYork\NY_edges.json")

    except Exception as e:
        print(f"An error occurred while loading edges, look for formatting or data entry mistakes: {e}")
    
    return create_city_edges(edges), edges

def create_city_edges(edges):
    city_edges = {}

    # Map cities to edges.
    for edge in edges:
        if edge.city1 not in city_edges:
            city_edges[edge.city1] = ()
        if edge.city2 not in city_edges:
            city_edges[edge.city2] = ()

        city_edges[edge.city1] = city_edges[edge.city1] + (edge,)
        city_edges[edge.city2] = city_edges[edge.city2] + (edge,)

    return city_edges

def get_scoring():
    # Create a dictionary for scoring.
    return {1: 1,
            2: 2,
            3: 4,
            4: 7,
            5: 10,
            6: 15}
