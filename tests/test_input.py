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

    def test_input_event(self):
        event = InputEvent()

        param = OperationParam(code=VirtualKey.MouseLeft, state=InputState.Press)
        self.assertFalse(event.process(param))
        event.connect(VirtualKey.MouseLeft, self._on_input)
        self.assertTrue(event.process(param))
        event.disconnect(VirtualKey.MouseLeft)
        self.assertFalse(event.process(param))
        event.connect(VirtualKey.MouseLeft, self._on_input)
        event.disconnect_all()
        self.assertFalse(event.process(param))

    @staticmethod
    def _on_input(param: OperationParam) -> bool:
        return True


if __name__ == '__main__':
    unittest.main()
