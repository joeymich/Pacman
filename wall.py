import pygame
from constants import *
from vec2 import Vec2

class Wall():
    def __init__(self, x, y, img_num, rotate):
        self.position = Vec2(x, y)
        self.img_num = img_num
        self.rotate = rotate
        image_source = 'assets/graphics/walls/wall' + str(img_num) + '.png'
        self.image = pygame.image.load(image_source).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * TILE_SIZE / 8, self.image.get_height() * TILE_SIZE / 8))
        if self.rotate != ' ':
            self.image = pygame.transform.rotate(self.image, 90 * int(rotate))
        self.rect = self.image.get_rect(center = self.position.tile_to_pixels_tuple())

    def draw(self, screen):
        screen.blit(self.image, self.rect)