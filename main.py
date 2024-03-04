import pygame
from player import Player
from chunk import Chunk

if __name__ == '__main__':
    pygame.init()
    window_size = (300, 300)
    pygame.display.set_caption("Main window")
    screen = pygame.display.set_mode(window_size)
    background_color = (100, 200, 255)
    screen.fill(background_color)

    chunk = Chunk()
    chunk.load()
    player = Player()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            player.update(event)

        screen.fill(background_color)
        chunk.update()
        chunk.draw(screen, player.position)

        player.draw()

        pygame.display.flip()
