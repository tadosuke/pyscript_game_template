"""ゲームビュー."""

import typing as tp

from values import *


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

    def draw_text(self, text: str, position: tuple[int, int], font: str, color: Color) -> None:
        """テキストの描画."""
        pass
