from .classes import Edge, Colors


cities = ("Brooklyn",
"Central Park",
"Chelsea",
"Chinatown",
"East Village",
"Empire State Building",
"Gramercy Park",
"Greenwich Village",
"Lincoln Center",
"Lower East Side",
"Midtown West",
"Soho",
"Times Square",
"United Nations"
          )


def create_board():
    """
    Initializes the entirety of the board state.
    """
    # Create all the edges between cities.
    edges = [
Edge("Brooklyn","Chinatown", cost=3, color=Colors.yellow),
Edge("Brooklyn","Chinatown", cost=3, color=Colors.red),
Edge("Brooklyn","Lower East Side", cost=3, color=Colors.none),
Edge("Brooklyn","Wall Street", cost=3, color=Colors.blue),
Edge("Brooklyn","Wall Street", cost=3, color=Colors.black),
Edge("Central Park","Lincoln Center", cost=2, color=Colors.yellow),
Edge("Central Park","Times Square", cost=2, color=Colors.black),
Edge("Central Park","Times Square", cost=2, color=Colors.red),
Edge("Central Park","United Nations", cost=3, color=Colors.pink),
Edge("Chelsea","Empire State Building", cost=2, color=Colors.none),
Edge("Chelsea","Empire State Building", cost=2, color=Colors.none),
Edge("Chelsea","Gramercy Park", cost=2, color=Colors.yellow),
Edge("Chelsea","Greenwich Village", cost=3, color=Colors.red),
Edge("Chelsea","Greenwich Village", cost=3, color=Colors.green),
Edge("Chelsea","Midtown West", cost=2, color=Colors.blue),
Edge("Chelsea","Soho", cost=4, color=Colors.pink),
Edge("Chinatown","Greenwich Village", cost=2, color=Colors.none),
Edge("Chinatown","Greenwich Village", cost=2, color=Colors.none),
Edge("Chinatown","Lower East Side", cost=1, color=Colors.blue),
Edge("Chinatown","Wall Street", cost=1, color=Colors.green),
Edge("Chinatown","Wall Street", cost=1, color=Colors.pink),
Edge("East Village","Gramercy Park", cost=2, color=Colors.none),
Edge("East Village","Greenwich Village", cost=2, color=Colors.blue),
Edge("East Village","Lower East Side", cost=1, color=Colors.black),
Edge("Empire State Building","Gramercy Park", cost=1, color=Colors.blue),
Edge("Empire State Building","Gramercy Park", cost=1, color=Colors.red),
Edge("Empire State Building","Midtown West", cost=2, color=Colors.green),
Edge("Empire State Building","Times Square", cost=1, color=Colors.pink),
Edge("Empire State Building","Times Square", cost=1, color=Colors.yellow),
Edge("Empire State Building","United Nations", cost=2, color=Colors.black),
Edge("Gramercy Park","Greenwich Village", cost=2, color=Colors.pink),
Edge("Gramercy Park","Greenwich Village", cost=2, color=Colors.black),
Edge("Gramercy Park","United Nations", cost=3, color=Colors.green),
Edge("Greenwich Village","Lower East Side", cost=2, color=Colors.none),
Edge("Greenwich Village","Soho", cost=2, color=Colors.yellow),
Edge("Lincoln Center","Midtown West", cost=2, color=Colors.red),
Edge("Lincoln Center","Times Square", cost=2, color=Colors.green),
Edge("Lincoln Center","Times Square", cost=2, color=Colors.blue),
Edge("Midtown West","Times Square", cost=1, color=Colors.none),
Edge("Soho","Wall Street", cost=2, color=Colors.none),
Edge("Times Square","United Nations", cost=2, color=Colors.none)
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
