import pickle

import pygame

from block import Block, textures
from random import randrange
from settings import *


class Chunk():
    def __init__(self):
        self.loaded = False
        self.generated = False
        self.blocks = [[Block(NONE) for i in range(CHUNK_SIZE)] for j in range(CHUNK_SIZE)]

    def draw(self, screen, chunk_position, player_position):
        for i in range(len(self.blocks)):
                for j in range(len(self.blocks[i])):
                    block_position = (SCREEN_SENTER[0] + i * BLOCK_SIZE - player_position[0] * BLOCK_SIZE +
                                            chunk_position[0] * CHUNK_SIZE * BLOCK_SIZE,
                                            SCREEN_SENTER[1] + j * BLOCK_SIZE - player_position[1] * BLOCK_SIZE +
                                            chunk_position[1] * CHUNK_SIZE * BLOCK_SIZE)
                    if -BLOCK_SIZE < block_position[0] < SCREEN_SIZE[0] and -BLOCK_SIZE < block_position[1] < SCREEN_SIZE[1]:
                        self.blocks[i][j].draw(screen, block_position)

    def update(self):
        pass

    def load(self, x, y):
        if not self.loaded:
            try:
                with open(f'{WORLD_FOLDER_NAME}/{x} {y}.txt', 'r', encoding='utf-8') as file:
                    self.generated = bool(int(file.readline()))
                    self.loaded = bool(int(file.readline()))

                    for i, line in enumerate(file.readlines()):
                        for j, block_type in enumerate(line.split()):
                            self.blocks[i][j].type = int(block_type)
                #with open(f'world/{x} {y}', 'rb') as file:
                #    self.generated, self.loaded, self.blocks = pickle.load(file)
            except:
                pass

    def unload(self, x, y):
        if self.generated:
            with open(f'{WORLD_FOLDER_NAME}/{x} {y}.txt', 'w', encoding='utf-8') as file:
                file.write(str(int(self.generated)) + '\n')
                file.write(str(int(self.loaded)) + '\n')

                file.write('\n'.join([' '.join([str(block.type) for block in line]) for line in self.blocks]))
            #with open(f'world/{x} {y}', 'wb') as file:
            #    pickle.dump([self.generated, self.loaded, self.blocks], file)


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
