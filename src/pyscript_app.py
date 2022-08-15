"""アプリケーション."""

import asyncio

from js import (
    console,
    document,
)

from pyscript_controller import GameController
from model import GameModel
from pyscript_view import GameView, PyScriptRenderer


#: ゲームのFPS
_FPS = 1.0 / 30

#: プリロードする画像ファイル名
_PRELOAD_IMAGE_FILES: list[str] = [
    'image.png',
]


async def main() -> None:
    """メイン関数."""
    canvas = document.querySelector('#output')
    if canvas is None:
        console.error('canvas is None')
        return

    try:
        model = GameModel()
        renderer = PyScriptRenderer(canvas)
        view = GameView(model, renderer, _PRELOAD_IMAGE_FILES)
        controller = GameController(model, canvas)
    except ValueError as e:
        console.error(f'Failed to create GameObjects:{e}')
        return

    while True:
        model.update(_FPS)
        view.draw()
        await asyncio.sleep(_FPS)


if __name__ == '__main__':
    pyscript_loader.close()
    pyscript.run_until_complete(main())
