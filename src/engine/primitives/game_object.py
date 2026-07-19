from abc import abstractmethod
from enum import Enum
from typing import TypeVar

from engine.frame_context import FrameContext
from engine.vector import Vector2D
from engine.render_target import RenderTarget
from shared.colors import Color

T = TypeVar("T", bound="Component")


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
        self._parent: GameObject | None = None
        self._children: list[GameObject] = []
        self._components: list[Component] = []

        self._validate_init()

    def add_component(self, component: T) -> T:
        if component._owner is not None:
            raise ValueError("Component is already attached to a GameObject")

        component.on_attach(self)
        self._components.append(component)
        return component

    def get_component(self, component_type: type[T]) -> T | None:
        for component in self._components:
            if isinstance(component, component_type):
                return component

        return None

    def get_components(self, component_type: type[T]) -> list[T]:
        return [
            component
            for component in self._components
            if isinstance(component, component_type)
        ]

    def require_component(self, component_type: type[T]) -> T:
        component = self.get_component(component_type)
        if component is None:
            raise ValueError(f"GameObject is missing required component: {component_type.__name__}")

        return component

    def set_pos(self, pos: Vector2D) -> None:
        self._pos = pos

    def update_tree(self, ctx: FrameContext) -> None:
        for component in self._components:
            component.update(ctx)

        for child in self._children:
            child.update_tree(ctx)

    def iter_tree(self):
        yield self
        for child in self._children:
            yield from child.iter_tree()

    def add_child(self, child: GameObject) -> None:
        if child._parent is self:
            return

        if child._parent is not None:
            child._parent._children.remove(child)

        child._parent = self
        self._children.append(child)

    def set_transform(self, scale: float, offset: Vector2D) -> None:
        self._scale = scale
        self._offset = offset

    def _effective_transform(self) -> tuple[float, Vector2D]:
        if self._parent is None:
            return self._scale, self._offset

        parent_scale, parent_offset = self._parent._effective_transform()
        return (
            parent_scale * self._scale,
            parent_offset + self._offset * parent_scale,
        )

    def world_to_screen(self, pos: Vector2D) -> Vector2D:
        scale, offset = self._effective_transform()
        return Vector2D(
            offset.x + pos.x * scale,
            offset.y + pos.y * scale,
        )

    def screen_to_world(self, pos: Vector2D) -> Vector2D:
        scale, offset = self._effective_transform()
        return Vector2D(
            (pos.x - offset.x) / scale,
            (pos.y - offset.y) / scale,
        )

    def world_size_to_screen(self, size: Vector2D) -> Vector2D:
        scale, _ = self._effective_transform()
        return Vector2D(size.x * scale, size.y * scale)

    def render_tree(self, target: RenderTarget) -> None:
        self.render(target)
        for child in self._children:
            child.render_tree(target)

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


from engine.components.component import Component  # noqa: E402
