"""ゲームビュー(pyscript)."""

from js import (
    console,
    document,
    Element,
)

from model import GameModel


class GameView:
    """ゲームのビュー.

    :param model: ゲームモデル
    :param canvas: 描画先のCanvas
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
            canvas: Element) -> None:
        console.log('[GameView] Create')

        if model is None:
            raise ValueError('model is None')
        self._model = model

        if canvas is None:
            raise ValueError('canvas is None')
        self._canvas = canvas
        self._setup_canvas()
        self._ctx = canvas.getContext('2d')

    @property
    def canvas(self) -> Element:
        """Canvas."""
        return self._canvas

    def _setup_canvas(self) -> None:
        """ビューの初期化."""
        self._canvas.width = GameView.WIDTH
        self._canvas.height = GameView.HEIGHT

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

