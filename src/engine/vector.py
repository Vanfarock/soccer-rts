class Vector2D:
    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    def __add__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self._x + other._x, self._y + other._y)

    def __sub__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self._x - other._x, self._y - other._y)

    def __mul__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self._x * other._x, self._y * other._y)

    def __truediv__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self._x / other._x, self._y / other._y)

    def __floordiv__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self._x // other._x, self._y // other._y)

    def to_tuple(self) -> tuple[float, float]:
        return (self._x, self._y)
