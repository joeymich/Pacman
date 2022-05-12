import pygame
from vec2 import Vec2
from constants import *

class Pellet():
    def __init__(self, x, y, power=False):
        self.position = Vec2(x, y)
        self.show = True
        self.power = power

    def draw(self, screen):
        if self.show:
            if self.power:
                pygame.draw.circle(screen, WHITE, self.position.tile_to_pixels_tuple(), TILE_SIZE / 2)
            else:
                rect = pygame.Rect(0, 0, TILE_SIZE / 4, TILE_SIZE / 4)
                rect.center = self.position.tile_to_pixels_tuple()
                pygame.draw.rect(screen, WHITE, rect)
                # pygame.draw.circle(screen, WHITE, self.position.tile_to_pixels_tuple(), 4)