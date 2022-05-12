import pygame
from constants import *
from entity import Pacman, Blinky, Inky, Pinky, Clyde
from map import Map
from vec2 import Vec2

# TODO: Pacman, die, positions reset
# TODO: Add Ghost graphics
# TODO: Add Pacman graphics
# TODO: Add scoring system
# TODO: Add text
# TODO: Add pellet graphicsw
# TODO: Fix ghost home height

# pygame
pygame.init()
pygame.display.set_caption('Pac-Man Clone')
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE)

# background
background = pygame.surface.Surface(SCREEN_SIZE).convert_alpha()
background.fill((12, 12, 12))

# maps
map = Map(map=GAME_MAP, home_map=GHOST_HOME_MAP, pellet_map=PELLET_MAP, wall_map=WALL_MAP, wall_rotate_map=WALL_ROTATE_MAP)
map.connect_portal_pair((0, 18), (29, 18))

# important nodes
home_nodes = [map.node_lut[(12.5, 17)], map.node_lut[(12.5, 18)], map.node_lut[(12.5, 19)], map.node_lut[(14.5, 18)], map.node_lut[(16.5, 17)], map.node_lut[(16.5, 18)], map.node_lut[(16.5, 19)]]
home_entrance = map.node_lut[(14.5, 15)]
home_center = map.node_lut[(14.5, 18)]

# entities
pacman = Pacman(map.node_lut[(14.5, 27)])
blinky = Blinky(map.node_lut[(14.5, 15)], pacman=pacman)
inky = Inky(map.node_lut[(12.5, 18)], pacman=pacman, blinky=blinky)
pinky = Pinky(map.node_lut[(14.5, 18)], pacman=pacman)
clyde = Clyde(map.node_lut[(16.5, 18)], pacman=pacman)
ghosts = [blinky, pinky, inky, clyde]
pacman.block_access(Vec2(14.5, 18))

score = 0
fright_timer = 0
     
def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            pass
    pacman.input()

def update():
    global fright_timer
    dt = clock.tick(60) / 1000.0
    if (fright_timer > 0):
        fright_timer -= dt
        print(fright_timer)
    else:
        fright_timer = 0

    set_ghost_states()
    check_collisions(dt)

    pacman.update(dt)
    for ghost in ghosts:
        ghost.update(dt)

def check_collisions(dt):
    global score, fright_timer
    for pellet in map.pellet_lut.values():
        if pacman.position.equals(pellet.position, dt * pacman.speed) and pellet.show == True:
            if pellet.power:
                score += 50
                fright_timer = 7
            else:
                score += 10
            increase_dot_count()
            pellet.show = False
            print(f'Score: {score}')
    for ghost in ghosts:
        if pacman.position.equals(ghost.position, dt * (pacman.speed + ghost.speed)):
            if ghost.state != FRIGHTENED and ghost.state != EATEN:
                print('DIE')
                pacman.die()
            else:
                print('ATE GHOST')
                ghost.set_state(EATEN)

def apply_states(state):
    for ghost in ghosts:
        ghost.set_state(state)

def increase_dot_count():
    for ghost in ghosts:
        ghost.increase_dot_count()

def set_ghost_states():
    if fright_timer > 0:
        apply_states(FRIGHTENED)
    elif pygame.time.get_ticks() / 1000.0 > 85:
        apply_states(CHASE)
    elif pygame.time.get_ticks() / 1000.0 > 79:
        apply_states(SCATTER)
    elif pygame.time.get_ticks() / 1000.0 > 59:
        apply_states(CHASE)
    elif pygame.time.get_ticks() / 1000.0 > 54:
        apply_states(SCATTER)
    elif pygame.time.get_ticks() / 1000.0 > 34:
        apply_states(CHASE)
    elif pygame.time.get_ticks() / 1000.0 > 27:
        apply_states(SCATTER)
    elif pygame.time.get_ticks() / 1000.0 > 7:
        apply_states(CHASE)
    elif pygame.time.get_ticks() / 1000.0 > 0:
        apply_states(SCATTER)

def draw():
    screen.blit(background, (0, 0))

    # map.draw_grid(screen)
    # map.draw_nodes(screen)
    map.draw_pellets(screen)
    map.draw_walls(screen)

    pacman.draw(screen)
    for ghost in ghosts:
        ghost.draw(screen)

while __name__ == '__main__':
    check_events()
    update()
    draw()
    pygame.display.update()