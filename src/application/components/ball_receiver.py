from application.possession import PossessionService
from domain.ball.ball import Ball
from domain.player.player import Player
from infra.engine.components.component import Component
from infra.engine.frame_context import FrameContext


class BallReceiverComponent(Component):
    def __init__(self, ball: Ball) -> None:
        super().__init__()
        self._ball = ball

    def update(self, ctx: FrameContext) -> None:
        owner = self.owner
        if isinstance(owner, Player):
            PossessionService.try_receive(owner, self._ball)
