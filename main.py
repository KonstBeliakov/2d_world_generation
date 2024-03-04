import pygame
from player import Player
from chunk import Chunk
from settings import *
from utils import *

if __name__ == '__main__':
    pygame.init()
    window_size = (800, 800)
    pygame.display.set_caption("Main window")
    screen = pygame.display.set_mode(window_size)
    background_color = (100, 200, 255)
    screen.fill(background_color)

    chunks = {(i, j): Chunk() for i in range(2) for j in range(2)}
    for chunk in chunks.values():
        chunk.load()
    player = Player()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            player.update(event)

        screen.fill(background_color)

        for i in range(int(player.position[0] // CHUNK_SIZE - LOAD_DISTANSE),
                       int(player.position[0] // CHUNK_SIZE + LOAD_DISTANSE)):
            for j in range(int(player.position[1] // CHUNK_SIZE - LOAD_DISTANSE),
                           int(player.position[1] // CHUNK_SIZE + LOAD_DISTANSE)):

                if dist((i, j), (player.position[0] // CHUNK_SIZE, player.position[1] // CHUNK_SIZE)) <= LOAD_DISTANSE:
                    if (i, j) not in chunks:
                        chunks[(i, j)] = Chunk()
                    chunks[(i, j)].load()

        for chunk_position, chunk in chunks.items():
            if dist(chunk_position,
                    (player.position[0] // CHUNK_SIZE, player.position[1] // CHUNK_SIZE)) > LOAD_DISTANSE:
                chunk.unload()

            chunk.update()
            chunk.draw(screen, chunk_position, player.position)

        player.draw()

        pygame.display.flip()
