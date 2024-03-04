import pygame
from settings import *

textures_files = ['dirt.png', 'sand.png', 'grass.png', 'stone.png', None]

textures = [pygame.image.load(file) for file in textures_files if file]


class Block():
    def __init__(self, block_type):
        self.type = block_type

    def draw(self, screen, pos):
        if self.type != AIR:
            screen.blit(textures[self.type], pos)