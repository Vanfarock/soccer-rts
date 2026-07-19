import pygame

from domain.team.team import Team
from infra.engine.entity import GameObject, GameObjectType
from infra.engine.frame_context import FrameContext
from infra.engine.primitives.ellipse import Ellipse
from infra.engine.primitives.text import Text
from infra.engine.render_target import RenderTarget
from infra.engine.vector import Vector2D
from shared.colors import Color
from shared.entity_sizes import BALL_RADIUS, PLAYER_PICKUP_SLACK, PLAYER_RADIUS


class Player(GameObject):
    RADIUS = PLAYER_RADIUS
    PICKUP_SLACK = PLAYER_PICKUP_SLACK
    BASE_SPEED = 200
    WITH_BALL_SPEED_FACTOR = 0.8
    FOCUS_RING_PADDING = 2
    FOCUS_RING_WIDTH = 2
    NUMBER_LABEL_OFFSET = 14

    def __init__(self, pos: Vector2D, team: Team, number: int):
        super().__init__(
            type=GameObjectType.CUSTOM,
            pos=pos,
        )
        self._team = team
        self._number = number
        self._forward = Vector2D(1, 0)
        self._pickup_blocked_until_clear = False
        self._focused = False

    @property
    def team(self) -> Team:
        return self._team

    @property
    def number(self) -> int:
        return self._number

    @property
    def focused(self) -> bool:
        return self._focused

    def set_focused(self, focused: bool) -> None:
        self._focused = focused

    @property
    def forward(self) -> Vector2D:
        return self._forward

    @property
    def pickup_radius(self) -> float:
        return Player.RADIUS + BALL_RADIUS + Player.PICKUP_SLACK

    def update_facing(self, ctx: FrameContext) -> None:
        mouse_world = self.screen_to_world(ctx.mouse_pos)
        to_mouse = mouse_world - self.pos

        if to_mouse.length_squared() > 1e-6:
            self._forward = to_mouse.normalized()

    def update_pickup_block(self, ball_distance: float) -> bool:
        if not self._pickup_blocked_until_clear:
            return False

        if ball_distance <= self.pickup_radius:
            return True

        self._pickup_blocked_until_clear = False
        return False

    def block_pickup_after_kick(self) -> None:
        self._pickup_blocked_until_clear = True

    def movement_speed(self, has_ball: bool) -> float:
        speed = Player.BASE_SPEED
        if has_ball:
            speed *= Player.WITH_BALL_SPEED_FACTOR
        return speed

    def render(self, target: RenderTarget) -> None:
        diameter = self.world_size_to_screen(
            Vector2D(Player.RADIUS * 2, Player.RADIUS * 2)
        ).x
        top_left = self.world_to_screen(
            Vector2D(self.pos.x - Player.RADIUS, self.pos.y - Player.RADIUS)
        )
        Ellipse(top_left, Vector2D(diameter, diameter), self._team.color).render(target)

        if self._focused:
            ring_radius = Player.RADIUS + Player.FOCUS_RING_PADDING
            ring_diameter = self.world_size_to_screen(
                Vector2D(ring_radius * 2, ring_radius * 2)
            ).x
            ring_top_left = self.world_to_screen(
                Vector2D(self.pos.x - ring_radius, self.pos.y - ring_radius)
            )
            scale = target.pixel_scale
            pygame.draw.ellipse(
                target.surface,
                Color.WHITE.to_tuple(),
                (
                    round(ring_top_left.x * scale),
                    round(ring_top_left.y * scale),
                    round(ring_diameter * scale),
                    round(ring_diameter * scale),
                ),
                width=max(1, round(Player.FOCUS_RING_WIDTH * scale)),
            )

        label_pos = self.world_to_screen(
            Vector2D(self.pos.x, self.pos.y - Player.NUMBER_LABEL_OFFSET)
        )
        Text(str(self._number), label_pos, Color.WHITE, font_size=10).render(target)

        if self._focused:
            self.render_component_overlays(target)
