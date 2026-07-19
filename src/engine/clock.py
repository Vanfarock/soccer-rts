import pygame


class Clock:
    def __init__(self, fps: int):
        self._clock = pygame.time.Clock()
        self._fps = fps

    def tick(self) -> float:
        return self._clock.tick(self._fps) / 1000.0
