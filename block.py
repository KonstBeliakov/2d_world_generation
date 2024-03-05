import pygame
from settings import *

textures_files = ['dirt.png', 'sand.png', 'grass.png', 'stone.png', None, 'depth_stone.png', 'log.png', 'leaves.png']

textures = [pygame.image.load(f'textures/{file}') if file else None for file in textures_files]


class Block():
    def __init__(self, block_type):
        self.type = block_type

    def draw(self, screen, pos):
        if self.type != AIR:
            screen.blit(textures[self.type], pos)