from dataclasses import dataclass

from pygame.key import ScancodeWrapper


@dataclass(frozen=True)
class FrameContext:
    pressed_keys: ScancodeWrapper
    pressed_mouse: tuple[bool, bool, bool]
    dt: float
