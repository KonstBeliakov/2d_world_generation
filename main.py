import pygame
from player import Player
from world import World
import settings
import os


def update_textures():
    for i in range(len(settings.textures)):
        if settings.textures[i] is not None:
            settings.textures[i] = pygame.transform.scale(pygame.image.load(f'textures/{settings.textures_files[i]}'),
                                                          (settings.BLOCK_SIZE, settings.BLOCK_SIZE))
            # settings.textures[i] = pygame.transform.scale(settings.textures[i], (settings.BLOCK_SIZE, settings.BLOCK_SIZE))
    print(f'block size: {settings.BLOCK_SIZE}')


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
                    settings.DRAW_DISTANSE_X = (3 * 16 // settings.BLOCK_SIZE) + 1
                    settings.DRAW_DISTANSE_Y = (2 * 16 // settings.BLOCK_SIZE) + 1
                    settings.LOAD_DISTANSE = settings.DRAW_DISTANSE_X + 3
                    settings.GENERATION_DISTANSE = settings.DRAW_DISTANSE_X + 6

                    update_textures()
                    print('set', settings.BLOCK_SIZE)
                if event.key == pygame.K_p:
                    settings.BLOCK_SIZE //= 1.5
                    settings.DRAW_DISTANSE_X = (3 * 16 // settings.BLOCK_SIZE) + 1
                    settings.DRAW_DISTANSE_Y = (3 * 16 // settings.BLOCK_SIZE) + 1
                    settings.LOAD_DISTANSE = settings.DRAW_DISTANSE_X + 3
                    settings.GENERATION_DISTANSE = settings.DRAW_DISTANSE_X + 6
                    update_textures()
                    print('set', settings.BLOCK_SIZE)
            player.update(event)

        screen.fill(background_color)

        world.update(player.position)
        world.draw(screen, player.position)

        player.draw(screen)
        pygame.display.flip()
