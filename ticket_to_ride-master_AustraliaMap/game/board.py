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
        print(edges)

def create_board():
    """
    Initializes the entirety of the board state.
    """
    # Create all the edges between cities.
    edges = [
        Edge("Darwin","Broome", cost=6, color=Colors.yellow),

        Edge("Perth","Geraldton", cost=2, color=Colors.pink),
        Edge("Perth","Geraldton", cost=2, color=Colors.none),
        Edge("Perth","Albany", cost=2, color=Colors.green),
        Edge("Perth","Kalgoorlie", cost=3, color=Colors.red),
        Edge("Perth","Kalgoorlie", cost=3, color=Colors.none),

        Edge("Canberra","Broken Hill", cost=5, color=Colors.red),

        Edge("Canberra","Melbourne", cost=2, color=Colors.yellow),
        Edge("Canberra","Hobart", cost=4, color=Colors.black),

        Edge("Melbourne","Hobart", cost=3, color=Colors.green),

        Edge("Brisbane","Sydney", cost=5, color=Colors.pink),
        Edge("Brisbane","Thargomindah", cost=5, color=Colors.green),
        Edge("Brisbane","Emerald", cost=3, color=Colors.green),
        Edge("Brisbane","Cairns", cost=6, color=Colors.none),

        Edge("Sydney","Canberra", cost=1, color=Colors.none),
        Edge("Sydney","Canberra", cost=1, color=Colors.green),

        Edge("Adelaide","Melbourne", cost=3, color=Colors.blue),
        Edge("Adelaide","Melbourne", cost=3, color=Colors.none),

        Edge("Adelaide","Broken Hill", cost=2, color=Colors.black),

        Edge("Adelaide","Coober Pedy", cost=4, color=Colors.green),

        Edge("Alice Springs","Thargomindah", cost=5, color=Colors.black),
        Edge("Alice Springs","Warburton", cost=4, color=Colors.pink),

        Edge("Katherine","Darwin", cost=1, color=Colors.red),
        Edge("Katherine","Darwin", cost=1, color=Colors.green),

        Edge("Katherine","Halls Creek", cost=4, color=Colors.pink),
        Edge("Katherine","Halls Creek", cost=4, color=Colors.blue),
        Edge("Katherine","Tennant Creek", cost=3, color=Colors.pink),
        Edge("Katherine","Tennant Creek", cost=3, color=Colors.red),

        Edge("Kalgoorlie","Wiluna", cost=3, color=Colors.yellow),

        Edge("Kalgoorlie","Eucla", cost=4, color=Colors.green),
        Edge("Kalgoorlie","Eucla", cost=4, color=Colors.black),

        Edge("Cairns","Emerald", cost=4, color=Colors.blue),
        Edge("Cairns","Cloncurry", cost=4, color=Colors.green),

        Edge("Albany","Eucla", cost=6, color=Colors.yellow),

        Edge("Exmouth","Broome", cost=6, color=Colors.blue),
        Edge("Exmouth","Lake Disappointment", cost=5, color=Colors.none),
        Edge("Exmouth","Geraldton", cost=5, color=Colors.red),
        Edge("Exmouth","Wiluna", cost=5, color=Colors.pink),

        Edge("Halls Creek","Broome", cost=3, color=Colors.none),
        Edge("Halls Creek","Lake Disappointment", cost=5, color=Colors.black),

        Edge("Longreach","Cloncurry", cost=2, color=Colors.red),
        Edge("Longreach","Cloncurry", cost=2, color=Colors.blue),

        Edge("Longreach","Thargomindah", cost=3, color=Colors.yellow),
        Edge("Longreach","Thargomindah", cost=3, color=Colors.pink),

        Edge("Wiluna","Geraldton", cost=3, color=Colors.black),
        Edge("Wiluna","Lake Disappointment", cost=2, color=Colors.green),

        Edge("Warburton","Kalgoorlie", cost=4, color=Colors.none),
        Edge("Warburton","Kalgoorlie", cost=4, color=Colors.blue),

        Edge("Warburton","Tennant Creek", cost=6, color=Colors.yellow),
        Edge("Warburton","Coober Pedy", cost=5, color=Colors.red),

        Edge("Cape York","Cairns", cost=4, color=Colors.red),
        Edge("Cape York","Cairns", cost=4, color=Colors.yellow),
        Edge("Cape York","Cloncurry", cost=5, color=Colors.none),

        Edge("Emerald","Longreach", cost=2, color=Colors.none),
        Edge("Emerald","Longreach", cost=2, color=Colors.black),

        Edge("Coober Pedy","Alice Springs", cost=3, color=Colors.yellow),
        Edge("Coober Pedy","Alice Springs", cost=3, color=Colors.red),

        Edge("Coober Pedy","Broken Hill", cost=3, color=Colors.black),
        Edge("Coober Pedy","Broken Hill", cost=3, color=Colors.pink),

        Edge("Tennant Creek","Alice Springs", cost=2, color=Colors.blue),
        Edge("Tennant Creek","Alice Springs", cost=2, color=Colors.none),

        Edge("Tennant Creek","Cloncurry", cost=3, color=Colors.yellow),
        Edge("Tennant Creek","Cloncurry", cost=3, color=Colors.black),

        Edge("Eucla","Adelaide", cost=5, color=Colors.none),
        Edge("Eucla","Adelaide", cost=5, color=Colors.pink),

        Edge("Eucla","Coober Pedy", cost=3, color=Colors.blue),
        Edge("Eucla","Coober Pedy", cost=3, color=Colors.red),

        Edge("Thargomindah","Broken Hill", cost=2, color=Colors.blue),
        Edge("Thargomindah","Broken Hill", cost=2, color=Colors.green),

        Edge("Broome","Lake Disappointment", cost=4, color=Colors.red),
    ]

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
