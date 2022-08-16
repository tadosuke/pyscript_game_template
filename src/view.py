"""ゲームビュー."""

from values import *


class AbstractRenderer:
    """描画の抽象クラス."""

    def __init__(self):
        pass

    @property
    def size(self) -> Size:
        pass

    def clear(self):
        """画面をクリアする."""
        pass

    def draw_rect(self, rect: Rect, fill_style: str) -> None:
        """矩形の描画."""
        pass

    def draw_line(self, start_pos: tuple[int, int], end_pos: tuple[int, int], stroke_style: str) -> None:
        """線の描画."""
        pass

    def draw_circle(self, center: tuple[int, int], radius: int, fill_style: str) -> None:
        """円の描画."""
        pass

    def draw_image(self, image, position: Position, size: Size) -> None:
        """画像の描画."""
        pass

    def draw_text(self, text: str, position: tuple[int, int], font: str, color: Color) -> None:
        """テキストの描画."""
        pass
