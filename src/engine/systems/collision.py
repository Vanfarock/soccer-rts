import math

from engine.components.collider import ColliderComponent, ColliderMode, ColliderShape
from engine.primitives.game_object import GameObject
from engine.vector import Vector2D


class CollisionSystem:
    @staticmethod
    def step(roots: list[GameObject]) -> None:
        colliders = [
            component
            for game_object in _iter_tree(roots)
            for component in game_object.get_components(ColliderComponent)
        ]

        _resolve_solids(colliders)
        _update_triggers(colliders)


def _iter_tree(roots: list[GameObject]):
    for root in roots:
        yield from root.iter_tree()


def _resolve_solids(colliders: list[ColliderComponent]) -> None:
    solids = [c for c in colliders if c.mode is ColliderMode.SOLID]

    for index, first in enumerate(solids):
        for second in solids[index + 1 :]:
            if not _overlaps(first, second):
                continue

            if first.shape is ColliderShape.CIRCLE and second.shape is ColliderShape.CIRCLE:
                _resolve_circle_circle(first, second)
            elif first.shape is ColliderShape.CIRCLE and second.shape is ColliderShape.RECT:
                _resolve_circle_rect(first, second)
            elif first.shape is ColliderShape.RECT and second.shape is ColliderShape.CIRCLE:
                _resolve_circle_rect(second, first)


def _update_triggers(colliders: list[ColliderComponent]) -> None:
    triggers = [c for c in colliders if c.mode is ColliderMode.TRIGGER]
    solids = [c for c in colliders if c.mode is ColliderMode.SOLID]

    for trigger in triggers:
        current: set[ColliderComponent] = set()

        for solid in solids:
            if solid.owner is trigger.owner:
                continue
            if _overlaps(trigger, solid):
                current.add(solid)

        for solid in current - trigger._overlapping:
            trigger.notify_enter(solid)
            solid.notify_enter(trigger)

        for solid in trigger._overlapping - current:
            trigger.notify_exit(solid)
            solid.notify_exit(trigger)


def _overlaps(first: ColliderComponent, second: ColliderComponent) -> bool:
    if first.shape is ColliderShape.CIRCLE and second.shape is ColliderShape.CIRCLE:
        return _circle_circle_overlap(first, second)
    if first.shape is ColliderShape.CIRCLE and second.shape is ColliderShape.RECT:
        return _circle_rect_overlap(first, second)
    if first.shape is ColliderShape.RECT and second.shape is ColliderShape.CIRCLE:
        return _circle_rect_overlap(second, first)

    return False


def _circle_circle_overlap(first: ColliderComponent, second: ColliderComponent) -> bool:
    delta = second.pos - first.pos
    distance_sq = delta.x**2 + delta.y**2
    radius_sum = first.radius + second.radius
    return distance_sq <= radius_sum**2


def _circle_rect_overlap(circle: ColliderComponent, rect: ColliderComponent) -> bool:
    left, top, right, bottom = rect.rect_bounds()
    closest_x = _clamp(circle.pos.x, left, right)
    closest_y = _clamp(circle.pos.y, top, bottom)
    delta_x = circle.pos.x - closest_x
    delta_y = circle.pos.y - closest_y
    return delta_x**2 + delta_y**2 <= circle.radius**2


def _resolve_circle_circle(first: ColliderComponent, second: ColliderComponent) -> None:
    delta = second.pos - first.pos
    distance = math.hypot(delta.x, delta.y)
    overlap = (first.radius + second.radius) - distance

    if overlap <= 0:
        return

    if distance == 0:
        separation = Vector2D(1, 0)
    else:
        separation = Vector2D(delta.x / distance, delta.y / distance)

    half = overlap / 2
    first.owner.set_pos(first.owner.pos - separation * half)
    second.owner.set_pos(second.owner.pos + separation * half)


def _resolve_circle_rect(circle: ColliderComponent, rect: ColliderComponent) -> None:
    left, top, right, bottom = rect.rect_bounds()
    closest_x = _clamp(circle.pos.x, left, right)
    closest_y = _clamp(circle.pos.y, top, bottom)
    delta = circle.pos - Vector2D(closest_x, closest_y)
    distance = math.hypot(delta.x, delta.y)

    if distance == 0:
        penetration_left = circle.pos.x - left
        penetration_right = right - circle.pos.x
        penetration_top = circle.pos.y - top
        penetration_bottom = bottom - circle.pos.y
        min_penetration = min(
            penetration_left,
            penetration_right,
            penetration_top,
            penetration_bottom,
        )

        if min_penetration is penetration_left:
            circle.owner.set_pos(Vector2D(left - circle.radius, circle.pos.y))
        elif min_penetration is penetration_right:
            circle.owner.set_pos(Vector2D(right + circle.radius, circle.pos.y))
        elif min_penetration is penetration_top:
            circle.owner.set_pos(Vector2D(circle.pos.x, top - circle.radius))
        else:
            circle.owner.set_pos(Vector2D(circle.pos.x, bottom + circle.radius))
        return

    overlap = circle.radius - distance
    if overlap <= 0:
        return

    separation = Vector2D(delta.x / distance, delta.y / distance)
    circle.owner.set_pos(circle.owner.pos + separation * overlap)


def _clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(value, maximum))
