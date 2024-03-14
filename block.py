from settings import *


class Block():
    def __init__(self, block_type):
        self.type = block_type

    def draw(self, screen, pos):
        try:
            if self.type != AIR:
                screen.blit(textures[self.type], pos)
        except:
            raise ValueError(str(self.type))