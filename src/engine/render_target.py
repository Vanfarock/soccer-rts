from typing import Protocol

import pygame

from shared.colors import Color


class RenderTarget(Protocol):
    @property
    def surface(self) -> pygame.Surface: ...

    @property
    def pixel_scale(self) -> float: ...

    def set_background_color(self, color: Color) -> None: ...
