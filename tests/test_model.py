"""modelモジュールのテスト."""

import unittest

from model import *
from input import *
from values import *


class TestModel(unittest.TestCase):

    def test_game_model(self):
        model = GameModel()
        self.assertAlmostEqual(model.time, 0)

        model.update(1.0)
        self.assertAlmostEqual(model.time, 1.0)

        param = OperationParam(
            code=VirtualKey.MouseMove,
            state=InputState.Press,
            position=Position(10, 20))
        model.operate(param)
        self.assertEqual(model.mouse_pos, Position(10, 20))


if __name__ == '__main__':
    unittest.main()
