import pygame
import numpy as np
from settings import *

textures_files = ['dirt.png', 'sand.png', 'grass.png', 'stone.png', None, 'depth_stone.png', 'log.png', 'leaves.png',
                  'none.png', 'iron_ore.png', 'coal_ore.png', 'depth_coal_ore.png', 'depth_iron_ore.png',
                  'grass_block.png', 'dense_depth_stone.png', 'reddish_stone.png', 'hell_stone.png',
                  'magma.png', 'hell_star_ore.png', 'rich_hell_star_ore.png', 'poor_hell_star_ore.png']

textures = [pygame.image.load(f'textures/{file}') if file else None for file in textures_files]


class Block():
    def __init__(self, block_type):
        self.type = block_type

    def draw(self, screen, pos):
        try:
            if self.type != AIR:
                screen.blit(textures[self.type], pos)
        except:
            raise ValueError(str(self.type))