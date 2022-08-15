"""ゲームビュー(pyscript)."""
import math

from js import (
    console,
    Element,
    CanvasRenderingContext2D,
)

from model import GameModel
from values import *


def draw_line(ctx: CanvasRenderingContext2D, start_pos: tuple[int, int], end_pos: tuple[int, int], stroke_style: str) -> None:
    """線の描画."""
    ctx.beginPath()
    ctx.strokeStyle = stroke_style
    ctx.moveTo(*start_pos)
    ctx.lineTo(*end_pos)
    ctx.stroke()
    ctx.closePath()


def draw_circle(ctx: CanvasRenderingContext2D, center: tuple[int, int], radius: int, fill_style: str) -> None:
    """円の描画."""
    angle_start = 0 * math.pi / 180
    angle_end = 360 * math.pi / 180

    (x, y) = center
    ctx.beginPath()
    ctx.fillStyle = fill_style
    ctx.arc(x, y, radius, angle_start, angle_end)
    ctx.fill()
    ctx.closePath()


def draw_text(ctx: CanvasRenderingContext2D, text: str, position: tuple[int, int], font: str, fill_style: str) -> None:
    """テキストの描画."""
    (x, y) = position
    text = text
    ctx.font = font
    ctx.fillStyle = fill_style
    ctx.fillText(text, x, y)


def draw_rect(ctx: CanvasRenderingContext2D, rect: Rect, fill_style: str) -> None:
    """矩形の描画."""
    ctx.fillStyle = fill_style
    ctx.fillRect(rect.position.x, rect.position.y, rect.size.width, rect.size.height)


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

        draw_line(
            self._ctx,
            start_pos=(100, 100),
            end_pos=(200, 120),
            stroke_style='rgb(200, 0, 0)')

        draw_circle(
            self._ctx,
            center=(200, 200),
            radius=50,
            fill_style='rgb(0, 0, 200)')

        draw_text(
            self._ctx,
            text='GameTemplate',
            position=(50, 300),
            font='48px bold serif',
            fill_style='rgb(0, 100, 0)')

        draw_rect(
            self._ctx,
            rect=Rect(Position(300, 200), Size(100, 50)),
            fill_style='rgb(0, 200, 0)')

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

