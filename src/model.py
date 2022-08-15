"""ゲームモデル."""

from input import VirtualKey, OperationParam, InputState
from values import Position


class GameModel:
    """ゲーム本体."""

    def __init__(self) -> None:
        print('[GameModel] Create')
        self.time = 0
        self.mouse_pos: Position = Position(0, 0)
        self.keys: dict[VirtualKey, bool] = {}

    def update(self, delta) -> None:
        """定期更新処理.

        :param delta: デルタ秒
        """
        self.time += delta

    def operate(self, param: OperationParam) -> None:
        """入力時に外部から呼ばれる."""
        if param.code == VirtualKey.MouseMove:
            self.mouse_pos = param.position
            return
        self.keys[param.code] = param.is_press()
