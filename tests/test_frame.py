"""frameモジュールのテスト."""

import unittest

from frame import *
from values import *
from input import *


class TestFrame(unittest.TestCase):

    def test_case(self):
        frame1 = Frame(Rect(Position(10, 20), Size(30, 40)))

        self.assertIsNone(frame1._input_callback.get(VirtualKey.MouseLeft))
        frame1.connect_input(VirtualKey.MouseLeft, self._on_input)
        self.assertIsNotNone(frame1._input_callback.get(VirtualKey.MouseLeft))

        param = OperationParam(
            code=VirtualKey.MouseLeft,
            state=InputState.Press)
        self.assertTrue(frame1.process_input(param))

        param = OperationParam(
            code=VirtualKey.MouseRight,
            state=InputState.Press)
        self.assertFalse(frame1.process_input(param))

        frame2 = Frame(Rect(Position(30, 40), Size(50, 60)), parent=frame1)
        self.assertEqual(frame2.parent, frame1)
        self.assertEqual(frame1._children[0], frame2)

        frame2.connect_input(VirtualKey.MouseMiddle, self._on_input)
        param = OperationParam(
            code=VirtualKey.MouseMiddle,
            state=InputState.Press)
        self.assertTrue(frame1.process_input(param))  # 子フレームが受け取るか

    @staticmethod
    def _on_input(param: OperationParam) -> bool:
        return True


if __name__ == '__main__':
    unittest.main()
