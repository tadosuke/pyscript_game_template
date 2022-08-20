"""ゲームビュー."""

from __future__ import annotations
import typing as tp

from input import VirtualKey, OperationParam
from model import GameModel
from values import *
from interface import AbstractRenderer, AbstractImageLoader
from frame import Frame


# 型：ログ出力関数
LogFuncType = tp.Callable[[str], None]


class Button(Frame):
    """ボタン."""

    MARGIN_LEFT = 5

    def __init__(
            self,
            rect: Rect,
            renderer: AbstractRenderer,
            text: str = '',
            parent: Frame = None):
        super().__init__(rect, parent)

        self.text = text
        self._renderer = renderer

        #: 押された時に呼ばれるコールバック
        self.onpress: tp.Callable[[Button], None] = None

        self.connect_input(VirtualKey.MouseLeft, self._on_mouseleft)

    def draw(self):
        """描画."""

        self._renderer.draw_rect(self.rect, Color(255, 255, 255))
        self._renderer.draw_rect(self.rect, Color(128, 128, 128), fill=False)

        font_size = 30
        (x, y) = self.position.x, self.position.y
        x += self.MARGIN_LEFT
        y += font_size
        self._renderer.draw_text(self.text, (x, y), Font(font_size, 'serif'), Color(0, 0, 0))

    def _on_mouseleft(self, param: OperationParam):
        if param.is_press():
            if self.onpress is not None:
                self.onpress(self)


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
            image_loader: AbstractImageLoader,
            log_func: LogFuncType = None) -> None:

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

        if log_func is None:
            self.log = lambda mes: print(mes)
        else:
            self.log = log_func

        self._root_frame = self._create_root_frame()
        self._mouse_pos = Position(0, 0)

        self._buttons: list[Button] = []
        self._create_buttons()

    def _create_root_frame(self) -> Frame:
        """ルートフレームを生成する."""
        position = Position(0, 0)
        rect = Rect(position, self._renderer.size)
        frame = Frame(rect, None)
        return frame

    def _create_buttons(self):
        """ボタンを生成する."""
        x = 10
        y = 50
        size = Size(130, 40)

        for i in range(4):
            button = Button(
                Rect(Position(x, y + i*45), size),
                self._renderer,
                f'Button {i}',
                self._root_frame)
            button.onpress = self._on_button_pressed
            self._buttons.append(button)

    def draw(self) -> None:
        """描画."""
        self._renderer.clear()

        # 先読み画像の読み込み待ち
        if self._image_loader.is_loading():
            self._show_loading()
            return

        self._renderer.draw_line(
            start_pos=(300, 100),
            end_pos=(400, 120),
            color=Color(200, 0, 0))

        self._renderer.draw_circle(
            center=(300, 200),
            radius=50,
            color=Color(0, 0, 200))

        self._renderer.draw_text(
            text='GameTemplate',
            position=(10, 380),
            font=Font(size=48, name='serif', bold=True),
            color=Color(0, 100, 0))

        self._renderer.draw_rect(
            rect=Rect(
                Position(400, 250),
                Size(100, 50)),
            color=Color(0, 200, 0))

        image = self._image_loader.get_image('image.png')
        if image is not None:
            self._renderer.draw_image(
                image=image,
                position=self._mouse_pos,
                size=Size(32, 32))

        for button in self._buttons:
            button.draw()

        self._display_debug()

    def operate(self, param: OperationParam) -> None:
        """入力時に外部から呼ばれる."""
        if param.code == VirtualKey.MouseMove:
            self._mouse_pos = param.position

        if param.code == VirtualKey.S and param.is_press():
            self._model.save()
        elif param.code == VirtualKey.L and param.is_press():
            self._model.load()

        self._root_frame.process_input(param)

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
        self._renderer.draw_text(f'MousePos={self._mouse_pos}', (0, 20), font, color)
        self._display_debug_frame()

    def _display_debug_frame(self) -> None:
        """フレームのデバッグ表示."""
        rect = self._root_frame.rect
        self._renderer.draw_rect(rect, Color(0, 255, 255), fill=False)

    def _on_button_pressed(self, button: Button) -> None:
        """ボタンが押された."""
        self.log(f'Button({button.text}) Pressed.')
