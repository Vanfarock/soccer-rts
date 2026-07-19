import math

from domain.ball.boundary import resolve_pitch_bounds
from infra.engine.entity import Component, GameObject, GameObjectType
from infra.engine.frame_context import FrameContext
from infra.engine.primitives.ellipse import Ellipse
from infra.engine.render_target import RenderTarget
from infra.engine.vector import Vector2D
from shared.colors import Color
from shared.entity_sizes import BALL_ATTACH_GAP, BALL_RADIUS, PLAYER_RADIUS


class BallPhysicsComponent(Component):
    BOUNCE_RESTITUTION = 0.75

    def __init__(self, drag: float, pitch_size: Vector2D) -> None:
        super().__init__()
        self._drag = drag
        self._pitch_size = pitch_size

    def update(self, ctx: FrameContext) -> None:
        ball = self.owner
        if not isinstance(ball, Ball):
            return

        if ball.carrier is not None:
            ball.sync_to_carrier()
            return

        next_pos = ball.pos + ball.velocity * ctx.dt
        next_pos, next_velocity = resolve_pitch_bounds(
            next_pos,
            ball.velocity,
            Ball.RADIUS,
            self._pitch_size.x,
            self._pitch_size.y,
            restitution=BallPhysicsComponent.BOUNCE_RESTITUTION,
        )
        ball.set_pos(next_pos)
        ball.set_velocity(next_velocity)

        if ball.velocity.length_squared() < 1e-6:
            ball.set_velocity(Vector2D(0, 0))
            return

        decay = math.exp(-self._drag * ctx.dt)
        ball.set_velocity(ball.velocity * decay)

        if ball.velocity.length() < 5:
            ball.set_velocity(Vector2D(0, 0))


class Ball(GameObject):
    RADIUS = BALL_RADIUS
    ATTACH_GAP = BALL_ATTACH_GAP

    def __init__(self, pos: Vector2D, drag: float, pitch_size: Vector2D):
        super().__init__(
            type=GameObjectType.CUSTOM,
            pos=pos,
        )
        self._velocity = Vector2D(0, 0)
        self._carrier: GameObject | None = None
        self.add_component(BallPhysicsComponent(drag, pitch_size))

    @property
    def velocity(self) -> Vector2D:
        return self._velocity

    @property
    def carrier(self) -> GameObject | None:
        return self._carrier

    @property
    def is_free(self) -> bool:
        return self._carrier is None

    def attach_offset(self) -> float:
        return PLAYER_RADIUS + Ball.RADIUS + Ball.ATTACH_GAP

    def attach(self, carrier: GameObject) -> None:
        self._carrier = carrier
        self._velocity = Vector2D(0, 0)
        self.sync_to_carrier()

    def detach(self) -> None:
        self._carrier = None

    def set_velocity(self, velocity: Vector2D) -> None:
        self._velocity = velocity

    def sync_to_carrier(self) -> None:
        if self._carrier is None:
            return

        forward = getattr(self._carrier, "forward", None)
        if forward is None:
            return

        self.set_pos(self._carrier.pos + forward * self.attach_offset())

    def render(self, target: RenderTarget) -> None:
        diameter = self.world_size_to_screen(
            Vector2D(Ball.RADIUS * 2, Ball.RADIUS * 2)
        ).x
        top_left = self.world_to_screen(
            Vector2D(self.pos.x - Ball.RADIUS, self.pos.y - Ball.RADIUS)
        )
        Ellipse(top_left, Vector2D(diameter, diameter), Color.YELLOW).render(target)
