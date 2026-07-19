import pygame


class Clock:
    def __init__(self, fps: int):
        self._clock = pygame.time.Clock()
        self._fps = fps

    def tick(self):
        self._clock.tick(self._fps)
