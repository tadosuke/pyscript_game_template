"""アプリケーション."""

import asyncio

from js import (
    console,
    document,
    Element,
)
from pyodide import create_proxy

from pyscript_controller import GameController
from model import GameModel
from pyscript_view import GameView


#: ゲームのFPS
_FPS = 1.0 / 30


async def main() -> None:
    """メイン関数."""
    canvas = document.querySelector('#output')
    if canvas is None:
        console.error('context is None')
        return

    try:
        model = GameModel()
        view = GameView(model, canvas)
        controller = GameController(model, view)
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
