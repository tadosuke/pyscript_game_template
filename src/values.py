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
