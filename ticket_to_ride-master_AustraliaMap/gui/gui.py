from game.classes import *
from game.player import *
import json
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from game.board import create_board

class MapLoader:
    def __init__(self, config_file):
        self.config = self.load_config(config_file)
        
    def load_config(self, config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    
    def load_map(self, map_name):
        map_info = self.config['maps'].get(map_name)
        if not map_info:
            raise ValueError(f"Map '{map_name}' not found in config.")
        img = mpimg.imread(map_info['path'])
        return img, map_info
class GUI:

    #Paste this in Path for New York map: 'game\config_files\NewYork\NY_placeCities.json'

    def __init__(self, config_path=Path(r'game\config_files\NewYork\NY_placeCities.json'), x_size=6, y_size=10):

        print('initializing gui')
        self.needs_reset = False

        self.config_path = config_path
        config_file = 'game/config_files/maps_config.json'
        self.map_loader = MapLoader(config_file)
        
        # Load map information from the configuration file. Change the string in the below load_map() function from 
        #"Australia" to "NewYork" to change to the New York map
        img, map_info = self.map_loader.load_map("NewYork")
        if img is None or map_info is None:
            raise ValueError("Failed to load map. Make sure the file path for the image is correct and the string in the load_map() function is correct")
        
        plt.ion()
        self.fig = plt.figure(figsize=(map_info['x_size'], map_info['y_size']))
        plt.imshow(img)
        plt.xlim(map_info['xlim'])
        plt.ylim(map_info['ylim'])
        plt.show()

        # imgplot = plt.imdraw(img)
        self.place_cities()
        self.plot_board()
        self.set_colors()

        [city_edges, edges] = create_board()

        x_offset = 15
        y_offset = -5

        # Plot the edges for connecting cities
        for index1, edge in enumerate(edges):
            offset = 0
            for index2, edge2 in enumerate(edges):
                # Check if this is a double edge
                if edge.city1 is edge2.city1 and edge.city2 is edge2.city2 and edge is not edge2:
                    if (index1 > index2):
                        offset = -1
                    else:
                        offset = 1

            x_1 = []
            y_1 = []
            x_1.append(self.cities[edge.city1][0] + offset * x_offset)
            y_1.append(self.cities[edge.city1][1] + offset * y_offset)
            x_1.append(self.cities[edge.city2][0] + offset * x_offset)
            y_1.append(self.cities[edge.city2][1] + offset * y_offset)
            self.edge_colors[edge] = plt.plot(x_1, y_1, self.colors[edge.color])
            plt.setp(self.edge_colors[edge], linewidth=4)

            x_mean = (x_1[0] + x_1[1]) / 2
            y_mean = (y_1[0] + y_1[1]) / 2
            self.edge_means[edge] = [x_mean, y_mean]

            self.edge_weights[edge] = plt.plot(x_mean, y_mean, 'go')
            plt.setp(self.edge_weights[edge], 'ms', 15.0)
            self.edge_numbers[edge] = plt.text(x_mean - 5, y_mean + 5, str(edge.cost), fontdict=None)

        for city in self.cities:
            self.city_points[city] = plt.plot(self.cities[city][0], self.cities[city][1], 'ro')
            self.city_texts[city] = plt.text(self.cities[city][0] - 5, self.cities[city][1] + 5, '', fontdict=None)

        # Plot the numbers of cards player 1 and 2 have
        # First for player 1
        x = 1022
        y = 55
        i = 0
        for i in range(7):
            self.player_1_cards[str(i)] = plt.text(x, y, '0', fontdict=None)
            x = x + 34
        self.p1_score = plt.text(x + 84, y, '0', fontdict=None)
        self.p1_cars = plt.text(x + 10, y, '0', fontdict=None)

        # Next for player 2
        x = 1022
        y = 187
        i = 0
        for i in range(7):
            self.player_2_cards[str(i)] = plt.text(x, y, '0', fontdict=None)
            x = x + 34
        self.p2_score = plt.text(x + 84, y, '0', fontdict=None)
        self.p2_cars = plt.text(x + 10, y, '0', fontdict=None)

        self.cards['0'] = mpimg.imread('gui/red.png')
        self.cards['1'] = mpimg.imread('gui/blue.png')
        self.cards['2'] = mpimg.imread('gui/yellow.png')
        self.cards['3'] = mpimg.imread('gui/green.png')
        self.cards['4'] = mpimg.imread('gui/pink.png')
        self.cards['5'] = mpimg.imread('gui/black.png')
        self.cards['6'] = mpimg.imread('gui/wild.png')

        i = 0
        # x = 0.858
        # y = 0.78
        x = 0.90
        y = 0.862
        
        for i in range(5):
            self.table_card_slots.append(self.fig.add_axes([x, y - 0.020 * i, 0.034, 0.016], 'auto_scale_on'))
            self.table_card_slots[i].get_xaxis().set_visible(False)
            self.table_card_slots[i].get_yaxis().set_visible(False)
        plt.draw()
        # plt.show()

    # Variables
    colors = []
    cities = dict()
    x = []
    y = []
    player_1_cards = dict()
    player_2_cards = dict()
    edge_weights = dict()
    edge_colors = dict()
    cards = dict()
    table_card_slots = list()
    p1_score = []
    p2_score = []
    p1_cars = []
    p2_cars = []
    fig = []
    edge_icons = dict()
    edge_numbers = dict()
    edge_means = dict()
    need_reset = False
    city_points = dict()
    city_texts = dict()
    destination_cities = dict()

    player_1 = None
    player_2 = None

    def set_city(self, city, number):
        plt.setp(self.city_points[city], 'color', 'w')
        plt.setp(self.city_points[city], marker='H')
        plt.setp(self.city_points[city], 'ms', 20.0)
        plt.setp(self.city_texts[city], text=str(number))

    def reset_cities(self):
        for city in self.city_points:
            plt.setp(self.city_points[city], 'color', 'r')
            plt.setp(self.city_points[city], marker='o')
            plt.setp(self.city_points[city], 'ms', 1.0)
            plt.setp(self.city_texts[city], text=str(''))

    # Display the destinations
    def show_destinations(self, destinations):
        for index, destination in enumerate(destinations):
            self.set_city(destination.city1, index)
            self.set_city(destination.city2, index)
            # plt.ioff()
            # plt.show()

    def show_path(self, path):
        # print 'in show path'
        for edge in path.edges:
            # print edge
            plt.setp(self.edge_colors[edge], linewidth=10)
            plt.setp(self.edge_colors[edge], linestyle='solid')
        self.needs_reset = True
        plt.ioff()
        plt.draw()

    def reset_edge_labels(self, edges):
        for edge in edges:
            plt.setp(self.edge_weights[edge], 'color', 'g')
            plt.setp(self.edge_weights[edge], marker='o')
            plt.setp(self.edge_weights[edge], linewidth=2)
            plt.setp(self.edge_numbers[edge], text=str(edge.cost))
            plt.setp(self.edge_colors[edge], linewidth=2)
            plt.setp(self.edge_colors[edge], linestyle='solid')

    def show_edges(self, edges):
        for index, edge in enumerate(edges):
            # print 'updating:'
            # print edge
            plt.setp(self.edge_weights[edge], 'color', 'w')
            plt.setp(self.edge_weights[edge], marker='s')
            plt.setp(self.edge_numbers[edge], text=str(index))

        self.needs_reset = True
        plt.ioff()
        plt.draw()

    def place_cities(self):
        with open(self.config_path, 'r') as f:
                self.cities = json.load(f)
                       
        print(self.cities)

    def set_colors(self):
        self.colors = ['#b61c16', '#1033bc', '#d8c413', '#13750a', '#6c0a75', '#030203',
                       '#6d696d']

    def plot_board(self):
        for city in self.cities:
            self.x.append(self.cities[city][0])
            self.y.append(self.cities[city][1])

    def update(self, game):
        self.player_1 = str(game._players[0])
        self.player_2 = str(game._players[1])

        if self.needs_reset:
            self.reset_cities()
            self.reset_edge_labels(game.get_edge_claims())
            self.needs_reset = False
        # TODO: Implement.
        self.update_display(game)
        self.update_edges(game)
        self.update_cards(game)
        plt.draw()
        pass

    def update_cards(self, game):
        face_up_cards = game.get_face_up_cards()
        i = 0
        for card_key in face_up_cards:
            # print(str(card_key))
            if (i < len(self.table_card_slots)):
                self.table_card_slots[i].imshow(self.cards[str(card_key)])
                i = i + 1

    def update_display(self, game):
        scores = game.get_visible_scores()

        # print scores
        for player in game._players:
            cards = game.get_player_info(player).hand.cards
            for card in cards:
                if (player.name == self.player_1):
                    self.player_1_cards[str(card)].set_text(str(cards[card]))
                    self.p1_score.set_text(str(scores[player.name]))
                    self.p1_cars.set_text(str(game.get_player_info(player).num_cars))
                elif (player.name == self.player_2):
                    self.player_2_cards[str(card)].set_text(str(cards[card]))
                    self.p2_score.set_text(str(scores[player.name]))
                    self.p2_cars.set_text(str(game.get_player_info(player).num_cars))

    def update_edges(self, game):
        edges = game.get_edge_claims()

        # scoring = dict()

        for index, edge in enumerate(edges):
            # print(edge)
            # print(edges[edge])

            # scoring[edge.cost] = 0

            if (edges[edge] == self.player_1):
                plt.setp(self.edge_weights[edge], 'color', 'b')
                plt.setp(self.edge_colors[edge], 'color', 'b')
                plt.setp(self.edge_colors[edge], marker='.')
                plt.setp(self.edge_colors[edge], linewidth=6)
                plt.setp(self.edge_colors[edge], linestyle='--')
                plt.setp(self.edge_colors[edge], 'ms', 10.0)
            elif (edges[edge] == self.player_2):
                plt.setp(self.edge_weights[edge], 'color', 'r')
                plt.setp(self.edge_colors[edge], 'color', 'r')
                plt.setp(self.edge_colors[edge], marker='.')
                plt.setp(self.edge_colors[edge], linewidth=6)
                plt.setp(self.edge_colors[edge], linestyle='--')
                plt.setp(self.edge_colors[edge], 'ms', 10.0)

                # print(card_value)
                # print(game.get_player_info(player).hand.cards{card})
                # i=i+1

                # print(self.cards_pos_x[int(card)])
                # print(self.cards_pos_y[j])

                # plt.text(self.cards_pos_x[int(card)], self.cards_pos_y[j], str(cards[card]), fontdict=None)
                # path = Path(edges,scoring)
                # self.show_path(path)

    def close(self):
        plt.clf()
        plt.close()
        print ("GUI closed figure")
        # colors = []
        # cities = dict()
        # x = []
        # y = []
        # player_1_cards = dict()
        # player_2_cards = dict()
        # edge_weights = dict()
        # edge_colors = dict()
        # cards = dict()
        # table_card_slots = list()
        # p1_score=[]
        # p2_score=[]
        # p1_cars=[]
        # p2_cars=[]
        # fig = []
        # edge_icons = dict()
        # edge_numbers = dict()
        # edge_means = dict()
        # need_reset =False
        # city_points = dict()
        # city_texts = dict()
        # destination_cities = dict()

    def update_game_ended(self, game):
        self.update(game)
        plt.ioff()
        plt.draw()
        # TODO: Implement.
        pass

    def update_game_ended_and_close(self, game):
        self.update(game)
        plt.ioff()
        plt.draw()
        # TODO: Implement.
        pass

        # game.add_turn_ended_event(self.update)
