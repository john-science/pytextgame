
import unittest
from pytextgame.colors import *
from pytextgame.displays import Displays
from pytextgame.geometry import *
from pytextgame.window import Window


class FakeWindow(Window):

    def __init__(ui, stdscr, game, rect, border=WHITE):
        Window.__init__(ui, stdscr, game, rect, border)


class TestDisplays(unittest.TestCase):

    def setUp(self):
        pass

    def test_one_window_display(self):
        displays = Displays()
        displays['fake'] = {'test': [FakeWindow, Rectangle(0, 0, 60, 30)]}
        self.assertEqual(displays.keys(), ['fake'])
        self.assertEqual(displays['fake'].keys(), ['test'])

    def test_multiple_displays(self):
        displays = Displays()
        displays['fake'] = {'test': [FakeWindow, Rectangle(0, 0, 60, 30)]}
        displays['not_real'] = {'testing': [FakeWindow, Rectangle(0, 0, 60, 30), RED]}
        self.assertEqual(sorted(displays.keys()), ['fake', 'not_real'])
        self.assertEqual(displays['fake'].keys(), ['test'])

    def test_add_broken_keys(self):
        displays = Displays()
        with self.assertRaises(TypeError):
            displays[123] = {'test': [FakeWindow, Rectangle(0, 0, 60, 30)]}

    def test_add_broken_window_name(self):
        displays = Displays()
        with self.assertRaises(TypeError):
            displays['faux'] = {123: [FakeWindow, Rectangle(0, 0, 60, 30)]}

    def test_add_broken_window(self):
        displays = Displays()
        with self.assertRaises(TypeError):
            displays['faux'] = {'test': [123, Rectangle(0, 0, 60, 30)]}

    def test_add_broken_rectangle(self):
        displays = Displays()
        with self.assertRaises(TypeError):
            displays['faux'] = {'test': [FakeWindow, Direction(0, 1)]}


if __name__ == '__main__':
    unittest.main()
