import pygame

from infra.engine.render_target import RenderTarget
from infra.engine.vector import Vector2D
from shared.colors import Color


class Text:
    _font_cache: dict[int, pygame.font.Font] = {}

    def __init__(
        self, text: str, pos: Vector2D, color: Color, font_size: int = 12
    ) -> None:
        self.text = text
        self.pos = pos
        self.color = color
        self.font_size = font_size

    @classmethod
    def _get_font(cls, size: int) -> pygame.font.Font:
        if size not in cls._font_cache:
            cls._font_cache[size] = pygame.font.SysFont(None, size)

        return cls._font_cache[size]

    def render(self, target: RenderTarget) -> None:
        scale = target.pixel_scale
        font = self._get_font(max(1, round(self.font_size * scale)))
        surface = font.render(self.text, True, self.color.to_tuple())
        center = (
            round(self.pos.x * scale),
            round(self.pos.y * scale),
        )
        rect = surface.get_rect(center=center)
        target.surface.blit(surface, rect)
