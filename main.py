import pygame
from player import Player
from world import World
from settings import *
import os


if __name__ == '__main__':
    os.mkdir(WORLD_FOLDER_NAME)

    pygame.init()
    window_size = (1200, 800)
    pygame.display.set_caption("Main window")
    screen = pygame.display.set_mode(window_size)
    background_color = (100, 200, 255)
    screen.fill(background_color)

    player = Player()
    world = World()

    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            player.update(event)

        screen.fill(background_color)

        world.draw(screen, player.position)

        player.draw(screen)
        pygame.display.flip()
