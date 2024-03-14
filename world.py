import random

from settings import *
import settings
from utils import *
from chunk import Chunk
from perlin_noise import PerlinNoise
from time import perf_counter
import structures


class World():
    def __init__(self):
        self.chunks = {(i, j): Chunk() for i in range(2) for j in range(2)}
        for chunk_pos, chunk in self.chunks.items():
            chunk.load(*chunk_pos)
        self.seed = settings.WORLD_SEED
        self.noiseGenerator = PerlinNoise()
        self.time = perf_counter()
        self.temp = 0
        self.prev_player_position = None
        self.t = 0

    def update(self, player_position):
        moved = self.prev_player_position is None or \
                (player_position[0] // CHUNK_SIZE != self.prev_player_position[0] // CHUNK_SIZE or
                 player_position[1] // CHUNK_SIZE != self.prev_player_position[1] // CHUNK_SIZE)
        self.prev_player_position = player_position

        if moved:
            t = perf_counter()
            for i in range(int(player_position[0] // CHUNK_SIZE - settings.GENERATION_DISTANSE),
                           int(player_position[0] // CHUNK_SIZE + settings.GENERATION_DISTANSE)):
                for j in range(int(player_position[1] // CHUNK_SIZE - settings.GENERATION_DISTANSE),
                               int(player_position[1] // CHUNK_SIZE + settings.GENERATION_DISTANSE)):
                    # loading
                    if (i, j) not in self.chunks:
                        self.chunks[(i, j)] = Chunk()
                        self.chunks[(i, j)].load(i, j)
                    # pre-generating
                    if not self.chunks[(i, j)].generated:
                        self.generate((i, j))
            print('loading:', perf_counter() - t, end=' ')

            # generating structures
            t = perf_counter()
            for i in range(int(player_position[0] // CHUNK_SIZE - settings.LOAD_DISTANSE),
                           int(player_position[0] // CHUNK_SIZE + settings.LOAD_DISTANSE)):
                for j in range(int(player_position[1] // CHUNK_SIZE - settings.LOAD_DISTANSE),
                               int(player_position[1] // CHUNK_SIZE + settings.LOAD_DISTANSE)):
                    if dist((i, j),
                            (player_position[0] // CHUNK_SIZE, player_position[1] // CHUNK_SIZE)) <= settings.LOAD_DISTANSE:
                        if not self.chunks[(i, j)].loaded:
                            self.structures_generate((i, j))

            print('generating:', perf_counter() - t, end=' ')

            # unloading
            t2 = perf_counter()
            t = []
            for chunk_position, chunk in self.chunks.items():
                if dist(chunk_position,
                        (player_position[0] // CHUNK_SIZE, player_position[1] // CHUNK_SIZE)) > settings.GENERATION_DISTANSE:
                    t.append(chunk_position)
            for i in t:
                self.chunks[i].unload(*i)
                del self.chunks[i]

            print('unloading:', perf_counter() - t2, end=' ')

    def draw(self, screen, player_position):
        for chunk_position, chunk in self.chunks.items():
            if abs(chunk_position[0] - player_position[0] // CHUNK_SIZE) <= settings.DRAW_DISTANSE_X and \
                    abs(chunk_position[1] - player_position[1] // CHUNK_SIZE) <= settings.DRAW_DISTANSE_Y:
                chunk.update()
                chunk.draw(screen, chunk_position, player_position)

        self.t += 1

        if self.t % 10 == 0:
            print('fps:', 10 / (perf_counter() - self.time))
            self.time = perf_counter()

    def generate(self, chunk_position):
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
                    elif j2 < DEPTH_STONE_LEVEL:
                        block = STONE
                    elif j2 < DEPTH_STONE_LEVEL + len(DEPTH_STONE_PROBABILITY):
                        block = DEPTH_STONE if (
                                randrange(100) < DEPTH_STONE_PROBABILITY[j2 - DEPTH_STONE_LEVEL]) else STONE
                    elif j2 < REDDISH_STONE_LEVEL:
                        block = DEPTH_STONE
                    elif j2 < REDDISH_STONE_LEVEL + len(REDDISH_STONE_PROBABILITY):
                        block = REDDISH_STONE if randrange(100) < REDDISH_STONE_PROBABILITY[
                            j2 - REDDISH_STONE_LEVEL] else DEPTH_STONE
                    elif j2 < HELL_STONE_LEVEL:
                        block = REDDISH_STONE
                    elif j2 < HELL_STONE_LEVEL + len(HELL_STONE_PROBABILITY):
                        block = HELL_STONE if randrange(100) < HELL_STONE_PROBABILITY[
                            j2 - HELL_STONE_LEVEL] else REDDISH_STONE
                    else:
                        block = HELL_STONE
                    self.chunks[chunk_position].blocks[i][j].type = block
            self.chunks[chunk_position].generated = True
        self.chunks[chunk_position].unload(*chunk_position)

    def structures_generate(self, chunk_position):
        for i in range(CHUNK_SIZE):
            for j in range(CHUNK_SIZE):
                position = (chunk_position[0] * CHUNK_SIZE + i, chunk_position[1] * CHUNK_SIZE + j)
                if self.chunks[chunk_position].blocks[i][j].type == GRASS and self.chunks[chunk_position].blocks[i][
                    j - 1].type == AIR:
                    if randrange(100) < 10:
                        structures.tree(self, position)
                    if randrange(100) < 30:
                        self.setblock(position, GRASS_BLOCK)
                if self.chunks[chunk_position].blocks[i][j].type in [STONE, DEPTH_STONE]:
                    if randrange(10000) < 4:
                        print('cave', position)
                        structures.cave(self, position)
                    if randrange(10000) < 5:
                        structures.ore(self, position, randrange(10, 40), SAND)
                    if randrange(10000) < 20:
                        structures.ore(self, position, randrange(7, 20), COAL_ORE, depth_block_verion=DEPTH_COAL_ORE)
                    if randrange(10000) < 10:
                        structures.ore(self, position, randrange(5, 15), IRON_ORE, depth_block_verion=DEPTH_IRON_ORE)
                if self.chunks[chunk_position].blocks[i][j].type == HELL_STONE:
                    if randrange(10000) < 15:
                        structures.ore(self, position, randrange(15, 30), MAGMA)
                    if randrange(10000) < 8:
                        print('hell star', position)
                        structures.hell_star(self, position)
                j2 = j + CHUNK_SIZE * chunk_position[1]
                if j2 > DEPTH_STONE_LEVEL and self.chunks[chunk_position].blocks[i][j - 1].type == AIR:
                    if randrange(100) < 3:
                        structures.ore(self, position, randrange(5, 15), DENSE_DEPTH_STONE)
        self.chunks[chunk_position].loaded = True

        self.setblock((chunk_position[0] * settings.CHUNK_SIZE, chunk_position[1] * settings.CHUNK_SIZE), settings.NONE)

    def setblock(self, position, block_type):
        chunk_pos = (position[0] // CHUNK_SIZE, position[1] // CHUNK_SIZE)
        if chunk_pos not in self.chunks:
            self.chunks[chunk_pos] = Chunk()
            self.chunks[chunk_pos].load(*chunk_pos)
        if not self.chunks[chunk_pos].generated:
            self.generate(chunk_pos)
        self.chunks[chunk_pos].blocks[position[0] % CHUNK_SIZE][position[1] % CHUNK_SIZE].type = block_type

    def getblock(self, x, y):
        chunk_pos = (x // CHUNK_SIZE, y // CHUNK_SIZE)
        if chunk_pos not in self.chunks:
            self.chunks[chunk_pos] = Chunk()
            self.chunks[chunk_pos].load(*chunk_pos)
        if not self.chunks[chunk_pos].generated:
            self.generate(chunk_pos)
        return self.chunks[chunk_pos].blocks[x % CHUNK_SIZE][y % CHUNK_SIZE].type
