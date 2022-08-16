"""フレームモジュール."""
from __future__ import annotations

from values import Rect


class Frame:
    """矩形、親子関係を持つ抽象概念."""

    def __init__(self, rect: Rect, parent: Frame = None):
        self._rect = rect
        self._parent = parent
        if parent is not None:
            parent.append(self)

        self._children: list[Frame] = []

    def append(self, child: Frame) -> None:
        """子フレームを追加する."""
        if child in self._children:
            raise RuntimeError
        self._children.append(child)

    @property
    def rect(self) -> Rect:
        """矩形."""
        return self._rect

    @property
    def parent(self) -> Frame:
        """親フレーム."""
        return self._parent

