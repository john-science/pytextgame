
import unittest
from pytextgame.colors import *

TEST_RED = 16711680


class TestColors(unittest.TestCase):

    def setUp(self):
        pass

    def test_int2tuple_black(self):
        self.assertEqual(color_int2tuple(0), (0, 0, 0))

    def test_int2tuple_blue(self):
        self.assertEqual(color_int2tuple(255), (0, 0, 255))

    def test_int2tuple_red(self):
        self.assertEqual(color_int2tuple(TEST_RED), (255, 0, 0))

    def test_tuple2int_black(self):
        self.assertEqual(color_tuple2int((0, 0, 0)), 0)

    def test_tuple2int_blue(self):
        self.assertEqual(color_tuple2int((0, 0, 255)), 255)

    def test_tuple2int_red(self):
        self.assertEqual(color_tuple2int((255, 0, 0)), TEST_RED)

    def test_colors_black(self):
        self.assertEqual(COLORS['BLACK'], 0)

    def test_colors_blue(self):
        self.assertEqual(COLORS['BLUE'], 255)

    def test_colors_red(self):
        self.assertEqual(COLORS['RED'], TEST_RED)


if __name__ == '__main__':
    unittest.main()
