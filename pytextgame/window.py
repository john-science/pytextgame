# -- coding: utf-8 --
'''A window is a subsection of the charcter grid on the program screen'''

from pytextgame.geometry import Position


class Window:

    def __init__(self, ui, stdscr, model, rect, border = False):
        self.ui = ui
        self.stdscr = stdscr
        self.model = model
        self.rect = rect
        self.border = border
        self.window = stdscr.subwin(rect.height, rect.width, rect.y, rect.x)

    def can_write(self, pos, string=' '):
        '''Verify that you can draw the string (usually a single
        charachter) at the given position. This is a test to make sure
        you're not trying to write outside the visible surface.
        '''
        if pos.y < 0 or pos.y >= self.rect.height - self.border * 2:
            return False

        if pos.x < 0 and abs(pos.x) >= len(string):
            return False

        if self.rect.width - pos.x - self.border * 2 <= 0:
            return False

        return True

    def write(self, pos, string, attributes=[]):
        '''Write text into a window, provided you have a position
        and some attributes (colors)
        '''
        if not self.can_write(pos) or string is None:
            return

        if pos.x < 0:
            self.write(Position(0, pos.y), string[abs(pos.x):])
            return

        max_len = self.rect.width - pos.x - self.border * 2

        if len(string) > max_len:
            string = string[:max_len]

        x = pos.x + self.border
        y = pos.y + self.border

        # TODO: What are these attributes? Colors and fonts?
        if attributes:
            self.window.addstr(y, x, string, reduce(lambda a, b: a | b, attributes))
        else:
            self.window.addstr(y, x, string)

    def clear(self):
        '''Empty the content of the current sub-window'''
        self.window.clear()

        # re-draw borders, if they are wanted
        if self.border:
            self.window.box()

    def refresh(self):
        '''Refresh the subwindow, using it's own subwindow method.
        '''
        self.window.refresh()

    def display(self):
        raise 'Not implemented'
