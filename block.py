import pygame

textures_files = ['dirt.png', 'sand.png']
textures = [pygame.image.load(file) for file in textures_files]


class Block():
    def __init__(self, block_type):
        self.type = block_type

    def draw(self, screen, pos):
        screen.blit(textures[self.type], pos)