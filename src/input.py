"""入力モジュール."""

import typing as tp
from dataclasses import dataclass
from enum import Enum, auto

from values import Position


class VirtualKey(Enum):
    """抽象キー."""
    Dummy = auto()

    MouseLeft = auto()
    MouseMiddle = auto()
    MouseRight = auto()
    MouseBack = auto()
    MouseNext = auto()
    MouseMove = auto()

    Enter = auto()
    Escape = auto()
    Space = auto()
    Control = auto()
    Shift = auto()
    Alt = auto()
    BackSpace = auto()

    Up = auto()
    Down = auto()
    Left = auto()
    Right = auto()

    A = auto()
    B = auto()
    C = auto()
    D = auto()
    E = auto()
    F = auto()
    G = auto()
    H = auto()
    I = auto()
    J = auto()
    K = auto()
    L = auto()
    M = auto()
    N = auto()
    O = auto()
    P = auto()
    Q = auto()
    R = auto()
    S = auto()
    T = auto()
    U = auto()
    V = auto()
    W = auto()
    X = auto()
    Y = auto()
    Z = auto()

    T0 = auto()
    T1 = auto()
    T2 = auto()
    T3 = auto()
    T4 = auto()
    T5 = auto()
    T6 = auto()
    T7 = auto()
    T8 = auto()
    T9 = auto()

    Num0 = auto()
    Num1 = auto()
    Num2 = auto()
    Num3 = auto()
    Num4 = auto()
    Num5 = auto()
    Num6 = auto()
    Num7 = auto()
    Num8 = auto()
    Num9 = auto()


class InputState(Enum):
    """入力状態."""
    #: 押された
    Press = auto()
    #: 離された
    Release = auto()
    #: リピートされた
    Repeat = auto()


@dataclass
class OperationParam:
    """operateに渡すパラメーター."""
    code: VirtualKey
    state: InputState
    position: tp.Optional[Position] = None

    def is_press(self) -> bool:
        """押されているか."""
        return self.state == InputState.Press

    def is_release(self) -> bool:
        """離されたか."""
        return self.state == InputState.Release

    def is_repeat(self) -> bool:
        """リピートされたか."""
        return self.state == InputState.Repeat


class InputEvent:
    """入力イベント."""

    #: 入力イベントに対するコールバック
    Callback = tp.Callable[[OperationParam], bool]
    #: 入力コールバック辞書
    CallbackDict = dict[VirtualKey, Callback]

    def __init__(self):
        self._callback_dict: InputEvent.CallbackDict = {}

    def process(self, param: OperationParam) -> bool:
        """入力を処理する.

        :param param: 入力情報
        :return: 処理されたか
        """
        callback = self._callback_dict.get(param.code)
        if callback is None:
            return False
        processed = callback(param)
        return processed

    def connect(self, code: VirtualKey, callback: Callback) -> None:
        """コールバックを登録する.

        :param code: 抽象キー
        :param callback: 抽象キーが押された際に呼ばれるコールバック
        """
        if code in self._callback_dict.keys():
            raise ValueError(f'code({code}) is already registered.')
        self._callback_dict[code] = callback

    def disconnect(self, code: VirtualKey) -> None:
        """コールバックの登録を解除する.

        :param code: 抽象キー
        """
        del self._callback_dict[code]

    def disconnect_all(self) -> None:
        """全てのキーのコールバック登録を解除する."""
        self._callback_dict.clear()
