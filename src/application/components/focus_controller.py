import pygame

from application.components.keyboard_controller import KeyboardControllerComponent
from domain.ball.ball import Ball
from domain.player.player import Player
from domain.team.team import Team
from infra.engine.components.component import Component
from infra.engine.frame_context import FrameContext

_NUMBER_KEYS: dict[int, int] = {
    pygame.K_1: 1,
    pygame.K_2: 2,
    pygame.K_3: 3,
    pygame.K_4: 4,
    pygame.K_5: 5,
    pygame.K_6: 6,
    pygame.K_7: 7,
    pygame.K_8: 8,
    pygame.K_9: 9,
    pygame.K_0: 0,
}


class FocusControllerComponent(Component):
    def __init__(self, ball: Ball, my_team: Team, roster: list[Player]) -> None:
        super().__init__()
        self._ball = ball
        self._my_team = my_team
        self._roster = roster
        self._focused: Player | None = None
        self._prev_tab = False
        self._prev_numbers = {key: False for key in _NUMBER_KEYS}

    @property
    def active_player(self) -> Player | None:
        carrier = self._ball.carrier
        if isinstance(carrier, Player):
            return carrier
        return None

    @property
    def focused_player(self) -> Player | None:
        return self._focused

    def initialize_focus(self, player: Player) -> None:
        self.set_focus(player)

    def set_focus(self, player: Player | None) -> None:
        if player is not None and player.team != self._my_team:
            return

        if self._focused is player:
            return

        if self._focused is not None:
            self._focused.set_focused(False)
            controller = self._focused.get_component(KeyboardControllerComponent)
            if controller is not None:
                controller.clear_charge()

        self._focused = player

        if player is not None:
            player.set_focused(True)

    def update(self, ctx: FrameContext) -> None:
        tab_pressed = ctx.pressed_keys[pygame.K_TAB]
        if tab_pressed and not self._prev_tab:
            active = self.active_player
            if active is not None and active.team == self._my_team:
                self.set_focus(active)

        for key, number in _NUMBER_KEYS.items():
            pressed = ctx.pressed_keys[key]
            if pressed and not self._prev_numbers[key]:
                for player in self._roster:
                    if player.number == number:
                        self.set_focus(player)
                        break
            self._prev_numbers[key] = pressed

        self._prev_tab = tab_pressed
