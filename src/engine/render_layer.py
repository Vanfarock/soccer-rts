import pygame

from engine.vector import Vector2D
from engine.window import Window
from shared.colors import Color


class RenderLayer:
    def __init__(self, width: int, height: int, *, pixel_scale: float = 1.0):
        self._surface = pygame.Surface((width, height))
        self._pixel_scale = pixel_scale

    @property
    def surface(self) -> pygame.Surface:
        return self._surface

    @property
    def pixel_scale(self) -> float:
        return self._pixel_scale

    def set_background_color(self, color: Color) -> None:
        self._surface.fill(color.to_tuple())

    def blit_scaled_to(
        self, window: Window, dest: Vector2D, dest_size: Vector2D
    ) -> None:
        scaled = pygame.transform.smoothscale(
            self._surface,
            (round(dest_size.x), round(dest_size.y)),
        )
        window.surface.blit(scaled, (round(dest.x), round(dest.y)))
