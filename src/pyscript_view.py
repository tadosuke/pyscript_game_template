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
from view import AbstractRenderer, AbstractImageLoader, Font


class PyScriptFont(Font):

    def __init__(self, size: int, name: str, bold: bool = False):
        super().__init__(size, name, bold)

    def __str__(self):
        result = f'{self.size}px '
        if self.bold:
            result += 'bold '
        result += self.name
        return result


class PyScriptRenderer(AbstractRenderer):
    """PyScript用の描画クラス."""

    #: 背景色
    BACK_GROUND_COLOR = 'rgb(200, 200, 200)'

    def __init__(
            self,
            canvas: Element) -> None:
        if canvas is None:
            raise ValueError('canvas is None')
        self._canvas = canvas
        self._ctx = canvas.getContext('2d')

    @property
    def size(self) -> Size:
        """サイズ."""
        return Size(self._canvas.width, self._canvas.height)

    def clear(self):
        """画面をクリアする."""
        self._ctx.fillStyle = self.BACK_GROUND_COLOR
        self._ctx.fillRect(0, 0, self.size.width, self.size.height)

    def draw_text(self, text: str, position: tuple[int, int], font: PyScriptFont, color: Color) -> None:
        """テキストの描画."""
        (x, y) = position
        text = text
        self._ctx.font = str(font)
        self._ctx.fillStyle = self._color_to_style(color)
        self._ctx.fillText(text, x, y)

    def draw_rect(self, rect: Rect, color: Color) -> None:
        """矩形の描画."""
        self._ctx.fillStyle = self._color_to_style(color)
        self._ctx.fillRect(rect.position.x, rect.position.y, rect.size.width, rect.size.height)

    def draw_line(self, start_pos: tuple[int, int], end_pos: tuple[int, int], color: Color) -> None:
        """線の描画."""
        self._ctx.beginPath()
        self._ctx.strokeStyle = self._color_to_style(color)
        self._ctx.moveTo(*start_pos)
        self._ctx.lineTo(*end_pos)
        self._ctx.stroke()
        self._ctx.closePath()

    def draw_circle(self, center: tuple[int, int], radius: int, color: Color) -> None:
        """円の描画."""
        angle_start = 0 * math.pi / 180
        angle_end = 360 * math.pi / 180

        (x, y) = center
        self._ctx.beginPath()
        self._ctx.fillStyle = self._color_to_style(color)
        self._ctx.arc(x, y, radius, angle_start, angle_end)
        self._ctx.fill()
        self._ctx.closePath()

    def draw_image(self, image: Image, position: Position, size: Size) -> None:
        """画像の描画."""
        self._ctx.drawImage(image, position.x, position.y, size.width, size.height)

    @staticmethod
    def _color_to_style(color: Color) -> str:
        return f'rgb({color.r},{color.g},{color.b})'


class PyScriptImageLoader(AbstractImageLoader):
    """PyScript用の画像読み込みクラス."""

    def __init__(self, file_names: tp.Collection[str]):
        super().__init__(file_names)
        self._file_names = file_names
        self._img_dict: dict[str, Image] = {}

    def load(self) -> None:
        """読み込む."""
        for file_name in self._file_names:
            console.log(f'Load image({file_name})')
            self._img_dict[file_name] = None
            image = Image.new()  # pythonではnew Image()とできないので、特殊な書き方になる
            image.src = file_name
            image.onload = lambda e: self._onload_image(image)

    def _onload_image(self, image: Image):
        """読み込み完了時に呼ばれる."""
        console.log(f'Onload image({image.src})')
        self._img_dict[os.path.basename(image.src)] = image

    def is_loading(self) -> bool:
        """読み込み中か."""
        if None in self._img_dict.values():
            return True
        return False

    def get_image(self, file_name: str) -> Image:
        """画像データを得る."""
        return self._img_dict[file_name]


class GameView:
    """ゲームのビュー.

    :param model: ゲームモデル
    :param renderer: 描画クラス
    :param image_loader: 画像読み込みクラス
    """

    def __init__(
            self,
            model: GameModel,
            renderer: AbstractRenderer,
            image_loader: AbstractImageLoader) -> None:
        console.log('[GameView] Create')

        if model is None:
            raise ValueError('model is None')
        self._model = model

        if renderer is None:
            raise ValueError('renderer is None')
        self._renderer = renderer

        if image_loader is None:
            raise ValueError('image_loader is None')
        self._image_loader = image_loader
        self._image_loader.load()

    def draw(self) -> None:
        """描画."""
        self._renderer.clear()

        # 先読み画像の読み込み待ち
        if self._image_loader.is_loading():
            self._show_loading()
            return

        self._renderer.draw_line(
            start_pos=(100, 100),
            end_pos=(200, 120),
            color=Color(200, 0, 0))

        self._renderer.draw_circle(
            center=(200, 200),
            radius=50,
            color=Color(0, 0, 200))

        self._renderer.draw_text(
            text='GameTemplate',
            position=(50, 300),
            font=PyScriptFont(size=48, name='serif', bold=True),
            color=Color(0, 100, 0))

        self._renderer.draw_rect(
            rect=Rect(Position(300, 200), Size(100, 50)),
            color=Color(0, 200, 0))

        image = self._image_loader.get_image('image.png')
        if image is not None:
            self._renderer.draw_image(
                image=image,
                position=Position(400, 80),
                size=Size(32, 32))

        self._display_debug()

    def _show_loading(self) -> None:
        """ロード中表示."""
        self._renderer.draw_text(
            text='Now Loading...',
            position=(120, 200),
            font=PyScriptFont(size=48, name='sans-serif', bold=True),
            color=Color(255, 255, 255))

    def _display_debug(self) -> None:
        """デバッグ情報を画面に描画する."""

        font = PyScriptFont(size=10, name='sans-serif')
        color = Color(0, 0, 0)
        self._renderer.draw_text(f'Time={self._model.time:.1f}', (0, 10), font, color)
        self._renderer.draw_text(f'MousePos={self._model.mouse_pos}', (0, 20), font, color)
