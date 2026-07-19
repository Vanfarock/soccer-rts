import pygame

from engine.primitives.game_object import GameObject, GameObjectType
from engine.render_target import RenderTarget
from engine.vector import Vector2D
from shared.colors import Color


class Ellipse(GameObject):
    def __init__(self, pos: Vector2D, size: Vector2D, color: Color):
        super().__init__(
            type=GameObjectType.ELLIPSE,
            pos=pos,
            size=size,
            color=color,
        )

    def render(self, target: RenderTarget) -> None:
        scale = target.pixel_scale
        pygame.draw.ellipse(
            target.surface,
            self.color.to_tuple(),
            (
                round(self.pos.x * scale),
                round(self.pos.y * scale),
                round(self.size.x * scale),
                round(self.size.y * scale),
            ),
        )
