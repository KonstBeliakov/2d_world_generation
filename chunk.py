from block import Block
from random import randrange
from settings import *


class Chunk():
    def __init__(self):
        self.loaded = False
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

    def load(self):
        if not self.loaded:
            self.generate()
            #self.loaded = True

    def unload(self):
        self.blocks = None
        self.loaded = False

    def generate(self):
        self.blocks = [[Block(AIR) for i in range(CHUNK_SIZE)] for j in range(CHUNK_SIZE)]
