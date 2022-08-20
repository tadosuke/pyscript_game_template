"""フレームモジュール."""
from __future__ import annotations

from input import OperationParam, VirtualKey, InputEvent
from values import Rect, Position, Size


class Frame:
    """矩形、親子関係を持つ抽象概念."""

    def __init__(self, rect: Rect, parent: Frame = None):
        self._rect = rect
        self._parent = parent
        if parent is not None:
            parent.append(self)

        self._children: list[Frame] = []
        self._input_event = InputEvent()

    def append(self, child: Frame) -> None:
        """子フレームを追加する."""
        if child in self._children:
            raise RuntimeError(f'Frame is already exists.')
        self._children.append(child)

    def connect_input(self, code: VirtualKey, callback: InputEvent.Callback) -> None:
        """入力コールバックを登録する."""
        self._input_event.connect(code, callback)

    def disconnect_input(self, code: VirtualKey) -> None:
        """入力コールバックの登録を解除する."""
        self._input_event.disconnect(code)

    def disconnect_input_all(self, code: VirtualKey) -> None:
        """全てのキーの入力コールバックの登録を解除する."""
        self._input_event.disconnect_all()

    def process_input(self, param: OperationParam) -> bool:
        """入力を処理する.

        :return: 処理されたか
        """

        # 子
        for frame in reversed(self._children):
            if frame.process_input(param):
                return True

        # 自分
        if not self._need_process(param):
            return False
        return self._input_event.process(param)

    def _need_process(self, param: OperationParam) -> bool:
        """処理するべき入力か."""
        position = param.position
        if position is not None:
            if not self._rect.contains_point(position):
                return False

        return True

    @property
    def rect(self) -> Rect:
        """矩形."""
        return self._rect

    @property
    def position(self) -> Position:
        return self._rect.position

    @property
    def size(self) -> Size:
        return self._rect.size

    @property
    def parent(self) -> Frame:
        """親フレーム."""
        return self._parent
