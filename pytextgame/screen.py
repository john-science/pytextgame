# -- coding: utf-8 --
'''Create a basic text-grid screen using Pygame'''

import os
import sys
import time
from colors import *
import pygame
from pygame.time import Clock
from pygame.locals import *
from pkg_resources import resource_stream, resource_filename
if sys.version_info[0] < 3: range = xrange

# Key Constants
CONTROL_Q = 17
NULL_KEY = 'Null Key'


def wrapper(method, num_rows, num_cols, icon):
    '''
    This funtion exists to keep all references
    to pygame in this module.
    '''
    pygame.init()
    method(Screen(num_rows, num_cols, icon))


class Screen(object):

    PYTEXTGAME = 'pytextgame'
    RESOURCE_DIR = 'resources'
    ICON = 'rocket32.png'
    # FONT[is_oblique][is_bold]
    FONT = {False: {False: 'DejaVuSansMono.ttf',
            True: 'DejaVuSansMono-Bold.ttf'},
            True: {False: 'DejaVuSansMono-Oblique.ttf',
            True: 'DejaVuSansMono-BoldOblique.ttf'}}

    def __init__(self, height, width, icon=None):
        # general screen info
        self._id = 0
        self._height = height
        self._width  = width
        self._bgcolor = (0, 0, 0)
        self._chars = [[(' ', 0, False, False) for y in range(height)] for x in range(width)]
        self._boxes = {0: None}
        self.set_repeat(150, 50)
        # set icon and THEN start pygame display (which we do when we set the font)
        if icon is not None:
            self.set_icon(icon)
        else:
            self.set_icon(resource_stream(__name__, os.path.join(self.RESOURCE_DIR, self.ICON)))
        self.set_caption(self.PYTEXTGAME)
        # font info
        self._font_size = 16
        self._font_path = {False: {}, True: {}}
        self.init_font_paths()
        self._font = {False: {}, True: {}}
        self.reset_font()
        # special characters
        self.key_quit = 17  # default is (Control-Q)
        self.key_size_up = K_F1
        self.key_size_down = K_F2
        self.keys_non_unicode = [K_UP, K_DOWN, K_LEFT, K_RIGHT, self.key_size_up,
                                 self.key_size_down]

    def _char(self, x, y):
        '''Get the char at a particular X/Y point on the display. '''
        return self._chars[x][y][0]

    def _color(self, x, y):
        '''Get the color at a particular X/Y point on the display.
        And convert the integer you get to an RGB tuple.
        '''
        return color_int2tuple(self._chars[x][y][1])

    def _font_at(self, x, y):
        '''Get the font at a particular X/Y point on the display.
        '''
        return self._chars[x][y][2], self._chars[x][y][3]

    def _rect(self, x, y):
        '''Given the X/Y coordinate of the character on the screen, create
        a rectangular bounding box in pixels space
        '''
        return pygame.Rect(x * self._x_font_size, y * self._y_font_size,
                           self._x_font_size, self._y_font_size)

    def boxes(self):
        '''Return a dictionary of the bounding boxes
        for all included windows by their id
        '''
        return self._boxes

    def id(self):
        '''A (hopefully) unique id for the current screen or window.
        This is zero on the main screen, but must be overriden in subclasses.
        in subclasses.'''
        return 0

    def x(self):
        '''X coord of the top-left corner of the window.
        This is zero on the main screen, but must be overriden in subclasses.
        '''
        return 0

    def y(self):
        '''Y coord of the top-left corner of the window.
        This is zero on the main screen, but must be overriden in subclasses.
        '''
        return 0

    def width(self):
        '''Number of columns of text in the window'''
        return self._width

    def height(self):
        '''Number of rows of text in the window'''
        return self._height

    def screen(self):
        '''get the pygame display'''
        return self._screen

    def font_size(self):
        '''Get the size of the current font'''
        return self._font_size

    def set_font_size(self, num):
        '''Public Setter for font size'''
        self._font_size = num

    def font(self, is_obli=False, is_bold=False):
        '''Get the pygame font object'''
        return self._font[is_obli][is_bold]

    def init_font_paths(self):
        '''Initialize all four fonts.
        '''
        for is_obli in [False, True]:
            for is_bold in [False, True]:
                path = os.path.join(self.RESOURCE_DIR, self.FONT[is_obli][is_bold])
                self._font_path[is_obli][is_bold] = resource_filename(self.PYTEXTGAME, path)

    def set_font_path(self, font, is_obli, is_bold):
        '''Set one of the four basic fonts: normal, oblique (italic), bold, and bold/oblique.
        NOTE: Screen size is determined based off the normal font.
        NOTE: If you choose unrelated fonts for each of the four cases, they may not be the
        same size and your display will come out looking strange.
        '''
        self._font_path[is_obli][is_bold] = font

    def reset_font(self):
        '''Reset all four fonts.
        Also has to reset the pygame display for this change to take effect.
        '''
        for is_obli in [False, True]:
            for is_bold in [False, True]:
                path = self._font_path[is_obli][is_bold]
                self._font[is_obli][is_bold] = pygame.font.Font(path, self._font_size)
        (x, y) = self._font[False][False].size('@')
        self._x_font_size = x
        self._y_font_size = y
        self._screen = pygame.display.set_mode((x * self._width, y * self._height),
                                               pygame.RESIZABLE)

    def subwin(self, height, width, y, x, color=WHITE):
        '''Add the bounding box frame for a given bounding box
        And then return a related sub-window'''
        self._id += 1
        self._boxes[self._id] = None

        return SubWin(self, self._id, height, width, y, x, color)

    def addstr(self, y, x, text, color=WHITE, is_obli=False, is_bold=False):
        '''Add a string to the 2D window character list,
        given an X-position, Y-position, string, and color
        '''
        dx = 0

        for c in text:
            self._chars[x + dx][y] = (c, color, is_obli, is_bold)
            dx += 1

    def refresh(self):
        '''clear the screen and then fill it with color characters'''
        # clear the screen
        self.screen().fill(self._bgcolor)

        # draw each character onto the screen
        for x in range(self.width()):
            for y in range(self.height()):
                char  = self._char(x, y)
                color = self._color(x, y)
                is_obli, is_bold = self._font_at(x, y)
                text  = self.font(is_obli, is_bold).render(char, True, color)
                # blit: display one image over another
                self.screen().blit(text, self._rect(x, y))

        # draw each window box onto the screen
        for box in self.boxes().values():
            if box is None:
                continue

            self._draw_box(box)

        # flip: send the final image to the screen
        pygame.display.flip()

    def clear(self):
        '''wipe out the boxes and empty the contents of all subwindows'''
        self._boxes = {0: None}

        for x in range(self.width()):
            for y in range(self.height()):
                self.addstr(y, x, ' ', BLACK)

    def box(self):
        '''put a box around this whole screen (could be a window)'''
        self.add_box(self)

    def add_box(self, win):
        '''Add a box around any arbitrary window'''
        self._boxes[win.id()] = (win.x(), win.y(), win.width(), win.height(), win.color())

    def del_box(self, window):
        '''delete a box from the collection on the screen'''
        self._boxes[window.id()] = None

    def _draw_box(self, box):
        '''actually draw the box onto the screen right now'''
        (x, y, width, height, color) = box

        px = x * self._x_font_size + self._x_font_size / 2
        py = y * self._y_font_size + self._y_font_size / 2
        pw = width * self._x_font_size - self._x_font_size
        ph = height * self._y_font_size - self._y_font_size

        pygame.draw.rect(self.screen(), color_int2tuple(color),
                         pygame.Rect(px, py, pw, ph), 1)

    def getch(self):
        '''get raw characters of user input'''
        key = None

        for event in pygame.event.get():
            if event.type == QUIT:
                # configurable quit-game key
                return self.key_quit
            elif event.type == KEYDOWN:
                # here is where we parse all real keyboard inputs
                if event.key in self.keys_non_unicode:
                    # special keys, like arrow and function keys (configurable list)
                    key = event.key
                elif len(event.unicode) >= 1:
                    # typical case: return a typed letter or number
                    key = ord(event.unicode)
            elif event.type == VIDEORESIZE:
                # for when a user drags the corner of the window to resize it
                key = NULL_KEY

        return key

    def getch_original(self):
        '''get raw characters of user input'''
        key = None

        while key is None:
            for event in pygame.event.get():
                if event.type == QUIT:
                    # configurable quit-game key
                    return self.key_quit
                elif event.type == KEYDOWN:
                    # here is where we parse all real keyboard inputs
                    if event.key in self.keys_non_unicode:
                        # special keys, like arrow and function keys (configurable list)
                        key = event.key
                    elif len(event.unicode) >= 1:
                        # typical case: return a typed letter or number
                        key = ord(event.unicode)
                elif event.type == VIDEORESIZE:
                    # for when a user drags the corner of the window to resize it
                    key = NULL_KEY

        return key

    def set_caption(self, caption):
        '''This is currently just a pass through for the pygame caption.'''
        pygame.display.set_caption(caption)

    def set_icon(self, icon):
        '''This is mostly just a pass through to pygame, to make
        the pytextgame API cleaner.
        '''
        pygame.display.set_icon(pygame.image.load(icon))

    def set_repeat(self, delay, interval):
        '''Open the API to allow for control over key repeat speed'''
        pygame.key.set_repeat(delay, interval)

    def set_bgcolor(self, tup):
        '''Public background color setter method'''
        self._bgcolor = tup

    def bgcolor(self):
        '''Public background color getter method'''
        return self._bgcolor


class SubWin(object):

    def __init__(self, stdscr, id, height, width, y, x, color=WHITE):
        self._stdscr = stdscr
        self._id     = id
        self._x      = x
        self._y      = y
        self._width  = width
        self._height = height
        self._color  = color

    def stdscr(self):
        '''A reference to the container screen for this subwindow'''
        return self._stdscr

    def id(self):
        '''Used to identify which subwindow is on the screen'''
        return self._id

    def x(self):
        '''X-coordinate of the top-left corner of subwindow bounding box'''
        return self._x

    def y(self):
        '''Y-coordinate of the top-left corner of subwindow bounding box'''
        return self._y

    def width(self):
        '''how wide the subwindow box is, counting by characters'''
        return self._width

    def height(self):
        '''how tall the subwindow box is, counting by characters'''
        return self._height

    def color(self):
        '''An integer representing the color of the subwindow'''
        return self._color

    def clear(self):
        '''replace every character in the subwindow with a blank'''
        self.stdscr().del_box(self)

        for x in range(self.width()):
            for y in range(self.height()):
                self.addstr(y, x, ' ', BLACK)

    def box(self):
        '''Add a bounding box for this subwindow to the main screen'''
        self.stdscr().add_box(self)

    def addstr(self, y, x, text, color=WHITE, is_obli=False, is_bold=False):
        '''Add a string to the subwindow, at X/Y, and give the color'''
        self.stdscr().addstr(y + self.y(), x + self.x(), text, color, is_obli, is_bold)
