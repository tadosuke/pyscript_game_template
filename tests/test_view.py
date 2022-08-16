import unittest

from view import *


class TestView(unittest.TestCase):

    def test_font(self):
        font = Font(size=10, name='sans-serif', bold=True)
        self.assertEqual(font.size, 10)
        self.assertEqual(font.name, 'sans-serif')
        self.assertTrue(font.bold)

        with self.assertRaises(ValueError):
            font = Font(size=0, name='sans-serif')
        with self.assertRaises(ValueError):
            font = Font(size=10, name='')


if __name__ == '__main__':
    unittest.main()
