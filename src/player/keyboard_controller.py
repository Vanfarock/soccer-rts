from __future__ import annotations

import pygame

from ball.ball import Ball
from engine.components.component import Component
from engine.frame_context import FrameContext
from engine.primitives.ellipse import Ellipse
from engine.primitives.line import Line
from engine.render_target import RenderTarget
from engine.vector import Vector2D
from player.player import Player
from shared.colors import Color


class KeyboardControllerComponent(Component):
    TOSS_POWER = 450
    PASS_MIN = 200
    PASS_MAX = 900
    CHARGE_TIME = 1.0
    AIM_LINE_THICKNESS = 4
    AIM_MARKER_RADIUS = 6

    @property
    def ball(self) -> Ball:
        return self._ball

    def __init__(self, ball: Ball, drag: float) -> None:
        super().__init__()
        self._ball = ball
        self._drag = drag
        self._prev_space = False
        self._prev_rmb = False
        self._charging = False
        self._charge_elapsed = 0.0
        self._aim_power = 0.0

    def update(self, ctx: FrameContext) -> None:
        player = self.owner
        if not isinstance(player, Player):
            return

        player.update_facing(ctx)
        player.try_receive(self._ball)

        space_pressed = ctx.pressed_keys[pygame.K_SPACE]
        rmb_pressed = ctx.pressed_mouse[2]

        if space_pressed and not self._prev_space and player.has_ball(self._ball):
            player.kick_ball(self._ball, KeyboardControllerComponent.TOSS_POWER)

        if rmb_pressed:
            if not self._prev_rmb and player.has_ball(self._ball):
                self._charging = True
                self._charge_elapsed = 0.0

            if self._charging:
                self._charge_elapsed += ctx.dt
                charge_ratio = min(1.0, self._charge_elapsed / KeyboardControllerComponent.CHARGE_TIME)
                self._aim_power = self._lerp(
                    KeyboardControllerComponent.PASS_MIN,
                    KeyboardControllerComponent.PASS_MAX,
                    charge_ratio,
                )
        elif self._prev_rmb and self._charging:
            if player.has_ball(self._ball):
                player.kick_ball(self._ball, self._aim_power)
            self._charging = False
            self._charge_elapsed = 0.0
            self._aim_power = 0.0

        self._prev_space = space_pressed
        self._prev_rmb = rmb_pressed

    def render_aim(self, target: RenderTarget) -> None:
        if not self._charging:
            return

        player = self.owner
        if not isinstance(player, Player) or not player.has_ball(self._ball):
            return

        start = self._ball.attach_point(player)
        distance = self._predicted_distance(self._aim_power)
        end = start + player.forward * distance

        Line(
            player.world_to_screen(start),
            player.world_to_screen(end),
            Color.WHITE,
            thickness=KeyboardControllerComponent.AIM_LINE_THICKNESS,
        ).render(target)

        marker_diameter = player.world_size_to_screen(
            Vector2D(
                KeyboardControllerComponent.AIM_MARKER_RADIUS * 2,
                KeyboardControllerComponent.AIM_MARKER_RADIUS * 2,
            )
        ).x
        marker_top_left = player.world_to_screen(
            Vector2D(
                end.x - KeyboardControllerComponent.AIM_MARKER_RADIUS,
                end.y - KeyboardControllerComponent.AIM_MARKER_RADIUS,
            )
        )
        Ellipse(
            marker_top_left,
            Vector2D(marker_diameter, marker_diameter),
            Color.WHITE,
        ).render(target)

    def _predicted_distance(self, power: float) -> float:
        if self._drag <= 0:
            return power

        return power / self._drag

    @staticmethod
    def _lerp(start: float, end: float, t: float) -> float:
        return start + (end - start) * t
