from dataclasses import dataclass

from pygame.key import ScancodeWrapper

from infra.engine.vector import Vector2D


@dataclass(frozen=True)
class FrameContext:
    pressed_keys: ScancodeWrapper
    pressed_mouse: tuple[bool, bool, bool]
    mouse_pos: Vector2D
    dt: float
