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

        with self.assertRaises(ValueError):
            color = Color(-1, -1, -1, -1)
            color = Color(256, 256, 256, 256)


if __name__ == '__main__':
    unittest.main()
