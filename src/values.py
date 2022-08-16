"""値オブジェクトたち."""

from dataclasses import dataclass


@dataclass
class Position:
    """座標."""
    x: float = 0
    y: float = 0

    def __str__(self):
        return f'({self.x}, {self.y})'


@dataclass
class Size:
    """サイズ."""
    width: int
    height: int


@dataclass
class Rect:
    """矩形."""
    position: Position
    size: Size

    @property
    def left(self) -> float:
        return self.position.x

    @property
    def right(self) -> float:
        return self.position.x + self.size.width

    @property
    def top(self) -> float:
        return self.position.y

    @property
    def bottom(self) -> float:
        return self.position.y + self.size.height

    @property
    def center(self) -> Position:
        x = self.position.x + self.size.width/2
        y = self.position.y + self.size.height/2
        return Position(x, y)

    def contains_point(self, point: Position) -> bool:
        """指定した点を含むか."""
        is_x = self.left <= point.x <= self.right
        is_y = self.top <= point.y <= self.bottom
        return is_x and is_y


class Color:
    """色."""

    def __init__(self, r: int, g: int, b: int, a: int = 255):
        if r < 0 or 255 < r:
            raise ValueError()
        if g < 0 or 255 < g:
            raise ValueError()
        if b < 0 or 255 < b:
            raise ValueError()
        if r < 0 or 255 < r:
            raise ValueError()

        self._r = r
        self._g = g
        self._b = b
        self._a = a

    @property
    def r(self) -> int:
        return self._r

    @property
    def g(self) -> int:
        return self._g

    @property
    def b(self) -> int:
        return self._b

    @property
    def a(self) -> int:
        return self._a

