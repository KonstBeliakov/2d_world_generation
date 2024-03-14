import copy
import random
#from world import World
from utils import dist
from settings import *


class World:
    pass

class v2:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def tree(world: World, position):
    tree_height = random.randint(4, 6)
    for j in range(position[1] - tree_height, position[1]):
        world.setblock((position[0], j), LOG)

    for i in range(position[0] - 2, position[0] + 3):
        for j in range(position[1] - tree_height - 2, position[1] - tree_height + 2):
            if world.getblock(i, j) != LOG:
                world.setblock((i, j), LEAVES)

    world.setblock((position[0] - 2, position[1] - tree_height - 2), AIR)
    world.setblock((position[0] + 2, position[1] - tree_height - 2), AIR)


def cave(world: World, position):
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
                world.setblock((position[0] + i - n // 2, position[1] + j - n // 2), AIR)


def ore(world: World, position: tuple, size: int, block_type, depth_block_verion=None):
    pos = [0, 0]

    s = {(pos[0], pos[1] + 1), (pos[0], pos[1] - 1), (pos[0] + 1, pos[1]), (pos[0] - 1, pos[1])}
    s2 = set()

    for i in range(size):
        p = random.choice(list(s))
        s.remove(p)
        s2.add(p)

        if world.getblock(position[0] + p[0], position[1] + p[1]) != AIR:
            if depth_block_verion and position[1] > DEPTH_STONE_LEVEL:
                world.setblock((position[0] + p[0], position[1] + p[1]), depth_block_verion)
            else:
                world.setblock((position[0] + p[0], position[1] + p[1]), block_type)

        for j in [(p[0], p[1] + 1), (p[0], p[1] - 1), (p[0] + 1, p[1]), (p[0] - 1, p[1])]:
            if j not in s2:
                s.add(j)


def hell_star(world: World, position):
    l = [[0] * 20 for i in range(20)]

    for x in range(-8, 9):
        for y in range(-8, 9):
            l[10 + x][10 + y] = int(randrange(1, 10) * (9 - dist((0, 0), (x, y))))

    for x in range(20):
        for y in range(20):
            pos = (position[0] + x, position[1] + y)
            if l[x][y] > 50:
                world.setblock(pos, RICH_HELL_STAR_ORE)
            elif l[x][y] > 20:
                world.setblock(pos, HELL_STAR_ORE)
            elif l[x][y] > 10:
                world.setblock(pos, POOR_HELL_STAR_ORE)