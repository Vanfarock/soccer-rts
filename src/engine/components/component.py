from __future__ import annotations

from typing import TYPE_CHECKING

from engine.frame_context import FrameContext

if TYPE_CHECKING:
    from engine.primitives.game_object import GameObject


class Component:
    def __init__(self) -> None:
        self._owner: GameObject | None = None

    @property
    def owner(self) -> GameObject:
        if self._owner is None:
            raise RuntimeError("Component is not attached to a GameObject")

        return self._owner

    def on_attach(self, owner: GameObject) -> None:
        self._owner = owner

    def on_detach(self) -> None:
        self._owner = None

    def update(self, ctx: FrameContext) -> None:
        pass
