import time

import pygame


class Player():
    def __init__(self):
        self.position = [0, 0]
        self.max_speed = 10
        self.current_speed = (0, 0)
        self.timer = time.perf_counter()

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.current_speed = (0, self.max_speed)
            if event.key == pygame.K_s:
                self.current_speed = (0, -self.max_speed)
            if event.key == pygame.K_a:
                self.current_speed = (self.max_speed, 0)
            if event.key == pygame.K_d:
                self.current_speed = (-self.max_speed, 0)
        elif event.type == pygame.KEYUP:
            self.current_speed = (0, 0)

        self.position = (self.position[0] + self.current_speed[0] * (self.timer - time.perf_counter()),
                         self.position[1] + self.current_speed[1] * (self.timer - time.perf_counter()))
        self.timer = time.perf_counter()

    def draw(self, screen):
        pass
