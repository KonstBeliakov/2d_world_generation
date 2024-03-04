from block import Block
from random import randrange


BLOCK_SIZE = 16
CHUNK_SIZE = 16

class Chunk():
    def __init__(self):
        self.loaded = False
        self.blocks = None

    def draw(self, screen, chunk_position, player_position):
        if self.loaded:
            for i in range(len(self.blocks)):
                for j in range(len(self.blocks[i])):
                    self.blocks[i][j].draw(screen,
                                           (i * BLOCK_SIZE - player_position[0] * BLOCK_SIZE + chunk_position[0] * CHUNK_SIZE * BLOCK_SIZE,
                                            j * BLOCK_SIZE - player_position[1] * BLOCK_SIZE + chunk_position[1] * CHUNK_SIZE * BLOCK_SIZE))

    def update(self):
        pass

    def load(self):
        self.generate()
        self.loaded = True

    def unload(self):
        self.blocks = None
        self.loaded = False

    def generate(self):
        self.blocks = [[Block(randrange(2)) for i in range(CHUNK_SIZE)] for j in range(CHUNK_SIZE)]
