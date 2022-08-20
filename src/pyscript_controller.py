"""ゲームコントローラー(pyscript).

html側の入力イベントを抽象コードに変換してModelに渡す.
"""

from js import (
    document,
    console,
    Element,
    MouseEvent,
    KeyboardEvent,
)
from pyodide import create_proxy

from model import GameModel
from view import GameView
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
    """ゲームのコントローラー.

    :param model: モデル
    :param canvas: 入力イベントを登録するためのCanvas
    """

    def __init__(self, model: GameModel, view: GameView, canvas: Element) -> None:
        console.log('[GameController] Create')

        if model is None:
            raise ValueError('model is None')
        self._model = model

        if view is None:
            raise ValueError('view is None')
        self._view = view

        if canvas is None:
            raise ValueError('canvas is None')
        self._register_input_events(canvas)

    def mousedown(self, event: MouseEvent) -> None:
        """マウスボタンが押された."""
        virtual_key = MOUSE_BUTTON_TO_VK_DICT[event.button]
        param = OperationParam(
            code=virtual_key,
            state=InputState.Press,
            position=Position(event.x, event.y))
        self._send_operation(param)

    def mouseup(self, event: MouseEvent) -> None:
        """マウスボタンが離された."""
        virtual_key = MOUSE_BUTTON_TO_VK_DICT[event.button]
        param = OperationParam(
            code=virtual_key,
            state=InputState.Release,
            position=Position(event.x, event.y))
        self._send_operation(param)

    def mousemove(self, event: MouseEvent) -> None:
        """マウスカーソルが移動した."""
        param = OperationParam(
            code=VirtualKey.MouseMove,
            state=InputState.Press,
            position=Position(event.x, event.y))
        self._send_operation(param)

    def keydown(self, event: KeyboardEvent) -> None:
        """キーが押された."""
        virtual_key = key_to_vk(event.key)
        if event.repeat:
            state = InputState.Repeat
        else:
            console.log(f'[GameController] keydown(key={event.key} -> VK={virtual_key})')
            state = InputState.Press
        param = OperationParam(code=virtual_key, state=state)
        self._send_operation(param)

    def keyup(self, event: KeyboardEvent) -> None:
        """キーが離された."""
        virtual_key = key_to_vk(event.key)
        param = OperationParam(code=virtual_key, state=InputState.Release)
        self._send_operation(param)

    def _send_operation(self, param: OperationParam):
        self._view.operate(param)
        self._model.operate(param)


    def _register_input_events(self, canvas: Element) -> None:
        """入力イベントを登録する."""
        canvas.addEventListener("mousedown", create_proxy(self.mousedown))
        canvas.addEventListener("mouseup", create_proxy(self.mouseup))
        canvas.addEventListener("mousemove", create_proxy(self.mousemove))

        # キーイベントはelementでは取れないのでdocumentに登録する必要がある
        document.addEventListener("keydown", create_proxy(self.keydown))
        document.addEventListener("keyup", create_proxy(self.keyup))
