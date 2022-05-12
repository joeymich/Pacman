import pygame
from constants import *

BASETILEWIDTH = 24
BASETILEHEIGHT = 24

class Spritesheet():
    def __init__(self):
        self.sheet = pygame.image.load('assets/graphics/ghosts/ghosts.png').convert_alpha()
        width = int(self.sheet.get_width() * SCALE_FACTOR)
        height = int(self.sheet.get_height() * SCALE_FACTOR)
        self.sheet = pygame.transform.scale(self.sheet, (width, height))

    def get_image(self, x, y, width, height):
        x *= 16 * SCALE_FACTOR
        y *= 16 * SCALE_FACTOR
        self.sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())

class GhostSprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.x = {BLINKY: 0, PINKY: 2, INKY: 4, CLYDE: 6}
        self.entity = entity
        self.entity.image = self.get_start_image()

        self.frame_index = 0
        self.animation_speed = 0.1

    def get_start_image(self):
        return self.get_image(self.x[self.entity.name], 0)

    def get_image(self, x, y):
        return Spritesheet.get_image(self, x, y, 16*SCALE_FACTOR, 16*SCALE_FACTOR)

    def update(self, dt):
        x = self.x[self.entity.name]
        y = 0

        if self.entity.direction.y < 0:
            y = 0
        elif self.entity.direction.x < 0:
            y = 1
        elif self.entity.direction.y > 0:
            y = 2
        elif self.entity.direction.x > 0:
            y = 3

        if self.entity.state in [SCATTER, CHASE]:
            x += int(self.frame_index)
            self.frame_index += self.animation_speed * dt * FPS
            if self.frame_index >= 2:
                self.frame_index = 0
        elif self.entity.state == EATEN:
            x = 8
        elif self.entity.state == FRIGHTENED:
            y = int(self.frame_index)
            x = 9

            self.frame_index += self.animation_speed * dt * FPS
            # if self.entity.mode.timer >= 5:
            #     if self.frame_index >= 4:
            #         self.frame_index = 0
            # else:
            if self.frame_index >= 2:
                self.frame_index = 0
            
        self.entity.image = self.get_image(x, y)

# class PacManSprites(Spritesheet):
#     def __init__(self, entity):
#         Spritesheet.__init__(self)
#         self.entity = entity
#         self.entity.image = self.get_start_image()

#         self.frame_index = 0
#         self.animation_speed = 0.2

#     def get_start_image(self):
#         return self.get_image(10, 1)

#     def get_image(self, x, y):
#         return Spritesheet.get_image(self, x, y, 16*SCALE_FACTOR, 16*SCALE_FACTOR)

#     def update(self, dt):
#         x = 10
#         y = int(self.frame_index)

#         if y == 3:
#             y = 1

#         self.frame_index += self.animation_speed * dt * FPS
#         if self.frame_index >= 4:
#             self.frame_index = 0

#         self.entity.image = self.get_image(x, y)
#         if self.entity.direction == LEFT:
#             self.entity.image = pygame.transform.rotate(self.entity.image, 90)
#         elif self.entity.direction == DOWN:
#             self.entity.image = pygame.transform.rotate(self.entity.image, 180)
#         elif self.entity.direction == RIGHT:
#             self.entity.image = pygame.transform.rotate(self.entity.image, 270)

# class MazeSprites():
#     def __init__(self):
#         self.wall_data = maze
#         self.rotate_data = wall_rotate

#     def construct_background(self, background):
#         for i, str in enumerate(maze):
#             for j, c in enumerate(str):
#                 if c == '0' or c == '1' or c == '2' or c == '3' or c == '4' or c == '5' or c == '6' or c == '7' or c == '8' or c == '9' or c == 'w':
#                     r = wall_rotate[i][j]
#                     self.center = (j * TILEWIDTH, i * TILEHEIGHT)
#                     image_source = 'graphics/walls/wall' + c + '.png'
#                     sprite = pygame.image.load(image_source).convert_alpha()
#                     sprite = pygame.transform.scale(sprite, (sprite.get_width() * SCALE_FACTOR, sprite.get_height() * SCALE_FACTOR))
#                     if r != ' ':
#                         sprite = pygame.transform.rotate(sprite, 90 * int(r))
#                     self.rect = sprite.get_rect(center = self.center)
#                     background.blit(sprite, (j * TILEWIDTH - TILEWIDTH/2, i * TILEHEIGHT - TILEHEIGHT/2))

#         return background
    