from .classes import Edge, Colors


cities = ("Darwin",
"Perth",
"Canberra",
"Melbourne",
"Hobart",
"Brisbane",
"Sydney",
"Adelaide",
"Broken Hill",
"Alice Springs",
"Katherine",
"Kalgoorlie",
"Cairns",
"Albany",
"Exmouth",
"Halls Creek",
"Longreach",
"Wiluna",
"Warburton",
"Cape York",
"Emerald",
"Coober Pedy",
"Geraldton",
"Cloncurry",
"Tennant Creek",
"Eucla",
"Lake Disappointment",
"Thargomindah"
        )


def create_board():
    """
    Initializes the entirety of the board state.
    """
    # Create all the edges between cities.
    edges = [
Edge("Darwin","Katherine", cost=1, color=Colors.red),
Edge("Darwin","Broome", cost=6, color=Colors.yellow),

Edge("Perth","Geraldton", cost=2, color=Colors.pink),
Edge("Perth","Albany", cost=2, color=Colors.green),
Edge("Perth","Kalgoorlie", cost=3, color=Colors.red),

Edge("Canberra","Broken Hill", cost=5, color=Colors.red),
Edge("Canberra","Sydney", cost=1, color=Colors.green),
Edge("Canberra","Melbourne", cost=2, color=Colors.yellow),
Edge("Canberra","Hobart", cost=4, color=Colors.black),

Edge("Melbourne","Hobart", cost=3, color=Colors.green),
Edge("Melbourne","Adelaide", cost=3, color=Colors.blue),

Edge("Brisbane","Sydney", cost=5, color=Colors.pink),
Edge("Brisbane","Thargomindah", cost=5, color=Colors.green),
Edge("Brisbane","Emerald", cost=3, color=Colors.green),
Edge("Brisbane","Cairns", cost=6, color=Colors.none),

Edge("Sydney","Canberra", cost=1, color=Colors.none),

Edge("Adelaide","Melbourne", cost=3, color=Colors.blue),
Edge("Adelaide","Broken Hill", cost=2, color=Colors.black),
Edge("Adelaide","Eucla", cost=5, color=Colors.pink),
Edge("Adelaide","Coober Pedy", cost=4, color=Colors.green),

Edge("Broken Hill","Coober Pedy", cost=3, color=Colors.pink),
Edge("Broken Hill","Thargomindah", cost=2, color=Colors.green),

Edge("Alice Springs","Coober Pedy", cost=3, color=Colors.yellow),
Edge("Alice Springs","Thargomindah", cost=5, color=Colors.black),
Edge("Alice Springs","Warburton", cost=4, color=Colors.pink),
Edge("Alice Springs","Tennant Creek", cost=2, color=Colors.blue),

Edge("Katherine","Darwin", cost=1, color=Colors.red),
Edge("Katherine","Halls Creek", cost=4, color=Colors.pink),
Edge("Katherine","Tennant Creek", cost=3, color=Colors.pink),

Edge("Kalgoorlie","Perth", cost=3, color=Colors.red),
Edge("Kalgoorlie","Wiluna", cost=3, color=Colors.yellow),
Edge("Kalgoorlie","Warburton", cost=4, color=Colors.blue),
Edge("Kalgoorlie","Eucla", cost=4, color=Colors.green),

Edge("Cairns","Cape York", cost=4, color=Colors.yellow),
Edge("Cairns","Emerald", cost=4, color=Colors.blue),
Edge("Cairns","Cloncurry", cost=4, color=Colors.green),

Edge("Albany","Eucla", cost=6, color=Colors.yellow),

Edge("Exmouth","Broome", cost=6, color=Colors.blue),
Edge("Exmouth","Lake Disappointment", cost=5, color=Colors.none),
Edge("Exmouth","Geraldton", cost=5, color=Colors.red),
Edge("Exmouth","Wiluna", cost=5, color=Colors.pink),

Edge("Halls Creek","Broome", cost=3, color=Colors.none),
Edge("Halls Creek","Lake Disappointment", cost=5, color=Colors.black),
Edge("Halls Creek","Katherine", cost=4, color=Colors.blue),

Edge("Longreach","Emerald", cost=2, color=Colors.black),
Edge("Longreach","Cloncurry", cost=2, color=Colors.red),
Edge("Longreach","Thargomindah", cost=3, color=Colors.yellow),

Edge("Wiluna","Geraldton", cost=3, color=Colors.black),
Edge("Wiluna","Lake Disappointment", cost=2, color=Colors.green),

Edge("Warburton","Kalgoorlie", cost=4, color=Colors.none),
Edge("Warburton","Tennant Creek", cost=6, color=Colors.yellow),
Edge("Warburton","Coober Pedy", cost=5, color=Colors.red),

Edge("Cape York","Cairns", cost=4, color=Colors.red),
Edge("Cape York","Cloncurry", cost=5, color=Colors.none),

Edge("Emerald","Longreach", cost=2, color=Colors.none),

Edge("Coober Pedy","Alice Springs", cost=3, color=Colors.yellow),
Edge("Coober Pedy","Broken Hill", cost=3, color=Colors.black),
Edge("Coober Pedy","Eucla", cost=3, color=Colors.red),

Edge("Geraldton","Perth", cost=2, color=Colors.none),

Edge("Cloncurry","Longreach", cost=2, color=Colors.blue),
Edge("Cloncurry","Tennant Creek", cost=3, color=Colors.black),

Edge("Tennant Creek","Alice Springs", cost=2, color=Colors.blue),
Edge("Tennant Creek","Cloncurry", cost=3, color=Colors.yellow),
Edge("Tennant Creek","Katherine", cost=3, color=Colors.red),

Edge("Eucla","Kalgoorlie", cost=4, color=Colors.black),
Edge("Eucla","Adelaide", cost=5, color=Colors.none),
Edge("Eucla","Coober Pedy", cost=3, color=Colors.blue),

Edge("Thargomindah","Broken Hill", cost=2, color=Colors.blue),
Edge("Thargomindah","Longreach", cost=3, color=Colors.pink),

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
