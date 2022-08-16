"""inputモジュールのテスト."""

import unittest

from input import *
from values import *


class TestInput(unittest.TestCase):

    def test_operation_param(self):
        param = OperationParam(
            code=VirtualKey.MouseLeft,
            state=InputState.Press,
            position=Position(10, 20))
        self.assertTrue(param.is_press())
        self.assertFalse(param.is_release())
        self.assertFalse(param.is_repeat())


if __name__ == '__main__':
    unittest.main()
