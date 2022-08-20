"""ゲームモデル."""

from input import VirtualKey, OperationParam
from values import Position, Size
import typing as tp


# 型：ログ出力関数
LogFuncType = tp.Callable[[str], None]


class AbstractRepository:
    """リポジトリの抽象クラス."""

    def save(self, key: str, value: tp.Any):
        pass

    def load(self, key: str, default: tp.Any = None) -> tp.Optional[tp.Any]:
        pass


class GameModel:
    """ゲーム本体.

    :param world_size: ゲーム空間の大きさ
    :param repository: リポジトリ
    """

    def __init__(
            self,
            world_size: Size,
            log_func: LogFuncType = None,
            repository: AbstractRepository = None) -> None:
        self._world_size = world_size
        self._repository = repository

        if log_func is None:
            self.log = lambda mes: print(mes)
        else:
            self.log = log_func

        self.time: float = 0
        self.mouse_pos: Position = Position(0, 0)
        self.keys: dict[VirtualKey, bool] = {}

        self.log('[GameModel] Create')

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

        if param.code == VirtualKey.S and param.is_press():
            self.save()
        elif param.code == VirtualKey.L and param.is_press():
            self.load()

        self.keys[param.code] = param.is_press()

    def save(self) -> None:
        """保存."""
        if self._repository is not None:
            self._repository.save(key='time', value=str(self.time))

    def load(self) -> None:
        """読み込み."""
        if self._repository is not None:
            value = self._repository.load(key='time', default=0)
            self.time = float(value)
