from __future__ import annotations

import math
from typing import TYPE_CHECKING

from engine.components.component import Component
from engine.frame_context import FrameContext
from engine.primitives.ellipse import Ellipse
from engine.primitives.game_object import GameObject, GameObjectType
from engine.render_target import RenderTarget
from engine.vector import Vector2D
from shared.colors import Color

if TYPE_CHECKING:
    from player.player import Player


class BallPhysicsComponent(Component):
    def __init__(self, drag: float) -> None:
        super().__init__()
        self._drag = drag

    def update(self, ctx: FrameContext) -> None:
        ball = self.owner
        if not isinstance(ball, Ball):
            return

        if ball.carrier is not None:
            ball.sync_to_carrier()
            return

        ball.set_pos(ball.pos + ball.velocity * ctx.dt)

        if ball.velocity.length_squared() < 1e-6:
            ball.set_velocity(Vector2D(0, 0))
            return

        decay = math.exp(-self._drag * ctx.dt)
        ball.set_velocity(ball.velocity * decay)

        if ball.velocity.length() < 5:
            ball.set_velocity(Vector2D(0, 0))


class Ball(GameObject):
    RADIUS = 4
    ATTACH_GAP = 2

    def __init__(self, pos: Vector2D, drag: float):
        super().__init__(
            type=GameObjectType.CUSTOM,
            pos=pos,
        )
        self._velocity = Vector2D(0, 0)
        self._carrier: Player | None = None
        self.add_component(BallPhysicsComponent(drag))

    @property
    def velocity(self) -> Vector2D:
        return self._velocity

    @property
    def carrier(self) -> Player | None:
        return self._carrier

    @property
    def is_free(self) -> bool:
        return self._carrier is None

    def attach_offset(self) -> float:
        from player.player import Player

        return Player.RADIUS + Ball.RADIUS + Ball.ATTACH_GAP

    def attach_point(self, player: Player) -> Vector2D:
        return player.pos + player.forward * self.attach_offset()

    def attach(self, player: Player) -> None:
        self._carrier = player
        self._velocity = Vector2D(0, 0)
        self.sync_to_carrier()

    def detach(self) -> None:
        self._carrier = None

    def set_velocity(self, velocity: Vector2D) -> None:
        self._velocity = velocity

    def sync_to_carrier(self) -> None:
        if self._carrier is None:
            return

        self.set_pos(self.attach_point(self._carrier))

    def render(self, target: RenderTarget) -> None:
        diameter = self.world_size_to_screen(
            Vector2D(Ball.RADIUS * 2, Ball.RADIUS * 2)
        ).x
        top_left = self.world_to_screen(
            Vector2D(self.pos.x - Ball.RADIUS, self.pos.y - Ball.RADIUS)
        )
        Ellipse(top_left, Vector2D(diameter, diameter), Color.YELLOW).render(target)
