import pygame
from spritesheet import GhostSprites
from vec2 import Vec2
from constants import *
from node import Node
import random
from support import import_folder

class Entity():
    def __init__(self, node=None):
        self.directions = {UP: Vec2(0, -1), DOWN: Vec2(0, 1), LEFT: Vec2(-1, 0), RIGHT: Vec2(1, 0)}
        self.color = WHITE
        self.start_node = node
        self.node = node
        self.target_node = node
        self.direction = self.directions[LEFT]
        self.blocked_tiles = []
        self.position = None
        if node is not None:
            self.position = node.get_tile()
        self.speed = 6
    def draw(self, screen):
        if self.position is not None:
            pygame.draw.circle(screen, self.color, self.position.tile_to_pixels_tuple(), TILE_SIZE * 3 / 4)

    def move(self, dt):
        if self.position is not None and self.direction is not None:
            self.position += self.direction * dt * self.speed

    def at_target(self):
        if self.node == self.target_node:
            return True
        return False

    def die(self):
        self.node = self.start_node
        self.target_node = self.start_node
        self.position = self.start_node.position

    def update(self, dt):
        self.pass_through()
        self.teleport()
        self.move(dt)
        self.reached_target()

    def reached_target(self):
        if (self.position - self.node.position).magnitude_squared() >= (self.target_node.position - self.node.position).magnitude_squared():
            self.node = self.target_node
            self.position = self.target_node.position

    def pass_through(self):
        if self.direction is not None:
            for key in self.node.adj:
                if key in self.directions:
                    if self.direction == self.directions[key] and self.node.adj[key] is not None:
                        self.target_node = self.node.adj[key]

    def teleport(self):
        if self.node.adj[PORTAL] is not None and self.position == self.node.position:
            self.node = self.node.adj[PORTAL]
            if self.node.adj[RIGHT] is not None:
                self.target_node = self.node.adj[RIGHT]
            if self.node.adj[LEFT] is not None:
                self.target_node = self.node.adj[LEFT]
            self.position = self.node.position

    def reverse_direction(self):
        if self.direction is not None:
            self.direction *= -1
            temp = self.target_node
            self.target_node = self.node
            self.node = temp

    def grant_access(self, tile):
        if tile in self.blocked_tiles:
            self.blocked_tiles.remove(tile)

    def block_access(self, tile):
        if tile not in self.blocked_tiles:
            self.blocked_tiles.append(tile)

class Pacman(Entity):
    def __init__(self, node=None):
        Entity.__init__(self, node=node)
        self.color = PACMAN_COLOR

    def update(self, dt):
        Entity.update(self, dt)

    def input(self):
        keys = pygame.key.get_pressed()
        key = None
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            key = UP
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            key = DOWN
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            key = LEFT
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            key = RIGHT
        if key is not None:
            if self.at_target():
                if self.node.adj[key] is not None and self.node.adj[key].position not in self.blocked_tiles:
                    self.node = self.target_node
                    self.target_node = self.node.adj[key]
                    self.direction = self.directions[key]
            else:
                if self.directions[key] == self.direction * -1:
                    self.reverse_direction()

class Ghost(Entity):
    def __init__(self, node=None):
        Entity.__init__(self, node=node)
        self.start_speed = self.speed
        self.corner = None
        self.target = None
        self.state = None
        self.dot_count = 0
        self.dot_limit = 0

        self.frame_index = 0
        self.animation_speed = 0.1

    def import_assets(self, path):
        self.animations = {'up': [], 'left': [], 'down': [], 'right': [], }
        for animation in self.animations:
            full_path = path + animation
            self.animations[animation] = import_folder(full_path, TILE_SIZE / 8)

    # Reverse directions when
        # chase -> scatter
        # chase -> frightened
        # scatter -> chase
        # scatter -> frightened

    def animate(self):
        if self.direction.y < 0:
            self.animation = 'up'
        elif self.direction.y > 0:
            self.animation = 'down'
        elif self.direction.x < 0:
            self.animation = 'left'
        elif self.direction.x > 0:
            self.animation = 'right'

        animation = self.animations[self.animation]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]

    def update(self, dt):
        Entity.update(self, dt)
        if self.in_home() and self.state != EATEN:
            if self.dot_count >= self.dot_limit:
                self.leave_home()
            else:
                self.stay_in_home()
            self.go_to_target()
        else:
            self.block_access(Vec2(14.5, 18))
            if self.state == SCATTER:
                self.scatter()
                self.go_to_target()
            elif self.state == CHASE:
                self.chase()
                self.go_to_target()
            elif self.state == FRIGHTENED:
                self.frightened()
            elif self.state == EATEN:
                self.eaten()
                self.go_to_target()
        if self.in_tunnel():
            self.speed = self.start_speed * 4 / 7.5
        self.animate()
        # self.sprites.update(dt)
    
    def move(self, dt):
        Entity.move(self, dt)
        if self.position is not None and self.direction is not None:
            self.rect.center = self.position.tile_to_pixels_tuple()

    def go_to_target(self):
        # set direction to shortest distance to target
        if self.target is not None:
            if self.at_target() and self.node.adj[PORTAL] is None:
                min = SCREEN_SIZE[1] ** 2
                direction = None
                if self.direction is not None:
                    for key in self.node.adj:
                        if self.node.adj[key] is not None and key in self.directions and self.directions[key] != self.direction * -1 and self.node.adj[key].position not in self.blocked_tiles:
                            distance = (self.target - (self.position + self.directions[key])).magnitude_squared()
                            if distance < min:
                                min = distance
                                direction = key
                if direction is not None:
                    self.node = self.target_node
                    self.target_node = self.node.adj[direction]
                    self.direction = self.directions[direction]
                else:
                    self.reverse_direction()

    def get_random_direction(self):
        if self.direction is not None:
            possible_directions = []
            if self.at_target() and self.node.adj[PORTAL] is None:
                for direction in self.directions:
                    if self.node.adj[direction] is not None and self.directions[direction] != self.direction * -1:
                        possible_directions.append(self.directions[direction])
            if possible_directions != []:
                self.node = self.target_node
                self.target_node = self.node.adj[direction]
                self.direction = random.choice(possible_directions)

    def stay_in_home(self):
        if self.at_target():
            if self.node.adj[UP] is None or self.node.adj[DOWN] is None:
                self.reverse_direction()

    def in_home(self):
        if self.position.x > 11 and self.position.x < 18 and self.position.y > 16 and self.position.y < 20:
            return True
        return False

    def in_tunnel(self):
        if self.node is not None and self.target_node is not None:
            if self.node.adj[PORTAL] is not None or self.target_node.adj[PORTAL] is not None:
                return True
        return False

    def leave_home(self):
        if self.position.x != 18:
            self.target = Vec2(14.5, 18)
        else:
            self.target = Vec2(14.5, 15)
                
    def set_state(self, state):
        if self.state != EATEN:
            if not self.in_home() and state != EATEN and ((self.state == CHASE and state != CHASE) or (self.state == SCATTER and state != SCATTER)):
                self.reverse_direction()
            self.state = state

    def eaten(self):
        self.speed = self.start_speed * 1.5
        self.grant_access(Vec2(14.5, 18))
        if self.position != Vec2(14.5, 15):
            self.target = Vec2(14.5, 15)
        else:
            self.target = Vec2(14.5, 18)
        if self.position == Vec2(14.5, 18):
            self.reverse_direction()
        if self.position == Vec2(14.5, 15) and self.direction == self.directions[UP]:
            self.state = SCATTER

    def scatter(self):
        # 1. target corner position
        # self.block_access_home_nodes()
        self.speed = self.start_speed
        self.target = self.corner

    def chase(self):
        # 1. follow ghost-specific target
        # self.block_access_home_nodes()'
        self.speed = self.start_speed

    def frightened(self):
        # 1. move randomly at 0.5 speed
        self.speed = self.start_speed * 2 / 3
        self.get_random_direction()

    def increase_dot_count(self):
        self.dot_count += 1

    def draw(self, screen):
        if self.image is None:
            Entity.draw(self, screen)
        else:
            screen.blit(self.image, self.rect)
        if self.target is not None:
            node = Node(*self.target.as_tuple(), color=self.color)
            node.draw(screen)

class Blinky(Ghost):
    def __init__(self, node=None, pacman=None):
        Ghost.__init__(self, node=node)
        self.name = BLINKY
        self.pacman = pacman
        self.color = BLINKY_COLOR
        self.corner = Vec2(26, 2)
        self.import_assets('assets/graphics/ghosts/blinky/')
        self.image = self.animations['left'][0]
        self.rect = self.image.get_rect(center = self.position.tile_to_pixels_tuple())
        # self.sprites = GhostSprites(self)

    def chase(self):
        Ghost.chase(self)
        self.target = self.pacman.position

class Inky(Ghost):
    def __init__(self, node=None, pacman=None, blinky=None):
        Ghost.__init__(self, node=node)
        self.name = INKY
        self.pacman = pacman
        self.blinky = blinky
        self.color = INKY_COLOR
        self.direction = self.directions[DOWN]
        self.corner = Vec2(28, 35)
        self.dot_limit = 30
        self.import_assets('assets/graphics/ghosts/inky/')
        self.image = self.animations['left'][0]
        self.rect = self.image.get_rect(center = self.position.tile_to_pixels_tuple())
        # self.sprites = GhostSprites(self)

    def chase(self):
        Ghost.chase(self)
        temp = self.pacman.position + self.pacman.direction * 2
        if self.pacman.direction == self.pacman.directions[UP]:
            temp += self.pacman.directions[LEFT] * 2
        self.target = self.blinky.position + (temp - self.blinky.position) * 2

class Pinky(Ghost):
    def __init__(self, node=None, pacman=None):
        Ghost.__init__(self, node=node)
        self.name = PINKY
        self.pacman = pacman
        self.color = PINKY_COLOR
        self.direction = self.directions[UP]
        self.corner = Vec2(3, 2)
        self.import_assets('assets/graphics/ghosts/pinky/')
        self.image = self.animations['left'][0]
        self.rect = self.image.get_rect(center = self.position.tile_to_pixels_tuple())
        # self.sprites = GhostSprites(self)

    def chase(self):
        Ghost.chase(self)
        self.target = self.pacman.position + self.pacman.direction * 4
        if self.pacman.direction == self.pacman.directions[UP]:
            self.target += self.pacman.directions[LEFT] * 4

class Clyde(Ghost):
    def __init__(self, node=None, pacman=None):
        Ghost.__init__(self, node=node)
        self.name = CLYDE
        self.pacman = pacman
        self.color = CLYDE_COLOR
        self.direction = self.directions[DOWN]
        self.corner = Vec2(1, 35)
        self.dot_limit = 90
        self.import_assets('assets/graphics/ghosts/clyde/')
        self.image = self.animations['left'][0]
        self.rect = self.image.get_rect(center = self.position.tile_to_pixels_tuple())
        # self.sprites = GhostSprites(self)

    def chase(self):
        Ghost.chase(self)
        if (self.pacman.position - self.position).magnitude_squared() > 8 ** 2:
            self.target = self.pacman.position
        else:
            self.target = self.corner