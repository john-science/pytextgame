# -- coding: utf-8 --
'''A window is a subsection of the charcter grid on the program screen'''

from pytextgame.geometry import Position
from colors import WHITE


class Window(object):

    def __init__(self, ui, stdscr, game, rect, border=WHITE):
        self.ui = ui
        self.stdscr = stdscr
        self.game = game
        self.rect = rect
        self.border = border
        self.has_border = True if border > -1 else False
        if self.has_border:
            self.window = stdscr.subwin(rect.height, rect.width, rect.y, rect.x, border)
        else:
            self.window = stdscr.subwin(rect.height, rect.width, rect.y, rect.x)

    def change_border_color(self, color):
        '''Helper method so that the color of the border of the window box
        can be changed on the fly.
        '''
        self.stdscr.del_box(self.window)
        self.window._color = color
        self.stdscr.add_box(self.window)

    def can_write(self, pos, string=' '):
        '''Verify that you can draw the string (usually a single
        charachter) at the given position. This is a test to make sure
        you're not trying to write outside the visible surface.
        '''
        if pos.y < 0 or pos.y >= self.rect.height - self.has_border * 2:
            return False

        if pos.x < 0 and abs(pos.x) >= len(string):
            return False

        if self.rect.width - pos.x - self.has_border * 2 <= 0:
            return False

        return True

    def write(self, pos, string, color, is_obli=False, is_bold=False):
        '''Write text into a window, provided you have a position
        and some attributes (colors, font style)
        '''
        if not self.can_write(pos) or string is None:
            return

        if pos.x < 0:
            self.write(Position(0, pos.y), string[abs(pos.x):], color, is_obli, is_bold)
            return

        max_len = self.rect.width - pos.x - self.has_border * 2

        if len(string) > max_len:
            string = string[:max_len]

        x = pos.x + self.has_border
        y = pos.y + self.has_border

        self.window.addstr(y, x, string, color, is_obli, is_bold)

    def clear(self):
        '''Empty the content of the current sub-window'''
        self.window.clear()

        # re-draw borders, if they are wanted
        if self.has_border:
            self.window.box()

    def refresh(self):
        '''Refresh the subwindow, using it's own subwindow method.
        '''
        self.window.refresh()

    def display(self):
        raise Exception("Not Implemented")


class Windows(dict):

    def __setitem__(self, key, item):
        '''validator method to ensure all values are Windows'''
        if not isinstance(item, Window):
            raise TypeError('You cannot add that, because it is not a Window.')

        dict.__setitem__(self, key, item)
