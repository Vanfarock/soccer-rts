import pygame

from application.components.ball_receiver import BallReceiverComponent
from application.components.focus_controller import FocusControllerComponent
from application.components.keyboard_controller import KeyboardControllerComponent
from application.components.movement import PlayerMovementComponent
from application.possession import PossessionService
from domain.ball.ball import Ball
from domain.pitch.pitch import Pitch
from domain.player.player import Player
from domain.team.team import Team
from infra.engine.clock import Clock
from infra.engine.components.collider import (
    ColliderComponent,
    ColliderMode,
    ColliderShape,
)
from infra.engine.engine import Engine
from infra.engine.vector import Vector2D
from infra.engine.window import Window


def _create_player(
    pos: Vector2D,
    team: Team,
    ball: Ball,
    number: int,
) -> Player:
    player = Player(pos, team, number)
    player.add_component(
        ColliderComponent(
            radius=Player.RADIUS,
            mode=ColliderMode.SOLID,
            on_exit=lambda other: print("left pitch bounds"),
            on_enter=lambda other: print("entered pitch bounds"),
        )
    )

    if team == Team.HOME:
        player.add_component(PlayerMovementComponent(speed=Player.BASE_SPEED))
        player.add_component(KeyboardControllerComponent(ball, Pitch.DRAG))
    else:
        player.add_component(BallReceiverComponent(ball))

    return player


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

        center = Vector2D(Pitch.WIDTH / 2, Pitch.HEIGHT / 2)
        ball = Ball(center, Pitch.DRAG)

        player = _create_player(center, Team.HOME, ball=ball, number=1)
        teammate = _create_player(
            Vector2D(center.x - 120, center.y),
            Team.HOME,
            ball=ball,
            number=2,
        )
        away_left = _create_player(
            Vector2D(Pitch.WIDTH * 0.75, center.y - 80),
            Team.AWAY,
            ball=ball,
            number=1,
        )
        away_right = _create_player(
            Vector2D(Pitch.WIDTH * 0.75, center.y + 80),
            Team.AWAY,
            ball=ball,
            number=2,
        )

        home_players = [player, teammate]
        focus_controller = FocusControllerComponent(ball, Team.HOME, home_players)
        focus_controller.initialize_focus(player)
        pitch.add_component(focus_controller)

        PossessionService.attach(player, ball)

        for game_object in (player, teammate, away_left, away_right, ball):
            pitch.add_child(game_object)

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
            mouse_pos = Vector2D(*pygame.mouse.get_pos())

            self._running = self._engine.update(pressed_keys, pressed_mouse, mouse_pos)
