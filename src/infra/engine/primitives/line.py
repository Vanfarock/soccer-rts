import pygame

from infra.engine.primitives.game_object import GameObject, GameObjectType
from infra.engine.render_target import RenderTarget
from infra.engine.vector import Vector2D
from shared.colors import Color


class Line(GameObject):
    def __init__(
        self,
        start: Vector2D,
        end: Vector2D,
        color: Color,
        thickness: float = 1,
    ):
        super().__init__(
            type=GameObjectType.LINE,
            pos=start,
            color=color,
            thickness=thickness,
        )
        self._end = end

    @property
    def end(self) -> Vector2D:
        return self._end

    def render(self, target: RenderTarget) -> None:
        scale = target.pixel_scale
        start = (self.pos.x * scale, self.pos.y * scale)
        end = (self._end.x * scale, self._end.y * scale)
        color = self.color.to_tuple()
        width = max(1, round(self.thickness * scale))

        pygame.draw.line(target.surface, color, start, end, width)
