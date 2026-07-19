from enum import Enum

from shared.colors import Color

_TEAM_COLORS: dict[str, Color] = {
    "home": Color(65, 105, 225),
    "away": Color(220, 53, 69),
}


class Team(Enum):
    HOME = "home"
    AWAY = "away"

    @property
    def color(self) -> Color:
        return _TEAM_COLORS[self.value]
