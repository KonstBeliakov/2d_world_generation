import copy
import random
from random import randrange

from settings import *
from utils import *
from chunk import Chunk
from perlin_noise import PerlinNoise
from time import perf_counter


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
        self.time = perf_counter()
        self.temp = 0
        self.prev_player_position = None

    def update(self, player_position):
        moved = self.prev_player_position is None or \
                (player_position[0] // CHUNK_SIZE != self.prev_player_position[0] // CHUNK_SIZE or
                 player_position[1] // CHUNK_SIZE != self.prev_player_position[1] // CHUNK_SIZE)
        self.prev_player_position = player_position

        if moved:
            t = perf_counter()
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
            print('loading:', perf_counter() - t, end=' ')

            # generating structures
            t = perf_counter()
            for i in range(int(player_position[0] // CHUNK_SIZE - LOAD_DISTANSE),
                           int(player_position[0] // CHUNK_SIZE + LOAD_DISTANSE)):
                for j in range(int(player_position[1] // CHUNK_SIZE - LOAD_DISTANSE),
                               int(player_position[1] // CHUNK_SIZE + LOAD_DISTANSE)):
                    if dist((i, j),
                            (player_position[0] // CHUNK_SIZE, player_position[1] // CHUNK_SIZE)) <= LOAD_DISTANSE:
                        if not self.chunks[(i, j)].loaded:
                            self.structures_generate((i, j))

            print('generating:', perf_counter() - t, end=' ')

            # unloading
            t2 = perf_counter()
            t = []
            for chunk_position, chunk in self.chunks.items():
                if dist(chunk_position,
                        (player_position[0] // CHUNK_SIZE, player_position[1] // CHUNK_SIZE)) > GENERATION_DISTANSE:
                    t.append(chunk_position)
            for i in t:
                self.chunks[i].unload(*i)
                del self.chunks[i]

            print('unloading:', perf_counter() - t2, end=' ')

    def draw(self, screen, player_position):
        for chunk_position, chunk in self.chunks.items():
            if abs(chunk_position[0] - player_position[0] // CHUNK_SIZE) <= DRAW_DISTANSE_X and \
                    abs(chunk_position[1] - player_position[1] // CHUNK_SIZE) <= DRAW_DISTANSE_Y:
                chunk.update()
                chunk.draw(screen, chunk_position, player_position)

        #print('fps:', 1 / (perf_counter() - self.time))
        #self.time = perf_counter()

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
                        self.tree(position)
                    if randrange(100) < 30:
                        self.setblock(position, GRASS_BLOCK)
                if self.chunks[chunk_position].blocks[i][j].type in [STONE, DEPTH_STONE]:
                    if randrange(10000) < 4:
                        print('cave', position)
                        self.cave(position)
                    if randrange(10000) < 5:
                        self.ore(position, randrange(10, 40), SAND)
                    if randrange(10000) < 20:
                        self.ore(position, randrange(7, 20), COAL_ORE, depth_block_verion=DEPTH_COAL_ORE)
                    if randrange(10000) < 10:
                        self.ore(position, randrange(5, 15), IRON_ORE, depth_block_verion=DEPTH_IRON_ORE)
                if self.chunks[chunk_position].blocks[i][j].type == HELL_STONE:
                    if randrange(10000) < 15:
                        self.ore(position, randrange(15, 30), MAGMA)
                    if randrange(10000) < 8:
                        self.hell_star(position)
                j2 = j + CHUNK_SIZE * chunk_position[1]
                if j2 > DEPTH_STONE_LEVEL and self.chunks[chunk_position].blocks[i][j - 1].type == AIR:
                    if randrange(100) < 3:
                        self.ore(position, randrange(5, 15), DENSE_DEPTH_STONE)
        self.chunks[chunk_position].loaded = True

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

        for _ in range(iteration):
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

    def ore(self, position: tuple, size: int, block_type, depth_block_verion=None):
        pos = [0, 0]

        s = {(pos[0], pos[1] + 1), (pos[0], pos[1] - 1), (pos[0] + 1, pos[1]), (pos[0] - 1, pos[1])}
        s2 = set()

        for i in range(size):
            p = random.choice(list(s))
            s.remove(p)
            s2.add(p)

            if self.getblock(position[0] + p[0], position[1] + p[1]) != AIR:
                if depth_block_verion and position[1] > DEPTH_STONE_LEVEL:
                    self.setblock((position[0] + p[0], position[1] + p[1]), depth_block_verion)
                else:
                    self.setblock((position[0] + p[0], position[1] + p[1]), block_type)

            for j in [(p[0], p[1] + 1), (p[0], p[1] - 1), (p[0] + 1, p[1]), (p[0] - 1, p[1])]:
                if j not in s2:
                    s.add(j)

    def hell_star(self, position):
        l = [[0] * 20 for i in range(20)]

        for x in range(-8, 9):
            for y in range(-8, 9):
                l[10 + x][10 + y] = int(randrange(1, 10) * (9 - dist((0, 0), (x, y))))

        for x in range(20):
            for y in range(20):
                pos = (position[0] + x, position[1] + y)
                if l[x][y] > 50:
                    self.setblock(pos, RICH_HELL_STAR_ORE)
                elif l[x][y] > 20:
                    self.setblock(pos, HELL_STAR_ORE)
                elif l[x][y] > 10:
                    self.setblock(pos, POOR_HELL_STAR_ORE)
            print()

        '''for x in range(-2, 3):
            for y in range(-2, 3):
                if randrange(100) < 30:
                    self.setblock((position[0] + x, position[1] + y), RICH_HELL_STAR_ORE)

                    self.setblock((position[0] + x + 1, position[1] + y), RICH_HELL_STAR_ORE)
                    self.setblock((position[0] + x - 1, position[1] + y), RICH_HELL_STAR_ORE)
                    self.setblock((position[0] + x, position[1] + y + 1), RICH_HELL_STAR_ORE)
                    self.setblock((position[0] + x, position[1] + y - 1), RICH_HELL_STAR_ORE)

        for x in range(-6, 7):
            for y in range(-6, 7):
                d =  dist((0, 0), (x, y))
                if randrange(6) < (7 - d):
                    self.setblock((position[0] + x, position[1] + y), HELL_STAR_ORE)'''