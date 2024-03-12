import copy
import random
from random import randrange

import pygame
from settings import *
from utils import *
from chunk import Chunk
from perlin_noise import PerlinNoise


class v2:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class World():
    def __init__(self):
        self.chunks = {(i, j): Chunk() for i in range(2) for j in range(2)}
        for chunk_pos, chunk in self.chunks.items():
            chunk.load(*chunk_pos)
        self.seed = 0
        self.noiseGenerator = PerlinNoise()

    def draw(self, screen, player_position):
        for i in range(int(player_position[0] // CHUNK_SIZE - GENERATION_DISTANSE),
                       int(player_position[0] // CHUNK_SIZE + GENERATION_DISTANSE)):
            for j in range(int(player_position[1] // CHUNK_SIZE - GENERATION_DISTANSE),
                           int(player_position[1] // CHUNK_SIZE + GENERATION_DISTANSE)):
                # loading
                if (i, j) not in self.chunks:
                    self.chunks[(i, j)] = Chunk()
                    self.chunks[(i, j)].load(i, j)
                # pre-generating
                if not self.chunks[(i, j)].generated:
                    self.generate((i, j))

        # generating structures

        for i in range(int(player_position[0] // CHUNK_SIZE - LOAD_DISTANSE),
                       int(player_position[0] // CHUNK_SIZE + LOAD_DISTANSE)):
            for j in range(int(player_position[1] // CHUNK_SIZE - LOAD_DISTANSE),
                           int(player_position[1] // CHUNK_SIZE + LOAD_DISTANSE)):
                if dist((i, j), (player_position[0] // CHUNK_SIZE, player_position[1] // CHUNK_SIZE)) <= LOAD_DISTANSE:
                    if not self.chunks[(i, j)].loaded:
                        self.structures_generate((i, j))

        # unloading
        t = []
        for chunk_position, chunk in self.chunks.items():
            if dist(chunk_position,
                    (player_position[0] // CHUNK_SIZE, player_position[1] // CHUNK_SIZE)) > GENERATION_DISTANSE:
                t.append(chunk_position)
        for i in t:
            self.chunks[i].unload(*i)
            del self.chunks[i]

        # drawing

        for chunk_position, chunk in self.chunks.items():
            if dist(chunk_position,
                    (player_position[0] // CHUNK_SIZE, player_position[1] // CHUNK_SIZE)) <= DRAW_DISTANSE:
                chunk.update()
                if chunk.generated:
                    chunk.draw(screen, chunk_position, player_position)
                else:
                    print('not generated:', chunk_position)

    def generate(self, chunk_position):
        if chunk_position not in self.chunks:
            self.chunks[chunk_position] = Chunk()
        if not self.chunks[chunk_position].generated:
            self.chunks[chunk_position].load(*chunk_position)
        if not self.chunks[chunk_position].generated:
            random.seed(self.seed)
            height = [self.noiseGenerator(i * 0.05) // 0.1 for i in
                      range(chunk_position[0] * CHUNK_SIZE, (chunk_position[0] + 1) * CHUNK_SIZE)]
            random.seed(self.seed + chunk_position[0] * 10 ** 6 + chunk_position[1])
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
        self.chunks[chunk_position].unload(*chunk_position)

    def structures_generate(self, chunk_position):
        if not self.chunks[chunk_position].generated:
            self.generate(chunk_position)
        position = (chunk_position[0] * CHUNK_SIZE, chunk_position[1] * CHUNK_SIZE)
        self.setblock(position, NONE)
        for i in range(CHUNK_SIZE):
            for j in range(CHUNK_SIZE):
                position = (chunk_position[0] * CHUNK_SIZE + i, chunk_position[1] * CHUNK_SIZE + j)
                if self.chunks[chunk_position].blocks[i][j].type == GRASS and self.chunks[chunk_position].blocks[i][
                    j - 1].type == AIR:
                    if randrange(100) < 10:
                        self.tree(position)
                if self.chunks[chunk_position].blocks[i][j].type in [STONE, DEPTH_STONE]:
                    if randrange(10000) < 7:
                        print('cave', position)
                        self.cave(position)
        self.chunks[chunk_position].genereted = True
        self.chunks[chunk_position].loaded = True
        self.chunks[chunk_position].unload(*chunk_position)

    def setblock(self, position, block_type):
        chunk_pos = (position[0] // CHUNK_SIZE, position[1] // CHUNK_SIZE)
        if chunk_pos not in self.chunks:
            self.chunks[chunk_pos] = Chunk()
            self.chunks[chunk_pos].load(*chunk_pos)
        if not self.chunks[chunk_pos].generated:
            self.generate(chunk_pos, structures=False)
        self.chunks[chunk_pos].blocks[position[0] % CHUNK_SIZE][position[1] % CHUNK_SIZE].type = block_type

    def getblock(self, x, y):
        chunk_pos = (x // CHUNK_SIZE, y // CHUNK_SIZE)
        if chunk_pos not in self.chunks:
            self.chunks[chunk_pos] = Chunk()
            self.chunks[chunk_pos].load(*chunk_pos)
        if not self.chunks[chunk_pos].generated:
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

    def cave(self, position):
        n = 400
        l = [[False] * n for _ in range(n)]

        p_now = v2(n // 2, n // 2)
        d = 3
        iteration = 75

        # generation

        for i in range(iteration):
            for x in range(max(0, int(p_now.x) - d), min(n - 1, int(p_now.x) + d + 1)):
                for y in range(max(0, int(p_now.y) - d), min(n - 1, int(p_now.y) + d + 1)):
                    l[x][y] = True
            match randrange(4):
                case 0:
                    p_now.x += d
                case 1:
                    p_now.x -= d
                case 2:
                    p_now.y += 1.3 * d
                case 3:
                    p_now.y -= d

        # smoothing corners
        l2 = copy.deepcopy(l)

        for i in range(1, len(l) - 1):
            for j in range(1, len(l[i]) - 1):
                t = l[i - 1][j] + l[i + 1][j] + l[i][j + 1] + l[i][j - 1]

                if t == 2:
                    l2[i][j] = False
                elif t == 3:
                    l2[i][j] = bool(randrange(2))

        for i in range(n):
            for j in range(n):
                if l2[i][j]:
                    self.setblock((position[0] + i - n // 2, position[1] + j - n // 2), AIR)
