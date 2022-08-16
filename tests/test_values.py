"""valuesモジュールのテスト."""

import unittest

from values import Color


class TestValues(unittest.TestCase):

    def test_color(self):
        color = Color(10, 20, 30, 40)
        self.assertEqual(color.r, 10)
        self.assertEqual(color.g, 20)
        self.assertEqual(color.b, 30)
        self.assertEqual(color.a, 40)


if __name__ == '__main__':
    unittest.main()
