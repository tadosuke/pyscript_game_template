"""ゲームコントローラー(pyscript).

html側の入力イベントをGameModel側の抽象コードに変換する.
"""

from js import (
    console,
    MouseEvent,
    KeyboardEvent,
)

from model import GameModel
from values import Position
from input import VirtualKey, InputState, OperationParam


# マウスボタン→抽象キーへの変換テーブル
MOUSE_BUTTON_TO_VK_DICT = {
    0: VirtualKey.MouseLeft,
    1: VirtualKey.MouseMiddle,
    2: VirtualKey.MouseRight,
    3: VirtualKey.MouseBack,
    4: VirtualKey.MouseNext
}

# キー→抽象キーへの変換テーブル
KEY_TO_VK_DICT = {
    "Enter": VirtualKey.Enter,
    "Escape": VirtualKey.Escape,
    " ": VirtualKey.Space,
    "Control": VirtualKey.Control,
    "Shift": VirtualKey.Shift,
    "Alt": VirtualKey.Alt,
    "Backspace": VirtualKey.BackSpace,

    "ArrowUp": VirtualKey.Up,
    "ArrowDown": VirtualKey.Down,
    "ArrowLeft": VirtualKey.Left,
    "ArrowRight": VirtualKey.Right,

    "a": VirtualKey.A,
    "b": VirtualKey.B,
    "c": VirtualKey.C,
    "d": VirtualKey.D,
    "e": VirtualKey.E,
    "f": VirtualKey.F,
    "g": VirtualKey.G,
    "h": VirtualKey.H,
    "i": VirtualKey.I,
    "j": VirtualKey.J,
    "k": VirtualKey.K,
    "l": VirtualKey.L,
    "m": VirtualKey.M,
    "n": VirtualKey.N,
    "o": VirtualKey.O,
    "p": VirtualKey.P,
    "q": VirtualKey.Q,
    "r": VirtualKey.R,
    "s": VirtualKey.S,
    "t": VirtualKey.T,
    "u": VirtualKey.U,
    "v": VirtualKey.V,
    "w": VirtualKey.W,
    "x": VirtualKey.X,
    "y": VirtualKey.Y,
    "z": VirtualKey.Z,

    "0": VirtualKey.T0,
    "1": VirtualKey.T1,
    "2": VirtualKey.T2,
    "3": VirtualKey.T3,
    "4": VirtualKey.T4,
    "5": VirtualKey.T5,
    "6": VirtualKey.T6,
    "7": VirtualKey.T7,
    "8": VirtualKey.T8,
    "9": VirtualKey.T9,
}


def key_to_vk(key) -> VirtualKey:
    """キーを抽象キーに変換する.

    :return: 抽象キー。登録されていないキーはVirtualKey.Dummy
    """
    if key not in KEY_TO_VK_DICT:
        return VirtualKey.Dummy
    return KEY_TO_VK_DICT[key]


class GameController:
    """ゲームのコントローラー."""

    def __init__(self, model: GameModel) -> None:
        print('[GameController] Create')

        if model is None:
            raise ValueError('model is None')
        self._model = model

    def mousedown(self, event: MouseEvent) -> None:
        """マウスボタンが押された."""
        virtual_key = MOUSE_BUTTON_TO_VK_DICT[event.button]
        param = OperationParam(code=virtual_key, state=InputState.Press)
        self._model.operate(param)

    def mouseup(self, event: MouseEvent) -> None:
        """マウスボタンが離された."""
        virtual_key = MOUSE_BUTTON_TO_VK_DICT[event.button]
        param = OperationParam(code=virtual_key, state=InputState.Release)
        self._model.operate(param)

    def mousemove(self, event: MouseEvent) -> None:
        """マウスカーソルが移動した."""
        param = OperationParam(
            code=VirtualKey.MouseMove,
            state=InputState.Press,
            position=Position(event.x, event.y))
        self._model.operate(param)

    def keydown(self, event: KeyboardEvent) -> None:
        """キーが押された."""
        virtual_key = key_to_vk(event.key)
        if event.repeat:
            state = InputState.Repeat
        else:
            console.log(f'[GameController] keydown(key={event.key} -> VK={virtual_key})')
            state = InputState.Press
        param = OperationParam(code=virtual_key, state=state)
        self._model.operate(param)

    def keyup(self, event: KeyboardEvent) -> None:
        """キーが離された."""
        virtual_key = key_to_vk(event.key)
        param = OperationParam(code=virtual_key, state=InputState.Release)
        self._model.operate(param)
