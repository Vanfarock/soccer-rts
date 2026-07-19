import pygame

from shared.colors import Color


class Window:
    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    @property
    def screen(self) -> pygame.Surface:
        return self._screen

    @property
    def surface(self) -> pygame.Surface:
        return self._screen

    @property
    def pixel_scale(self) -> float:
        return 1.0

    def set_background_color(self, color: Color) -> None:
        self._screen.fill(color.to_tuple())
