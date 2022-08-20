"""modelモジュールのテスト."""

import unittest
import typing as tp

from model import *
from input import *
from values import *


class MockRepository(AbstractRepository):
    """テスト用のモックリポジトリ."""

    def __init__(self):
        self.data: dict[str, tp.Any] = {}

    def save(self, key: str, value: tp.Any):
        self.data[key] = value

    def load(self, key: str, default: tp.Any = None) -> tp.Optional[tp.Any]:
        return self.data.get(key)


class TestModel(unittest.TestCase):

    def test_game_model(self):
        model = GameModel(
            world_size=Size(600, 400),
            log_func=None,
            repository=MockRepository())
        self.assertEqual(model._world_size, Size(600, 400))
        self.assertAlmostEqual(model.time, 0)

        # リポジトリ
        model.time = 0.0
        model.save()
        model.time = 10.0
        model.load()
        self.assertAlmostEqual(model.time, 0.0)

        # 更新
        model.time = 0.0
        model.update(1.0)
        self.assertAlmostEqual(model.time, 1.0)


if __name__ == '__main__':
    unittest.main()
