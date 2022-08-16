import unittest

from view import *


class TestView(unittest.TestCase):

    def test_font(self):
        font = Font(size=10, type='sans-serif', bold=True)
        self.assertEqual(font.size, 10)
        self.assertEqual(font.type, 'sans-serif')
        self.assertTrue(font.bold)


if __name__ == '__main__':
    unittest.main()
