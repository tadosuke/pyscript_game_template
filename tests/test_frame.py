"""frameモジュールのテスト."""

import unittest

from frame import *
from values import *


class TestFrame(unittest.TestCase):

    def test_case(self):
        frame = Frame(Rect(Position(10, 20), Size(30, 40)))


if __name__ == '__main__':
    unittest.main()
