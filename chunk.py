from block import Block
from random import randrange

class Chunk():
    def __init__(self):
        self.loaded = False
        self.blocks = None

    def draw(self, screen, player_position):
        if self.loaded:
            for i in range(len(self.blocks)):
                for j in range(len(self.blocks[i])):
                    self.blocks[i][j].draw(screen, (i * 16 - player_position[0], j * 16 - player_position[1]))

    def update(self):
        pass

    def load(self):
        self.generate()
        self.loaded = True

    def unload(self):
        self.blocks = None
        self.loaded = False

    def generate(self):
        self.blocks = [[Block(randrange(2)) for i in range(16)] for j in range(16)]