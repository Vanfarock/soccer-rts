from engine.primitives.ellipse import Ellipse
from engine.primitives.game_object import GameObject, GameObjectType
from engine.render_target import RenderTarget
from engine.vector import Vector2D
from team.team import Team


class Player(GameObject):
    RADIUS = 8

    def __init__(self, pos: Vector2D, team: Team):
        super().__init__(
            type=GameObjectType.CUSTOM,
            pos=pos,
        )
        self._team = team

    def render(self, target: RenderTarget) -> None:
        diameter = self.world_size_to_screen(
            Vector2D(Player.RADIUS * 2, Player.RADIUS * 2)
        ).x
        top_left = self.world_to_screen(
            Vector2D(self.pos.x - Player.RADIUS, self.pos.y - Player.RADIUS)
        )
        Ellipse(top_left, Vector2D(diameter, diameter), self._team.color).render(target)
