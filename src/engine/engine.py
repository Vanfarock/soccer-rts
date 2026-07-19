import pygame
from pygame.key import ScancodeWrapper

from engine.clock import Clock
from engine.primitives.game_object import GameObject
from engine.render_layer import RenderLayer
from engine.vector import Vector2D
from engine.window import Window


class Engine:
    def __init__(
        self,
        window: Window,
        clock: Clock,
        *,
        antialiasing: bool = True,
        aa_factor: int = 2,
    ):
        self._window = window
        self._clock = clock
        self._antialiasing = antialiasing
        self._aa_factor = aa_factor

        self._game_objects: list[GameObject] = []

    def add_game_object(self, game_object: GameObject):
        self._game_objects.append(game_object)

    def remove_game_object(self, game_object: GameObject):
        self._game_objects.remove(game_object)

    def _render_to(self, target) -> None:
        for game_object in self._game_objects:
            game_object.render_tree(target)

    def update(
        self, pressed_keys: ScancodeWrapper, pressed_mouse: tuple[bool, bool, bool]
    ) -> bool:
        if pressed_keys[pygame.K_ESCAPE]:
            return False

        screen_width, screen_height = self._window.screen.get_size()

        if self._antialiasing and self._aa_factor > 1:
            layer = RenderLayer(
                screen_width * self._aa_factor,
                screen_height * self._aa_factor,
                pixel_scale=self._aa_factor,
            )
            self._render_to(layer)
            layer.blit_scaled_to(
                self._window,
                Vector2D(0, 0),
                Vector2D(screen_width, screen_height),
            )
        else:
            self._render_to(self._window)

        pygame.display.flip()
        self._clock.tick()

        return True
