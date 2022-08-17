import unittest

from view import *


class MockRenderer(AbstractRenderer):
    pass


class MockImageLoader(AbstractImageLoader):
    pass


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

    def test_game_view(self):
        result = True
        try:
            model = GameModel(world_size=Size(600, 400))
            renderer = MockRenderer()
            loader = MockImageLoader([])
            view = GameView(model, renderer, loader)
        except Exception:
            result = False
        finally:
            self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
