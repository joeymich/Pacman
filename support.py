import pygame
from os import walk

def import_folder(path, scale_factor):
    surface_list = []

    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            image_surf = pygame.transform.scale(image_surf, (image_surf.get_width() * scale_factor, image_surf.get_height() * scale_factor))
            surface_list.append(image_surf)
    return surface_list