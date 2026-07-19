from enum import Enum

from infra.engine.vector import Vector2D


class PitchEdge(Enum):
    LEFT = "left"
    RIGHT = "right"
    TOP = "top"
    BOTTOM = "bottom"


class EdgeResponse(Enum):
    BOUNCE = "bounce"
    OUT_OF_PLAY = "out_of_play"


DEFAULT_EDGE_RESPONSES: dict[PitchEdge, EdgeResponse] = {
    PitchEdge.LEFT: EdgeResponse.BOUNCE,
    PitchEdge.RIGHT: EdgeResponse.BOUNCE,
    PitchEdge.TOP: EdgeResponse.BOUNCE,
    PitchEdge.BOTTOM: EdgeResponse.BOUNCE,
}


def resolve_pitch_bounds(
    pos: Vector2D,
    velocity: Vector2D,
    radius: float,
    pitch_width: float,
    pitch_height: float,
    *,
    restitution: float,
    edge_responses: dict[PitchEdge, EdgeResponse] | None = None,
) -> tuple[Vector2D, Vector2D]:
    responses = edge_responses or DEFAULT_EDGE_RESPONSES
    x = pos.x
    y = pos.y
    vx = velocity.x
    vy = velocity.y

    if x - radius < 0:
        if responses[PitchEdge.LEFT] is EdgeResponse.BOUNCE:
            x = radius
            vx = -vx * restitution
    elif x + radius > pitch_width:
        if responses[PitchEdge.RIGHT] is EdgeResponse.BOUNCE:
            x = pitch_width - radius
            vx = -vx * restitution

    if y - radius < 0:
        if responses[PitchEdge.TOP] is EdgeResponse.BOUNCE:
            y = radius
            vy = -vy * restitution
    elif y + radius > pitch_height:
        if responses[PitchEdge.BOTTOM] is EdgeResponse.BOUNCE:
            y = pitch_height - radius
            vy = -vy * restitution

    return Vector2D(x, y), Vector2D(vx, vy)
