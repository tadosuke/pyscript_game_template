"""フレームモジュール."""
from __future__ import annotations

import typing as tp
from values import Rect, Position, Size
from input import OperationParam, VirtualKey

#: 入力イベントに対するコールバック
InputCallback = tp.Callable[[OperationParam], bool]
#: 入力コールバック辞書
InputCallbackDict = dict[VirtualKey, InputCallback]


class Frame:
    """矩形、親子関係を持つ抽象概念."""

    def __init__(self, rect: Rect, parent: Frame = None):
        self._rect = rect
        self._parent = parent
        if parent is not None:
            parent.append(self)

        self._children: list[Frame] = []
        self._input_callback: InputCallbackDict = dict()

    def append(self, child: Frame) -> None:
        """子フレームを追加する."""
        if child in self._children:
            raise RuntimeError(f'Frame is already exists.')
        self._children.append(child)

    def connect_input(self, code: VirtualKey, callback: InputCallback):
        """入力コールバックを登録する."""
        if code in self._input_callback.keys():
            raise ValueError(f'code({code}) is already registered.')
        self._input_callback[code] = callback

    def disconnect_input(self, code: VirtualKey):
        """入力コールバックの登録を解除する."""
        del self._input_callback[code]

    def process_input(self, param: OperationParam) -> bool:
        """入力を処理する.

        :return: 処理されたか
        """

        # 子
        for frame in reversed(self._children):
            if frame.process_input(param):
                return True

        # 自分
        callback = self._input_callback.get(param.code)
        if callback is None:
            return False
        processed = callback(param)
        return processed

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
