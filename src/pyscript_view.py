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
    """PyScript用フォント設定."""

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

    def draw_text(self, text: str, position: tuple[int, int], font: Font, color: Color) -> None:
        """テキストの描画."""
        (x, y) = position
        text = text
        pyscript_font = PyScriptFont(font.size, font.name, font.bold)
        self._ctx.font = str(pyscript_font)
        self._ctx.fillStyle = self._color_to_style(color)
        self._ctx.fillText(text, x, y)

    def draw_rect(self, rect: Rect, color: Color, fill=True) -> None:
        """矩形の描画."""
        if fill:
            self._ctx.fillStyle = self._color_to_style(color)
            self._ctx.fillRect(rect.position.x, rect.position.y, rect.size.width, rect.size.height)
        else:
            self._ctx.strokeStyle = self._color_to_style(color)
            self._ctx.strokeRect(rect.position.x, rect.position.y, rect.size.width, rect.size.height)

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

