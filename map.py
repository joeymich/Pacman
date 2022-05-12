import pygame
from node import Node
from pellet import Pellet
from wall import Wall
from constants import *

class Map():
    def __init__(self, map=None, home_map=None, pellet_map=None, wall_map=None, wall_rotate_map=None):
        self.node_lut = {}
        self.pellet_lut = {}
        self.walls = []
        self.map = None
        self.home_map = None
        self.pellet_map = None
        self.wall_map = None
        self.wall_rotate_map = None
        if map is not None:
            self.map = self.format_map(map)
            self.fill_node_lut()
            self.connect_nodes()
            self.add_pacman_node()
        if home_map is not None:
            self.home_map = self.format_map(home_map)
            self.fill_home_node_lut()
            self.connect_home_nodes()
            self.connect_home_to_rest()
        if pellet_map is not None:
            self.pellet_map = self.format_map(pellet_map)
            self.fill_pellet_lut()
        if wall_map is not None:
            self.wall_map = wall_map
            self.wall_rotate_map = wall_rotate_map
            self.initialize_walls()

    def format_map(self, map):
        map_array = [[] for i in range(len(map))]
        for i, string in enumerate(map):
            row = string.split()
            map_array[i] = row
        return map_array

    def create_key(self, x, y):
        return x, y + 1

    def create_home_key(self, x, y):
            return x + 12.5, y + 15

    def create_pellet_key(self, x, y):
        return x + 1, y + 1
    
    def create_wall_key(self, x, y):
        return x + 1, y + 1

    def fill_node_lut(self):
        for j, row in enumerate(self.map):
            for i, element in enumerate(row):
                if element == 'X':
                    key = self.create_key(i, j)
                    self.node_lut[key] = Node(*key)

    def connect_nodes(self):
        for j, row in enumerate(self.map):
            key = None
            for i, element in enumerate(row):
                if element == 'X':
                    if key is None:
                        key = self.create_key(i, j)
                    else:
                        other_key = self.create_key(i, j)
                        self.node_lut[key].adj[RIGHT] = self.node_lut[other_key]
                        self.node_lut[other_key].adj[LEFT] = self.node_lut[key]
                        key = other_key
                elif element != '—':
                    key = None
        for i, col in enumerate(list(zip(*self.map))):
            for j, element in enumerate(col):
                if element == 'X':
                    if key is None:
                        key = self.create_key(i, j)
                    else:
                        other_key = self.create_key(i, j)
                        self.node_lut[key].adj[DOWN] = self.node_lut[other_key]
                        self.node_lut[other_key].adj[UP] = self.node_lut[key]
                        key = other_key
                elif element != '|' and element != 'X':
                    key = None

    def connect_portal_pair(self, key1, key2):
        self.node_lut[key1].adj[PORTAL] = self.node_lut[key2]
        self.node_lut[key2].adj[PORTAL] = self.node_lut[key1]

    def add_pacman_node(self):
        pac_node = Node(14.5, 27)
        right = self.node_lut[(16, 27)]
        left = self.node_lut[(13, 27)]
        self.node_lut[(14.5, 27)] = pac_node
        pac_node.adj[RIGHT] = right
        pac_node.adj[LEFT] = left
        right.adj[LEFT] = pac_node
        left.adj[RIGHT] = pac_node

    def fill_home_node_lut(self):
        for j, row in enumerate(self.home_map):
            for i, element in enumerate(row):
                if element == 'X':
                    key = self.create_home_key(i, j)
                    self.node_lut[key] = Node(*key)

    def connect_home_nodes(self):
        for j, row in enumerate(self.home_map):
            key = None
            for i, element in enumerate(row):
                if element == 'X':
                    if key is None:
                        key = self.create_home_key(i, j)
                    else:
                        other_key = self.create_home_key(i, j)
                        self.node_lut[key].adj[RIGHT] = self.node_lut[other_key]
                        self.node_lut[other_key].adj[LEFT] = self.node_lut[key]
                        key = other_key
                elif element != '—':
                    key = None
        for i, col in enumerate(list(zip(*self.home_map))):
            for j, element in enumerate(col):
                if element == 'X':
                    if key is None:
                        key = self.create_home_key(i, j)
                    else:
                        other_key = self.create_home_key(i, j)
                        self.node_lut[key].adj[DOWN] = self.node_lut[other_key]
                        self.node_lut[other_key].adj[UP] = self.node_lut[key]
                        key = other_key
                elif element != '|' and element != 'X':
                    key = None

    def connect_home_to_rest(self):
        entrance = self.node_lut[(14.5, 15)]
        right = self.node_lut[(16, 15)]
        left = self.node_lut[(13, 15)]
        entrance.adj[RIGHT] = right
        entrance.adj[LEFT] = left
        right.adj[LEFT] = entrance
        left.adj[RIGHT] = entrance

    def fill_pellet_lut(self):
        for j, row in enumerate(self.pellet_map):
            for i, element in enumerate(row):
                if element == 'o':
                    key = self.create_pellet_key(i, j)
                    self.pellet_lut[key] = Pellet(*key)
                elif element == 'P':
                    key = self.create_pellet_key(i, j)
                    self.pellet_lut[key] = Pellet(*key, True)

    def initialize_walls(self):
        for j, str in enumerate(self.wall_map):
            for i, char in enumerate(str):
                if char != ' ':
                    r = self.wall_rotate_map[j][i]
                    key = self.create_wall_key(i, j)
                    self.walls.append(Wall(*key, char, r))

    def draw_nodes(self, screen):
        if self.node_lut is not None:
            for node in self.node_lut.values():
                node.draw(screen)

    def draw_pellets(self, screen):
        if self.pellet_lut is not None:
            for pellet in self.pellet_lut.values():
                pellet.draw(screen)

    def draw_grid(self, screen):
        for i in range(NUM_COLS + 1):
            pygame.draw.line(screen, (0, 100, 0), (i * TILE_SIZE, 0), (i * TILE_SIZE, SCREEN_SIZE[1]))
        for i in range(NUM_ROWS + 1):
            pygame.draw.line(screen, (0, 100, 0), (0, i * TILE_SIZE), (SCREEN_SIZE[0], i * TILE_SIZE))

    def draw_walls(self, screen):
        for wall in self.walls:
            wall.draw(screen)