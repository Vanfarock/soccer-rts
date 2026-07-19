from __future__ import annotations

from typing import TYPE_CHECKING

from engine.frame_context import FrameContext
from engine.primitives.ellipse import Ellipse
from engine.primitives.game_object import GameObject, GameObjectType
from engine.render_target import RenderTarget
from engine.vector import Vector2D
from team.team import Team

if TYPE_CHECKING:
    from ball.ball import Ball


class Player(GameObject):
    RADIUS = 8
    PICKUP_SLACK = 8

    def __init__(self, pos: Vector2D, team: Team):
        super().__init__(
            type=GameObjectType.CUSTOM,
            pos=pos,
        )
        self._team = team
        self._forward = Vector2D(1, 0)

    @property
    def forward(self) -> Vector2D:
        return self._forward

    @property
    def pickup_radius(self) -> float:
        from ball.ball import Ball

        return Player.RADIUS + Ball.RADIUS + Player.PICKUP_SLACK

    def update_facing(self, ctx: FrameContext) -> None:
        mouse_world = self.screen_to_world(ctx.mouse_pos)
        to_mouse = mouse_world - self.pos

        if to_mouse.length_squared() > 1e-6:
            self._forward = to_mouse.normalized()

    def has_ball(self, ball: Ball) -> bool:
        return ball.carrier is self

    def kick_ball(self, ball: Ball, power: float) -> None:
        if not self.has_ball(ball):
            return

        ball.detach()
        ball.set_velocity(self._forward * power)

    def try_receive(self, ball: Ball) -> bool:
        if not ball.is_free:
            return False

        distance = (ball.pos - self.pos).length()
        if distance > self.pickup_radius:
            return False

        ball.attach(self)
        return True

    def render(self, target: RenderTarget) -> None:
        diameter = self.world_size_to_screen(
            Vector2D(Player.RADIUS * 2, Player.RADIUS * 2)
        ).x
        top_left = self.world_to_screen(
            Vector2D(self.pos.x - Player.RADIUS, self.pos.y - Player.RADIUS)
        )
        Ellipse(top_left, Vector2D(diameter, diameter), self._team.color).render(target)

        from player.keyboard_controller import KeyboardControllerComponent

        controller = self.get_component(KeyboardControllerComponent)
        if controller is not None:
            controller.render_aim(target)
