import pygame

class Player():
    def __init__(self):
        self.position = [0, 0]

    def update(self, event):
        print(self.position)
        if event.type == pygame.KEYDOWN:
            print('keydown event')
            if event.key == pygame.K_w:
                self.position[1] -= 1
            if event.key == pygame.K_s:
                self.position[1] += 1
            if event.key == pygame.K_a:
                self.position[0] -= 1
            if event.key == pygame.K_d:
                self.position[0] += 1

    def draw(self):
        pass