import pygame

from engine.components.component import Component
from engine.frame_context import FrameContext
from engine.vector import Vector2D


class MovableComponent(Component):
    def __init__(self, speed: float) -> None:
        super().__init__()
        self._base_speed = speed

    def update(self, ctx: FrameContext) -> None:
        from player.keyboard_controller import KeyboardControllerComponent
        from player.player import Player

        owner = self.owner
        speed = self._base_speed

        if isinstance(owner, Player):
            controller = owner.get_component(KeyboardControllerComponent)
            if controller is not None:
                if ctx.pressed_mouse[2] and owner.has_ball(controller.ball):
                    return
                speed = owner.movement_speed(controller.ball)

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
        delta = normalized * speed * ctx.dt
        owner.set_pos(owner.pos + delta)
