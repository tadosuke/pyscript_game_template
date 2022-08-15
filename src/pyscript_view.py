"""ゲームビュー(pyscript)."""

from js import (
    console,
    document,
    Element,
)
from pyodide import create_proxy

from pyscript_controller import GameController
from model import GameModel


class GameView:
    """ゲームのビュー.

    :param model: ゲームモデル
    :param canvas: 描画先のCanvas
    :param controller: コントローラー
    """

    #: 背景色
    BACK_GROUND_COLOR = 'rgb(200, 200, 200)'
    #: フォントの標準色
    FONT_COLOR = 'rgb(0, 0, 0)'
    #: 画面幅
    WIDTH = 600
    #: 画面高さ
    HEIGHT = 400

    def __init__(
            self,
            model: GameModel,
            canvas: Element,
            controller: GameController) -> None:
        console.log('[GameView] Create')

        if model is None:
            raise ValueError('model is None')
        self._model = model

        self._setup_view(canvas)
        self._register_input_events(canvas, controller)

    def _setup_view(self, canvas: Element) -> None:
        """ビューの初期化."""
        if canvas is None:
            raise ValueError('canvas is None')
        canvas.width = GameView.WIDTH
        canvas.height = GameView.HEIGHT

        self._ctx = canvas.getContext('2d')
        if self._ctx is None:
            raise ValueError('ctx is None')

    @staticmethod
    def _register_input_events(canvas: Element, controller: GameController) -> None:
        """入力イベントを登録する."""
        canvas.addEventListener("mousedown", create_proxy(controller.mousedown))
        canvas.addEventListener("mouseup", create_proxy(controller.mouseup))
        canvas.addEventListener("mousemove", create_proxy(controller.mousemove))

        # キーイベントはelementでは取れないのでdocumentに登録する必要がある
        document.addEventListener("keydown", create_proxy(controller.keydown))
        document.addEventListener("keyup", create_proxy(controller.keyup))

    def draw(self) -> None:
        """描画."""
        self._clear()
        self._display_debug()

    def _clear(self) -> None:
        """画面をクリアする."""
        self._ctx.fillStyle = GameView.BACK_GROUND_COLOR
        self._ctx.fillRect(0, 0, GameView.WIDTH, GameView.HEIGHT)

    def _display_debug(self) -> None:
        """デバッグ情報を画面に描画する."""
        self._ctx.font = "10px sans-serif"
        self._ctx.fillStyle = GameView.FONT_COLOR

        y = 10
        line_h = 10

        # 経過時間
        self._ctx.fillText(f'Time={self._model.time:.1f}', 0, y)
        y += line_h

        # マウス座標
        self._ctx.fillText(f'MousePos={self._model.mouse_pos}', 0, y)
        y += line_h

