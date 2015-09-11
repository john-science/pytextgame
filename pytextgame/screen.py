'''Create a basic text-grid screen using Pygame'''

import os
import pygame
import sys
import time
from pkg_resources import resource_stream, resource_filename
if sys.version_info[0] < 3: range = xrange

# Color Constants (TODO: Move to Properties?)
COLOR_BLACK   = 0
COLOR_BLUE    = 1
COLOR_GREEN   = 2
COLOR_CYAN    = 3
COLOR_RED     = 4
COLOR_MAGENTA = 5
COLOR_YELLOW  = 6
COLOR_WHITE   = 7
A_BOLD = 8
# Key Constants
KEY_UP    = 257
KEY_DOWN  = 258
KEY_LEFT  = 259
KEY_RIGHT = 260
NULL_KEY = 'Null Key'
# Resource Constants
PYTEXTGAME_DIR = 'pytextgame'
RESOURCE_DIR = 'resources'
ICON = 'rocket32.png'
FREE_MONO = 'FreeMono.ttf'
LUCIDA = 'Lucida Console'
DEFAULT_TITLE = 'PyTextGame'


def wrapper(method, num_rows, num_cols):
    '''
    This funtion exists to keep all references
    to pygame in this module.
    '''
    pygame.init()
    method(Screen(num_rows, num_cols))


class Screen:

    COLORS = [(  0,  0,  0), ( 32, 32, 192), (  0, 156,  0), (  0, 156, 156),
              (156,  0,  0), (156,  0, 156), (156, 156,  0), (156, 156, 156),
              ( 96, 96, 96), ( 96, 96, 255), ( 64, 255, 64), ( 64, 255, 255),
              (255, 64, 64), (255, 64, 255), (255, 255, 64), (255, 255, 255)]

    def __init__(self, height, width):
        pygame.key.set_repeat(250, 100)  # TODO: Should be configable?
        self._id = 0
        self._height = height
        self._width  = width
        self._font_size = 16             # TODO: Should be configable?
        self._font_name = LUCIDA         # TODO: Should be more configurable?
        self._bgcolor = (0, 0, 0)        # TODO: Should be configable?
        font_test = pygame.font.match_font(self._font_name)

        # TODO: Need to expose this, so it is not default.
        pygame.display.set_icon(pygame.image.load(resource_stream(__name__,
                                                  os.path.join(RESOURCE_DIR, ICON))))

        if font_test is None or font_test.lower().find(LUCIDA.split()[0].lower()) == -1:
            # Use FreeMono is system doesn't have Lucida
            self._font_name = FREE_MONO
            self.reset_font()
            self._size_window_4_font()
        else:
            # Do I really want to support System Fonts?
            self._font = pygame.font.SysFont(self._font_name, self._font_size)
            self._size_window_4_font()

        # TODO: Need to expose this, so it is not default.
        pygame.display.set_caption(DEFAULT_TITLE)

        self._chars = [[(' ', (0, 0, 0))
                        for y in range(height)]
                        for x in range(width)]

        self._boxes = {0: None}

    def _char(self, x, y):
        '''Get the char at a particular X/Y point on the display. '''
        return self._chars[x][y][0]

    def _color(self, x, y):
        '''Get the color at a particular X/Y point on the display.
        '''
        return self._chars[x][y][1]

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
        '''The main screen should have a static id'''
        return 0

    def x(self):
        '''The horizontal size of the font in pixels'''
        return 0

    def y(self):
        '''The vertical size of the font in pixels'''
        return 0

    # TODO: should I change the name of this to be "num_cols"?
    def width(self):
        '''Number of columns of text in the window'''
        return self._width

    # TODO: should I change the name of this to be "num_rows"?
    def height(self):
        '''Number of rows of text in the window'''
        return self._height

    def screen(self):
        '''get the pygame display'''
        return self._screen

    # TODO: more clearly demark local system fonts versus paths to fonts
    def font_name(self):
        '''Get the font path or name'''
        return self._font_name

    def font_size(self):
        '''Get the size of the current font'''
        return self._font_size

    def font(self):
        '''Get the pygame font object'''
        return self._font

    def reset_font(self):
        '''uses font name and font size, members of this class'''
        path = os.path.join(RESOURCE_DIR, FREE_MONO)
        path = resource_filename(PYTEXTGAME_DIR, path)
        self._font = pygame.font.Font(path, self._font_size)

    def subwin(self, height, width, y, x):
        '''Add the bounding box frame for a given bounding box
        And then return a related sub-window'''
        self._id += 1
        self._boxes[self._id] = None

        return SubWin(self, self._id, height, width, y, x)

    def addstr(self, y, x, text, color = COLOR_WHITE):
        '''Add a string to the 2D window character list,
        given an X-position, Y-position, string, and color
        '''
        dx = 0

        for c in text:
            self._chars[x + dx][y] = (c, self.COLORS[int(color)])
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
                text  = self.font().render(char, True, color)
                # blit: display one image over another
                self.screen().blit(text, self._rect(x, y))

        # draw each window box onto the screen
        for box in self.boxes().values():
            if box is None:
                continue

            (x, y, width, height) = box

            px = x * self._x_font_size + self._x_font_size / 2
            py = y * self._y_font_size + self._y_font_size / 2
            pw = width * self._x_font_size - self._x_font_size
            ph = height * self._y_font_size - self._y_font_size

            pygame.draw.rect(self.screen(), self.COLORS[COLOR_WHITE],
                             pygame.Rect(px, py, pw, ph), 1)

        # flip: send the final image to the screen
        pygame.display.flip()

    def clear(self):
        '''wipe out the boxes and empty the contents of all subwindows'''
        self._boxes = {0: None}

        for x in range(self.width()):
            for y in range(self.height()):
                self.addstr(y, x, ' ', COLOR_BLACK)

    def box(self):
        '''put a box around this whole screen (could be a window)'''
        self.add_box(self)

    def add_box(self, window):
        '''Add a box around any arbitrary window'''
        self._boxes[window.id()] = (window.x(), window.y(), window.width(), window.height())

    def del_box(self, window):
        '''delete a box from the collection on the screen'''
        self._boxes[window.id()] = None

    def getch(self):
        '''get raw characters of user input'''
        key = None

        while key is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return ord('Q')
                elif event.type == pygame.KEYDOWN:
                    # TODO: Shorten this? Map pygame.KEY_WHATEVER to CONSTANT
                    if event.key == pygame.K_UP:
                        key = KEY_UP
                    elif event.key == pygame.K_DOWN:
                        key = KEY_DOWN
                    elif event.key == pygame.K_LEFT:
                        key = KEY_LEFT
                    elif event.key == pygame.K_RIGHT:
                        key = KEY_RIGHT
                    elif event.key == pygame.K_F1:
                        self._font_size += 1
                        self.reset_font()
                        self._size_window_4_font()
                        key = NULL_KEY
                    elif event.key == pygame.K_F2:
                        if self._font_size > 5:
                            self._font_size -= 1
                            self.reset_font()
                            self._size_window_4_font()
                            key = NULL_KEY
                    elif len(event.unicode) >= 1:
                        key = ord(event.unicode)
                elif event.type == pygame.VIDEORESIZE:
                    key = NULL_KEY
                elif event.type == pygame.KEYUP:
                    key = None

        return key

    def _size_window_4_font(self):
        '''Updates the window size based on the requirements
        of the font size.
        '''
        (x, y) = self._font.size('@')
        self._x_font_size = x
        self._y_font_size = y
        self._screen = pygame.display.set_mode((x * self._width, y * self._height),
                                               pygame.RESIZABLE)


class SubWin:

    def __init__(self, stdscr, id, height, width, y, x):
        self._stdscr = stdscr
        self._id     = id
        self._x      = x
        self._y      = y
        self._width  = width
        self._height = height

    def stdscr(self):
        '''A reference to the container screen for this subwindow'''
        return self._stdscr

    def id(self):
        '''Used to identify which subwindow is on the screen'''
        return self._id

    # TODO: These coordinates, which corner is the origin?
    def x(self):
        '''X-coordinate of corner of subwindow bounding box'''
        return self._x

    # TODO: These coordinates, which corner is the origin?
    def y(self):
        '''Y-coordinate of corner of subwindow bounding box'''
        return self._y

    def width(self):
        '''how wide the subwindow box is, counting by characters'''
        return self._width

    def height(self):
        '''how tall the subwindow box is, counting by characters'''
        return self._height

    def clear(self):
        '''replace every character in the subwindow with a blank'''
        self.stdscr().del_box(self)

        for x in range(self.width()):
            for y in range(self.height()):
                self.addstr(y, x, ' ', COLOR_BLACK)

    # TODO: What if I want to change the color of the border?
    def box(self):
        '''Add a bounding box for this subwindow to the main screen'''
        self.stdscr().add_box(self)

    def addstr(self, y, x, text, color=COLOR_WHITE):
        '''Add a string to the subwindow, at X/Y, and give the color'''
        self.stdscr().addstr(y + self.y(), x + self.x(), text, color)
