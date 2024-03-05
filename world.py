import random
from random import randrange

import pygame
from settings import *
from utils import *
from chunk import Chunk
from perlin_noise import PerlinNoise


class World():
    def __init__(self):
        self.chunks = {(i, j): Chunk() for i in range(2) for j in range(2)}
        for chunk in self.chunks.values():
            chunk.load()
        self.seed = 0
        self.noiseGenerator = PerlinNoise()

    def draw(self, screen, player_position):
        for i in range(int(player_position[0] // CHUNK_SIZE - LOAD_DISTANSE),
                       int(player_position[0] // CHUNK_SIZE + LOAD_DISTANSE)):
            for j in range(int(player_position[1] // CHUNK_SIZE - LOAD_DISTANSE),
                           int(player_position[1] // CHUNK_SIZE + LOAD_DISTANSE)):

                if dist((i, j), (player_position[0] // CHUNK_SIZE, player_position[1] // CHUNK_SIZE)) <= LOAD_DISTANSE:
                    if (i, j) not in self.chunks:
                        self.chunks[(i, j)] = Chunk()
                    self.chunks[(i, j)].load()
                    if not self.chunks[(i, j)].loaded:
                        self.generate((i, j), structures=True)
        t = []
        for chunk_position, chunk in self.chunks.items():
            if dist(chunk_position,
                    (player_position[0] // CHUNK_SIZE, player_position[1] // CHUNK_SIZE)) > LOAD_DISTANSE:
                t.append(chunk_position)

            chunk.update()
            chunk.draw(screen, chunk_position, player_position)

        for i in t:
            del self.chunks[i]

        #print(f'chunks loaded: {len(self.chunks)}')

    def generate(self, chunk_position, structures=False):
        if chunk_position not in self.chunks:
            self.chunks[chunk_position] = Chunk()
        if not self.chunks[chunk_position].generated:
            self.chunks[chunk_position].generate()
            random.seed(self.seed)
            height = [self.noiseGenerator(i * 0.05) // 0.1 for i in range(chunk_position[0] * CHUNK_SIZE, (chunk_position[0] + 1) * CHUNK_SIZE)]
            random.seed(self.seed + chunk_position[0] * 10**6 + chunk_position[1])
            for i in range(CHUNK_SIZE):
                for j in range(CHUNK_SIZE):
                    j2 = j + CHUNK_SIZE * chunk_position[1]
                    if j2 < height[i]:
                        block = AIR
                    elif j2 == height[i]:
                        block = GRASS
                    elif j2 < height[i] + random.randint(3, 5):
                        block = DIRT
                    elif j2 < 16:
                        block = STONE
                    elif j2 < 22:
                        block = DEPTH_STONE if (randrange(100) < [10, 25, 40, 60, 75, 90][j2 - 16]) else STONE
                    else:
                        block = DEPTH_STONE
                    self.chunks[chunk_position].blocks[i][j].type = block
            self.chunks[chunk_position].generated = True
        if structures:
            self.structures_generate(chunk_position)
            self.chunks[chunk_position].loaded = True

    def structures_generate(self, chunk_position):
        for i in range(CHUNK_SIZE):
            for j in range(CHUNK_SIZE):
                if self.chunks[chunk_position].blocks[i][j].type == GRASS and self.chunks[chunk_position].blocks[i][j - 1].type == AIR:
                    if randrange(100) < 10:
                        self.tree((chunk_position[0] * CHUNK_SIZE + i, chunk_position[1] * CHUNK_SIZE + j))

    def setblock(self, position, block_type):
        chunk_pos = (position[0] // CHUNK_SIZE, position[1] // CHUNK_SIZE)
        if chunk_pos not in self.chunks:
            self.generate(chunk_pos, structures=False)
        self.chunks[chunk_pos].blocks[position[0] % CHUNK_SIZE][position[1] % CHUNK_SIZE].type = block_type

    def getblock(self, x, y):
        chunk_pos = (x // CHUNK_SIZE, y // CHUNK_SIZE)
        if chunk_pos not in self.chunks:
            self.generate(chunk_pos, structures=False)
        return self.chunks[chunk_pos].blocks[x % CHUNK_SIZE][y % CHUNK_SIZE].type

    def tree(self, position):
        tree_height = random.randint(4, 6)
        for j in range(position[1] - tree_height, position[1]):
            self.setblock((position[0], j), LOG)

        for i in range(position[0] - 2, position[0] + 3):
            for j in range(position[1] - tree_height - 2, position[1] - tree_height + 2):
                if self.getblock(i, j) != LOG:
                    self.setblock((i, j), LEAVES)

        self.setblock((position[0] - 2, position[1] - tree_height - 2), AIR)
        self.setblock((position[0] + 2, position[1] - tree_height - 2), AIR)
