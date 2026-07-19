from typing import ClassVar


class Color:
    BLACK: ClassVar["Color"]
    WHITE: ClassVar["Color"]
    RED: ClassVar["Color"]
    GREEN: ClassVar["Color"]
    BLUE: ClassVar["Color"]
    YELLOW: ClassVar["Color"]
    PURPLE: ClassVar["Color"]
    ORANGE: ClassVar["Color"]
    PINK: ClassVar["Color"]
    BROWN: ClassVar["Color"]
    GRAY: ClassVar["Color"]
    LIGHT_GRAY: ClassVar["Color"]

    PITCH_BG: ClassVar["Color"]
    PITCH_SURFACE: ClassVar["Color"]

    TEAM_HOME: ClassVar["Color"]
    TEAM_AWAY: ClassVar["Color"]

    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b

    def to_tuple(self) -> tuple[int, int, int]:
        return (self.r, self.g, self.b)


Color.BLACK = Color(0, 0, 0)
Color.WHITE = Color(255, 255, 255)
Color.RED = Color(255, 0, 0)
Color.GREEN = Color(0, 255, 0)
Color.BLUE = Color(0, 0, 255)
Color.YELLOW = Color(255, 255, 0)
Color.PURPLE = Color(128, 0, 128)
Color.ORANGE = Color(255, 165, 0)
Color.PINK = Color(255, 192, 203)
Color.BROWN = Color(165, 42, 42)
Color.GRAY = Color(128, 128, 128)
Color.LIGHT_GRAY = Color(200, 200, 200)
Color.PITCH_BG = Color(24, 32, 48)
Color.PITCH_SURFACE = Color(34, 48, 64)
Color.TEAM_HOME = Color(65, 105, 225)
Color.TEAM_AWAY = Color(220, 53, 69)
