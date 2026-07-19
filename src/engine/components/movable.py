import pygame

from engine.components.component import Component
from engine.frame_context import FrameContext
from engine.vector import Vector2D


class MovableComponent(Component):
    def __init__(self, speed: float) -> None:
        super().__init__()
        self._speed = speed

    def update(self, ctx: FrameContext) -> None:
        direction = Vector2D(0, 0)

        if ctx.pressed_keys[pygame.K_w]:
            direction = direction + Vector2D(0, -1)
        if ctx.pressed_keys[pygame.K_s]:
            direction = direction + Vector2D(0, 1)
        if ctx.pressed_keys[pygame.K_a]:
            direction = direction + Vector2D(-1, 0)
        if ctx.pressed_keys[pygame.K_d]:
            direction = direction + Vector2D(1, 0)

        if direction.x == 0 and direction.y == 0:
            return

        length = (direction.x**2 + direction.y**2) ** 0.5
        normalized = Vector2D(direction.x / length, direction.y / length)
        delta = normalized * self._speed * ctx.dt
        self.owner.set_pos(self.owner.pos + delta)
