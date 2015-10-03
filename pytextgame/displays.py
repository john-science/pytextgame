# -- coding: utf-8 --
'''A display is a collection of windows that together make up one unique view in the game.
Different parts of the game may have different displays: loading screen, game screen,
end credits, etc...
'''

from colors import WHITE
from geometry import Rectangle
from window import Window, LINE_BORDER


class Displays(dict):
    '''
    A single "display" would be a collection Windows used on the screen at the same time, in some
    layout for some game situation. These wouldn't be instantiated classes, but just the information
    necessary to create them. e.g.

    {'start_screen': {'start_new': [NewGameWindow, Rectangle(0, 0, 80, 24)]}}

    But a "displays" objedt has the screen layouts for many/all of the various screen layouts in
    the game?

    {'start_screen': {'start_new':   [NewGameWindow, Rectangle(0, 0, 80, 24)]}}
     'title_screen': {'title':       [TitleWindow, Rectangle(51, 16, 29, 8), LINE_BORDER, GRAY],
                      'new':         [NewWindow, Rectangle(51, 0, 29, 3)],
                      'load':        [LoadWindow, Rectangle(51, 3, 29, 13), SOLID_BORDER],
                      'artwork':     [MainArtworkWindow, Rectangle(0, 0, 51, 17)],
                      'exit':        [ExitWindow, Rectangle(0, 17, 51, 7)]},
     'end_game':     {'high_scores': [HighScoreWindow, Rectangle(0, 0, 80, 24)]}}

    This class exists to do type-checking on these dictionaries of displays information.
    '''

    def __setitem__(self, display_name, windows):
        '''This is just type validation for the displays'''
        if not isinstance(display_name, str):
            raise TypeError('Display names must be strings.')
        if not isinstance(windows, dict):
            raise TypeError('Display values must be a dictionary of Windows.')
        for key, item in windows.iteritems():
            if not isinstance(key, str):
                raise TypeError('Display windows must be given a string key')
            if not isinstance(item, list) or len(item) not in [2, 3, 4]:
                raise TypeError('Display windows must be defined with a list of 2 or 3 parameters.')
            if not issubclass(item[0], Window):
                raise TypeError('Displays must be collections of Windows, not: ' + str(type(item[0])))
            if not isinstance(item[1], Rectangle):
                raise TypeError('Each Window must be given a Rectangle, not: ' + str(type(item[1])))
            if len(item) == 2:
                windows[key].append(LINE_BORDER)
                windows[key].append(WHITE)
            elif len(item) == 3:
                windows[key].append(WHITE)

        dict.__setitem__(self, display_name, windows)
