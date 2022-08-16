"""ゲームビュー."""

import typing as tp

from model import GameModel
from values import *


class Font:
    """フォント設定."""

    def __init__(self, size: int, name: str, bold: bool = False):
        if size <= 0:
            raise ValueError()
        if not name:
            raise ValueError()

        self.size = size
        self.name = name
        self.bold = bold


class AbstractImageLoader:
    """画像読み込みの抽象クラス."""

    def __init__(self, file_names: tp.Collection[str]):
        pass

    def load(self) -> None:
        pass

    def is_loading(self) -> bool:
        """読み込み中か."""
        pass

    def get_image(self, file_name: str) -> object:
        """画像データを得る."""
        pass


class AbstractRenderer:
    """描画の抽象クラス."""

    @property
    def size(self) -> Size:
        pass

    def clear(self):
        """画面をクリアする."""
        pass

    def draw_rect(self, rect: Rect, color: Color) -> None:
        """矩形の描画."""
        pass

    def draw_line(self, start_pos: tuple[int, int], end_pos: tuple[int, int], color: Color) -> None:
        """線の描画."""
        pass

    def draw_circle(self, center: tuple[int, int], radius: int, color: Color) -> None:
        """円の描画."""
        pass

    def draw_image(self, image, position: Position, size: Size) -> None:
        """画像の描画."""
        pass

    def draw_text(self, text: str, position: tuple[int, int], font: Font, color: Color) -> None:
        """テキストの描画."""
        pass


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
        print('[GameView] Create')

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
            font=Font(size=48, name='serif', bold=True),
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
            font=Font(size=48, name='sans-serif', bold=True),
            color=Color(255, 255, 255))

    def _display_debug(self) -> None:
        """デバッグ情報を画面に描画する."""
        font = Font(size=10, name='sans-serif')
        color = Color(0, 0, 0)
        self._renderer.draw_text(f'Time={self._model.time:.1f}', (0, 10), font, color)
        self._renderer.draw_text(f'MousePos={self._model.mouse_pos}', (0, 20), font, color)
