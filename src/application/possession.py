from domain.ball.ball import Ball
from domain.player.player import Player
from infra.engine.vector import Vector2D


class PossessionService:
    @staticmethod
    def has_ball(player: Player, ball: Ball) -> bool:
        return ball.carrier is player

    @staticmethod
    def attach_point(player: Player, ball: Ball) -> Vector2D:
        return player.pos + player.forward * ball.attach_offset()

    @staticmethod
    def attach(player: Player, ball: Ball) -> None:
        ball.attach(player)

    @staticmethod
    def try_receive(player: Player, ball: Ball) -> bool:
        if not ball.is_free:
            return False

        distance = (ball.pos - player.pos).length()

        if player.update_pickup_block(distance):
            return False

        if distance > player.pickup_radius:
            return False

        PossessionService.attach(player, ball)
        return True

    @staticmethod
    def kick(player: Player, ball: Ball, power: float) -> None:
        if not PossessionService.has_ball(player, ball):
            return

        ball.detach()
        ball.set_velocity(player.forward * power)
        player.block_pickup_after_kick()

    @staticmethod
    def movement_speed(player: Player, ball: Ball) -> float:
        return player.movement_speed(PossessionService.has_ball(player, ball))
