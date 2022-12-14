"""frameモジュールのテスト."""

import unittest

from frame import *
from input import *
from values import *


class TestFrame(unittest.TestCase):

    def test_case(self):
        frame1 = Frame(Rect(Position(10, 20), Size(30, 40)))
        frame1.connect_input(VirtualKey.MouseLeft, self._on_input)

        # 登録したキー・範囲内
        param = OperationParam(
            code=VirtualKey.MouseLeft,
            state=InputState.Press,
            position=Position(11, 21))
        self.assertTrue(frame1.process_input(param))

        # 登録したキー・範囲外
        param = OperationParam(
            code=VirtualKey.MouseLeft,
            state=InputState.Press,
            position=Position(9, 19))
        self.assertFalse(frame1.process_input(param))

        # 親子付け
        frame2 = Frame(Rect(Position(30, 40), Size(50, 60)), parent=frame1)
        self.assertEqual(frame2.parent, frame1)
        self.assertEqual(frame1._children[0], frame2)

        # 子フレームが受け取るか
        frame2.connect_input(VirtualKey.MouseMiddle, self._on_input)
        param = OperationParam(
            code=VirtualKey.MouseMiddle,
            state=InputState.Press)
        self.assertTrue(frame1.process_input(param))

    @staticmethod
    def _on_input(param: OperationParam) -> bool:
        return True


if __name__ == '__main__':
    unittest.main()
