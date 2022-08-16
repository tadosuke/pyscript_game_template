"""valuesモジュールのテスト."""

import unittest

from values import *


class TestValues(unittest.TestCase):

    def test_color(self):
        color = Color(10, 20, 30, 40)
        self.assertEqual(color.r, 10)
        self.assertEqual(color.g, 20)
        self.assertEqual(color.b, 30)
        self.assertEqual(color.a, 40)

        color = Color(10, 20, 30)
        self.assertEqual(color.a, 255)

        with self.assertRaises(ValueError):
            color = Color(-1, -1, -1, -1)
            color = Color(256, 256, 256, 256)

    def test_rect(self):
        rect1 = Rect(Position(10, 20), Size(30, 40))
        self.assertEqual(rect1.position, Position(10, 20))
        self.assertEqual(rect1.size, Size(30, 40))
        self.assertEqual(rect1.left, 10)
        self.assertEqual(rect1.right, 10+30)
        self.assertEqual(rect1.top, 20)
        self.assertEqual(rect1.bottom, 20+40)
        self.assertEqual(rect1.center, Position(25, 40))

        self.assertFalse(rect1.contains_point(Position(10-1, 20-1)))
        self.assertTrue(rect1.contains_point(Position(10, 20)))
        self.assertTrue(rect1.contains_point(Position(10+30, 20+40)))
        self.assertFalse(rect1.contains_point(Position(10+30+1, 20+40+1)))

        rect2 = Rect(Position(20, 30), Size(40, 50))
        self.assertNotEqual(rect1, rect2)


if __name__ == '__main__':
    unittest.main()
