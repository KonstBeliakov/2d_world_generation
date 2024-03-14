import pygame
from player import Player
from world import World
import settings
import os


if __name__ == '__main__':
    global BLOCK_SIZE
    os.mkdir(settings.WORLD_FOLDER_NAME)

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
            if event.type == pygame.KEYDOWN:
                print('event keydown')
                if event.key == pygame.K_o:
                    settings.BLOCK_SIZE = int(settings.BLOCK_SIZE * 1.5)
                    settings.update()
                elif event.key == pygame.K_p:
                    settings.BLOCK_SIZE //= 1.5
                    settings.update()
            player.update(event)

        screen.fill(background_color)

        world.update(player.position)
        world.draw(screen, player.position)

        player.draw(screen)
        pygame.display.flip()
