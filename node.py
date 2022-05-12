import pygame
from vec2 import Vec2
from constants import *

class Node():
    def __init__(self, x, y, color=None):
        self.position = Vec2(x, y)
        self.adj = {UP: None, DOWN: None, LEFT: None, RIGHT: None, PORTAL: None}
        if color is None:
            self.color = RED
        else:
            self.color = color

    def get_tile(self):
        return self.position

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position.tile_to_pixels_tuple(), TILE_SIZE * 5 / 12)
        for key in self.adj:
            if self.adj[key] is not None and key != PORTAL:
                pygame.draw.line(screen, WHITE, self.position.tile_to_pixels_tuple(), self.adj[key].position.tile_to_pixels_tuple())