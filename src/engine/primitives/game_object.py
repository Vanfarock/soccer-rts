from abc import abstractmethod
from enum import Enum

from engine.vector import Vector2D
from engine.render_target import RenderTarget
from shared.colors import Color


class GameObjectType(Enum):
    RECTANGLE = "rectangle"
    LINE = "line"
    ELLIPSE = "ellipse"
    ARC = "arc"
    CUSTOM = "custom"


class GameObject:
    def __init__(
        self,
        *,
        type: GameObjectType,
        pos: Vector2D,
        size: Vector2D | None = None,
        thickness: float | None = None,
        color: Color | None = None,
        border_radius: float | None = None,
    ):
        self._type = type
        self._pos = pos
        self._size = size
        self._thickness = thickness
        self._color = color
        self._border_radius = border_radius
        self._scale = 1.0
        self._offset = Vector2D(0, 0)

        self._validate_init()

    def set_transform(self, scale: float, offset: Vector2D) -> None:
        self._scale = scale
        self._offset = offset

    def world_to_screen(self, pos: Vector2D) -> Vector2D:
        return Vector2D(
            self._offset.x + pos.x * self._scale,
            self._offset.y + pos.y * self._scale,
        )

    def screen_to_world(self, pos: Vector2D) -> Vector2D:
        return Vector2D(
            (pos.x - self._offset.x) / self._scale,
            (pos.y - self._offset.y) / self._scale,
        )

    def world_size_to_screen(self, size: Vector2D) -> Vector2D:
        return Vector2D(size.x * self._scale, size.y * self._scale)

    def _validate_init(self) -> None:
        if (
            self._type
            in (
                GameObjectType.RECTANGLE,
                GameObjectType.LINE,
                GameObjectType.ELLIPSE,
                GameObjectType.ARC,
            )
            and self._color is None
        ):
            raise ValueError("Color is required for drawable primitives")

    @property
    def type(self) -> GameObjectType:
        return self._type

    @property
    def pos(self) -> Vector2D:
        return self._pos

    @property
    def size(self) -> Vector2D:
        if self._size is None:
            raise ValueError("Size is not set")

        return self._size

    @property
    def thickness(self) -> float:
        if self._thickness is None:
            raise ValueError("Thickness is not set")

        return self._thickness

    @property
    def color(self) -> Color:
        if self._color is None:
            raise ValueError("Color is not set")

        return self._color

    @property
    def border_radius(self) -> float:
        if self._border_radius is None:
            raise ValueError("Border radius is not set")

        return self._border_radius

    @abstractmethod
    def render(self, target: RenderTarget) -> None:
        pass
