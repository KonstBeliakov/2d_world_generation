import pickle

import pygame

from block import Block
from random import randrange
from settings import *


class Chunk():
    def __init__(self):
        self.loaded = False
        self.generated = False
        self.blocks = None

    def draw(self, screen, chunk_position, player_position):
        if self.loaded:
            for i in range(len(self.blocks)):
                for j in range(len(self.blocks[i])):
                    self.blocks[i][j].draw(screen,
                                           (SCREEN_SENTER[0] + i * BLOCK_SIZE - player_position[0] * BLOCK_SIZE +
                                            chunk_position[0] * CHUNK_SIZE * BLOCK_SIZE,
                                            SCREEN_SENTER[1] + j * BLOCK_SIZE - player_position[1] * BLOCK_SIZE +
                                            chunk_position[1] * CHUNK_SIZE * BLOCK_SIZE))

    def update(self):
        pass

    def load(self, x, y):
        if not self.loaded:
            try:
                with open(f'world/{x} {y}', 'rb') as file:
                    self.blocks = pickle.load(file)
            except:
                self.generate()
            else:
                self.loaded = True

    def unload(self, x, y):
        with open(f'world/{x} {y}', 'wb') as file:
            pickle.dump(self.blocks, file)

        self.blocks = None
        self.loaded = False

    def generate(self):
        self.blocks = [[Block(AIR) for i in range(CHUNK_SIZE)] for j in range(CHUNK_SIZE)]


if __name__ == '__main__':
    chunk = Chunk()
    chunk.load(0, 1)
    chunk.unload(0, 1)
    chunk.load(0, 1)

    pygame.init()
    window_size = (800, 800)
    pygame.display.set_caption("Main window")
    screen = pygame.display.set_mode(window_size)
    background_color = (100, 200, 255)
    screen.fill(background_color)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill(background_color)

        chunk.draw(screen, (0, 0), (0, 0))

        pygame.display.flip()