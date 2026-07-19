import pygame

from engine.clock import Clock
from engine.components.collider import ColliderComponent, ColliderMode, ColliderShape
from engine.components.movable import MovableComponent
from engine.engine import Engine
from engine.vector import Vector2D
from engine.window import Window
from pitch.pitch import Pitch
from player.player import Player
from team.team import Team


class Game:
    def __init__(self):
        window = Window()
        self._engine = Engine(
            window=window,
            clock=Clock(fps=60),
            antialiasing=True,
            aa_factor=2,
        )

        pitch = Pitch(window)
        pitch.add_component(
            ColliderComponent(
                shape=ColliderShape.RECT,
                size=Vector2D(Pitch.WIDTH, Pitch.HEIGHT),
                mode=ColliderMode.TRIGGER,
            )
        )

        player = Player(
            Vector2D(Pitch.WIDTH / 2, Pitch.HEIGHT / 2),
            Team.HOME,
        )
        player.add_component(MovableComponent(speed=200))
        player.add_component(
            ColliderComponent(
                radius=Player.RADIUS,
                mode=ColliderMode.SOLID,
                on_exit=lambda other: print("left pitch bounds"),
                on_enter=lambda other: print("entered pitch bounds"),
            )
        )
        pitch.add_child(player)

        self._engine.add_game_object(pitch)

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
