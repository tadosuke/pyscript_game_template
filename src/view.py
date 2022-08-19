"""ゲームビュー."""

import typing as tp

from input import VirtualKey, OperationParam
from model import GameModel
from values import *
from interface import AbstractRenderer, AbstractImageLoader
from frame import Frame


class Button(Frame):

    MARGIN_LEFT = 5

    def __init__(
            self,
            rect: Rect,
            renderer: AbstractRenderer,
            text: str = '',
            parent: Frame = None):
        super().__init__(rect, parent)

        self._text = text
        self._renderer = renderer

        self.connect_input(VirtualKey.MouseLeft, self._on_mouseleft)

    def draw(self):
        self._renderer.draw_rect(self.rect, Color(255, 255, 255))
        self._renderer.draw_rect(self.rect, Color(128, 128, 128), fill=False)

        font_size = 30
        (x, y) = self.position.x, self.position.y
        x += self.MARGIN_LEFT
        y += font_size
        self._renderer.draw_text(self._text, (x, y), Font(font_size, 'serif'), Color(0, 0, 0))

    def _on_mouseleft(self, param: OperationParam):
        if param.is_press():
            print('Button pressed.')


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

        self._button = Button(
            Rect(Position(400, 100), Size(120, 40)),
            self._renderer,
            'Button',
            self._model.root_frame)

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

        self._renderer.draw_rect(rect=Rect(Position(300, 200), Size(100, 50)), color=Color(0, 200, 0))

        image = self._image_loader.get_image('image.png')
        if image is not None:
            self._renderer.draw_image(
                image=image,
                position=self._model.mouse_pos,
                size=Size(32, 32))

        self._button.draw()

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
        self._display_debug_frame()

    def _display_debug_frame(self) -> None:
        """フレームのデバッグ表示."""
        root_frame = self._model.root_frame
        rect = root_frame.rect
        self._renderer.draw_rect(rect, Color(0, 255, 255), fill=False)
