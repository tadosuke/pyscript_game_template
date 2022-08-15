"""ゲームビュー(pyscript)."""
import math
import os.path

from js import (
    console,
    Element,
    CanvasRenderingContext2D,
    Image,
)

import typing as tp
from model import GameModel
from values import *


class PyScriptRenderer:
    """PyScript用の描画クラス."""

    #: 背景色
    BACK_GROUND_COLOR = 'rgb(200, 200, 200)'

    def __init__(
            self,
            canvas: Element,
            context: CanvasRenderingContext2D,
            size: Size) -> None:
        if canvas is None:
            raise ValueError('canvas is None')
        self._canvas = canvas

        if context is None:
            raise ValueError('context is None')
        self._ctx = context
        self._size = size

    def draw_text(self, text: str, position: tuple[int, int], font: str, fill_style: str) -> None:
        """テキストの描画."""
        (x, y) = position
        text = text
        self._ctx.font = font
        self._ctx.fillStyle = fill_style
        self._ctx.fillText(text, x, y)

    def draw_rect(self, rect: Rect, fill_style: str) -> None:
        """矩形の描画."""
        self._ctx.fillStyle = fill_style
        self._ctx.fillRect(rect.position.x, rect.position.y, rect.size.width, rect.size.height)

    def draw_line(self, start_pos: tuple[int, int], end_pos: tuple[int, int], stroke_style: str) -> None:
        """線の描画."""
        self._ctx.beginPath()
        self._ctx.strokeStyle = stroke_style
        self._ctx.moveTo(*start_pos)
        self._ctx.lineTo(*end_pos)
        self._ctx.stroke()
        self._ctx.closePath()

    def draw_circle(self, center: tuple[int, int], radius: int, fill_style: str) -> None:
        """円の描画."""
        angle_start = 0 * math.pi / 180
        angle_end = 360 * math.pi / 180

        (x, y) = center
        self._ctx.beginPath()
        self._ctx.fillStyle = fill_style
        self._ctx.arc(x, y, radius, angle_start, angle_end)
        self._ctx.fill()
        self._ctx.closePath()

    def draw_image(self, image: Image, position: Position, size: Size) -> None:
        """画像の描画."""
        self._ctx.drawImage(image, position.x, position.y, size.width, size.height)

    def clear(self):
        """画面をクリアする."""
        self._ctx.fillStyle = self.BACK_GROUND_COLOR
        self._ctx.fillRect(0, 0, self._size.width, self._size.height)


class GameView:
    """ゲームのビュー.

    :param model: ゲームモデル
    :param canvas: 描画先のCanvas
    """

    #: 背景色
    BACK_GROUND_COLOR = 'rgb(200, 200, 200)'
    #: 画面幅
    WIDTH = 600
    #: 画面高さ
    HEIGHT = 400

    def __init__(
            self,
            model: GameModel,
            canvas: Element,
            preload_image_files: tp.Optional[list[str]] = None) -> None:
        console.log('[GameView] Create')

        if model is None:
            raise ValueError('model is None')
        self._model = model

        if canvas is None:
            raise ValueError('canvas is None')
        self._canvas = canvas
        self._setup_canvas()
        self._renderer = PyScriptRenderer(
            self._canvas,
            canvas.getContext('2d'),
            Size(self.WIDTH, self.HEIGHT))

        self._img_dict: dict[str, Image] = {}
        if preload_image_files:
            self._preload_finish = False
            self._preload_images(preload_image_files)
        else:
            self._preload_finish = True

    @property
    def canvas(self) -> Element:
        """Canvas."""
        return self._canvas

    def _preload_images(self, file_names: tp.Collection[str]) -> None:
        """画像ファイルの先読み."""
        for file in file_names:
            console.log(f'Preload image({file})')
            self._img_dict[os.path.basename(file)] = None
            image = Image.new()  # pythonではnew Image()とできないので、特殊な書き方になる
            image.src = file
            image.onload = lambda e: self._onload_image(image)

    def _onload_image(self, image):
        """画像の読み込み完了時に呼ばれる."""
        console.log(f'onload image({image.src})')
        self._img_dict[os.path.basename(image.src)] = image

        self._preload_finish = True
        for image in self._img_dict.values():
            if image is None:
                self._preload_finish = False

    def _setup_canvas(self) -> None:
        """ビューの初期化."""
        self._canvas.width = GameView.WIDTH
        self._canvas.height = GameView.HEIGHT

    def draw(self) -> None:
        """描画."""
        self._renderer.clear()

        # 先読み画像の読み込み待ち
        if not self._preload_finish:
            self._show_loading()
            return

        self._renderer.draw_line(
            start_pos=(100, 100),
            end_pos=(200, 120),
            stroke_style='rgb(200, 0, 0)')

        self._renderer.draw_circle(
            center=(200, 200),
            radius=50,
            fill_style='rgb(0, 0, 200)')

        self._renderer.draw_text(
            text='GameTemplate',
            position=(50, 300),
            font='48px bold serif',
            fill_style='rgb(0, 100, 0)')

        self._renderer.draw_rect(
            rect=Rect(Position(300, 200), Size(100, 50)),
            fill_style='rgb(0, 200, 0)')

        if self._img_dict:
            self._renderer.draw_image(
                image=self._img_dict['image.png'],  # プリロードに指定した画像
                position=Position(400, 80),
                size=Size(32, 32))

        self._display_debug()

    def _show_loading(self) -> None:
        """ロード中表示."""
        self._renderer.draw_text(
            text='Now Loading...',
            position=(120, 200),
            font='48px bold serif',
            fill_style='rgb(255, 255, 255)')

    def _display_debug(self) -> None:
        """デバッグ情報を画面に描画する."""
        font = "10px sans-serif"
        fill_style = 'rgb(0, 0, 0)'
        self._renderer.draw_text(f'Time={self._model.time:.1f}', (0, 10), font, fill_style)
        self._renderer.draw_text(f'MousePos={self._model.mouse_pos}', (0, 20), font, fill_style)
