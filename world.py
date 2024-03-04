from random import randrange

import pygame
from settings import *
from utils import *
from chunk import Chunk


class World():
    def __init__(self):
        self.chunks = {(i, j): Chunk() for i in range(2) for j in range(2)}
        for chunk in self.chunks.values():
            chunk.load()

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
                        self.generate((i, j))
        t = []
        for chunk_position, chunk in self.chunks.items():
            if dist(chunk_position,
                    (player_position[0] // CHUNK_SIZE, player_position[1] // CHUNK_SIZE)) > LOAD_DISTANSE:
                t.append(chunk_position)

            chunk.update()
            chunk.draw(screen, chunk_position, player_position)

        for i in t:
            del self.chunks[i]

        print(f'chunks loaded: {len(self.chunks)}')

    def generate(self, chunk_position):
        if chunk_position[1] > 0:
            pass
        if chunk_position[1] == 0:
            for i in range(CHUNK_SIZE):
                for j in range(CHUNK_SIZE):
                    if j == 0:
                        self.chunks[chunk_position].blocks[i][j].type = GRASS
                    elif j < randrange(2, 5):
                        self.chunks[chunk_position].blocks[i][j].type = DIRT
                    else:
                        self.chunks[chunk_position].blocks[i][j].type = STONE
        elif chunk_position[1] > 0:
            for i in range(CHUNK_SIZE):
                for j in range(CHUNK_SIZE):
                    self.chunks[chunk_position].blocks[i][j].type = STONE
        self.chunks[chunk_position].loaded = True
