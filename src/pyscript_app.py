"""アプリケーション."""

import asyncio

from js import (
    console,
    document,
    Element,
)

from pyscript_controller import GameController
from model import GameModel
from pyscript_view import GameView, PyScriptRenderer, PyScriptImageLoader


#: ゲームのFPS
_FPS = 1.0 / 30
#: 画面幅
SCREEN_WIDTH = 600
#: 画面高さ
SCREEN_HEIGHT = 400

#: プリロードする画像ファイル名
_PRELOAD_IMAGE_FILES: list[str] = [
    'image.png',
]


async def main() -> None:
    """メイン関数."""
    canvas = _setup_canvas()

    try:
        model = GameModel()
        renderer = PyScriptRenderer(canvas)
        loader = PyScriptImageLoader(_PRELOAD_IMAGE_FILES)
        view = GameView(model, renderer, loader)
        controller = GameController(model, canvas)
    except ValueError as e:
        console.error(f'Failed to create GameObjects:{e}')
        return

    while True:
        model.update(_FPS)
        view.draw()
        await asyncio.sleep(_FPS)


def _setup_canvas() -> Element:
    """canvasをセットアップする."""
    canvas = document.querySelector('#output')
    if canvas is None:
        raise ValueError('canvas is None')
    canvas.width = SCREEN_WIDTH
    canvas.height = SCREEN_HEIGHT
    return canvas


if __name__ == '__main__':
    pyscript_loader.close()
    pyscript.run_until_complete(main())
