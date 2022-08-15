"""入力モジュール."""
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
    position: Position = Position(0, 0)
