import pygame

from engine.primitives.game_object import GameObject, GameObjectType
from engine.render_target import RenderTarget
from engine.vector import Vector2D
from shared.colors import Color


class Rectangle(GameObject):
    def __init__(
        self,
        pos: Vector2D,
        size: Vector2D,
        color: Color,
        thickness: float = 0,
        border_radius: float = 0,
    ):
        super().__init__(
            type=GameObjectType.RECTANGLE,
            pos=pos,
            size=size,
            color=color,
            thickness=thickness,
            border_radius=border_radius,
        )

    def render(self, target: RenderTarget) -> None:
        scale = target.pixel_scale
        rect = (
            round(self.pos.x * scale),
            round(self.pos.y * scale),
            round(self.size.x * scale),
            round(self.size.y * scale),
        )
        color = self.color.to_tuple()
        width = round(self.thickness * scale)

        if self._border_radius:
            pygame.draw.rect(
                target.surface,
                color,
                rect,
                width,
                round(self._border_radius * scale),
            )
        else:
            pygame.draw.rect(target.surface, color, rect, width)
