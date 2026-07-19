from collections.abc import Callable
from enum import Enum

from infra.engine.components.component import Component
from infra.engine.vector import Vector2D


class ColliderMode(Enum):
    SOLID = "solid"
    TRIGGER = "trigger"


class ColliderShape(Enum):
    CIRCLE = "circle"
    RECT = "rect"


class ColliderComponent(Component):
    def __init__(
        self,
        *,
        shape: ColliderShape = ColliderShape.CIRCLE,
        radius: float | None = None,
        size: Vector2D | None = None,
        mode: ColliderMode = ColliderMode.SOLID,
        on_enter: Callable[["ColliderComponent"], None] | None = None,
        on_exit: Callable[["ColliderComponent"], None] | None = None,
    ) -> None:
        super().__init__()
        self._shape = shape
        self._radius = radius
        self._size = size
        self._mode = mode
        self._on_enter = on_enter
        self._on_exit = on_exit
        self._overlapping: set[ColliderComponent] = set()

        if shape is ColliderShape.CIRCLE and radius is None:
            raise ValueError("Circle colliders require a radius")
        if shape is ColliderShape.RECT and size is None:
            raise ValueError("Rect colliders require a size")

    @property
    def shape(self) -> ColliderShape:
        return self._shape

    @property
    def radius(self) -> float:
        if self._radius is None:
            raise ValueError("Radius is not set")

        return self._radius

    @property
    def size(self) -> Vector2D:
        if self._size is None:
            raise ValueError("Size is not set")

        return self._size

    @property
    def mode(self) -> ColliderMode:
        return self._mode

    @property
    def pos(self) -> Vector2D:
        return self.owner.pos

    def rect_bounds(self) -> tuple[float, float, float, float]:
        pos = self.pos
        size = self.size
        return (pos.x, pos.y, pos.x + size.x, pos.y + size.y)

    def notify_enter(self, other: "ColliderComponent") -> None:
        if other in self._overlapping:
            return

        self._overlapping.add(other)
        if self._on_enter is not None:
            self._on_enter(other)

    def notify_exit(self, other: "ColliderComponent") -> None:
        if other not in self._overlapping:
            return

        self._overlapping.remove(other)
        if self._on_exit is not None:
            self._on_exit(other)
