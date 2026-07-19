from enum import Enum

from shared.colors import Color

_TEAM_COLORS: dict[str, Color] = {
    "home": Color.TEAM_HOME,
    "away": Color.TEAM_AWAY,
}


class Team(Enum):
    HOME = "home"
    AWAY = "away"

    @property
    def color(self) -> Color:
        return _TEAM_COLORS[self.value]
