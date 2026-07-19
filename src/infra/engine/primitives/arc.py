import math

from infra.engine.primitives.game_object import GameObject, GameObjectType
from infra.engine.primitives.line import Line
from infra.engine.render_target import RenderTarget
from infra.engine.vector import Vector2D
from shared.colors import Color


class Arc(GameObject):
    def __init__(
        self,
        center: Vector2D,
        radius: float,
        start_angle: float,
        stop_angle: float,
        color: Color,
        thickness: float = 1,
        *,
        segments: int = 48,
    ):
        super().__init__(
            type=GameObjectType.ARC,
            pos=center,
            color=color,
            thickness=thickness,
        )
        self._radius = radius
        self._start_angle = start_angle
        self._stop_angle = stop_angle
        self._segments = segments

    def _point_at(self, angle: float) -> Vector2D:
        return Vector2D(
            self.pos.x + math.cos(angle) * self._radius,
            self.pos.y + math.sin(angle) * self._radius,
        )

    def render(self, target: RenderTarget) -> None:
        step = (self._stop_angle - self._start_angle) / self._segments
        prev = self._point_at(self._start_angle)

        for i in range(1, self._segments + 1):
            angle = self._start_angle + step * i
            point = self._point_at(angle)
            Line(prev, point, self.color, self.thickness).render(target)
            prev = point
