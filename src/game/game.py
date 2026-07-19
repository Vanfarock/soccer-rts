import pygame

from engine.clock import Clock
from engine.engine import Engine
from engine.window import Window
from pitch.pitch import Pitch


class Game:
    def __init__(self):
        window = Window()
        self._engine = Engine(
            window=window,
            clock=Clock(fps=60),
            antialiasing=True,
            aa_factor=2,
        )
        self._engine.add_game_object(Pitch(window))

        self._running = True

    def run(self):
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    continue

            pressed_keys = pygame.key.get_pressed()
            pressed_mouse = pygame.mouse.get_pressed()

            self._running = self._engine.update(pressed_keys, pressed_mouse)
