# -- coding: utf-8 --
'''A window is a subsection of the charcter grid on the program screen'''

from pytextgame.geometry import Position
from colors import WHITE, BLACK
import sys
if sys.version_info[0] < 3: range = xrange

# border type constants
LINE_BORDER = 1
SOLID_BORDER = 2


class Window(object):

    def __init__(self, ui, stdscr, game, rect, border_type=LINE_BORDER, border_color=WHITE):
        self.ui = ui
        self.stdscr = stdscr
        self.game = game
        self.rect = rect
        self.border_type = border_type
        self.border_color = border_color
        self.has_border = True
        self.check_for_border()
        self.window = stdscr.subwin(rect.height, rect.width, rect.y, rect.x, border_color)

    def check_for_border(self):
        '''Check to see if the border is either line or solid type.
        If not, the window has no border.
        '''
        self.has_border =  True if self.border_type in [LINE_BORDER, SOLID_BORDER] else False

    def draw_solid_border(self, color):
        '''Instead of drawing a line box, simply fill in the border tiles with solid colors.'''
        # draw horizontal borders
        for col in range(self.rect.width):
            # draw top border
            self.window.addstr(0, col, ' ', color, color, False, False)
            # draw bottom border
            self.window.addstr(self.rect.height - 1, col, ' ', color, color, False, False)

        # draw vertical borders
        for row in range(1, self.rect.height - 1):
            # draw left border
            self.window.addstr(row, 0, ' ', color, color, False, False)
            # draw right border
            self.window.addstr(row, self.rect.width - 1, ' ', color, color, False, False)

    def change_border_color(self, color):  # TODO: Silly method name?
        '''Helper method so that the color of the border of the window box
        can be changed on the fly.
        '''
        self.border_color = color
        if self.border_type == LINE_BORDER:
            self.stdscr.del_box(self.window)
            self.window._color = color          # TODO: Need to add setters and getters?
            self.stdscr.add_box(self.window)
        else:
            self.draw_solid_border(self.border_color)

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

    def write(self, pos, string, color, bgcolor=None, is_obli=False, is_bold=False):
        '''Write text into a window, provided you have a position
        and some attributes (colors, font style)
        '''
        if not self.can_write(pos) or string is None:
            return

        if pos.x < 0:
            self.write(Position(0, pos.y), string[abs(pos.x):], color, bgcolor, is_obli, is_bold)
            return

        max_len = self.rect.width - pos.x - self.has_border * 2

        if len(string) > max_len:
            string = string[:max_len]

        x = pos.x + self.has_border
        y = pos.y + self.has_border

        self.window.addstr(y, x, string, color, bgcolor, is_obli, is_bold)

    def clear(self):
        '''Empty the content of the current sub-window'''
        self.window.clear()

        # re-draw borders, if they are wanted
        if self.has_border:
            if self.border_type == LINE_BORDER:
                self.window.box()
            else:
                self.draw_solid_border(self.border_color)  # TODO: Do I just need to re-write 'draw_solid_border'?

    def refresh(self):
        '''Refresh the subwindow, using it's own subwindow method.
        '''
        self.window.refresh()

    def display(self):
        raise Exception("Not Implemented")


class Windows(dict):
    '''Windows is a simple dictionary of names (string keys) mapped to
    Windows that define the current display of the game.
    There is some light type-checking done.
    '''

    def __setitem__(self, key, item):
        '''validator method to ensure all values are Windows'''
        if not isinstance(key, str):
            raise TypeError('Window keys must be strings.')
        if not isinstance(item, Window):
            raise TypeError('You cannot add that, because it is not a Window.')

        dict.__setitem__(self, key, item)
