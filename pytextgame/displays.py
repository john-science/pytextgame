# -- coding: utf-8 --
'''A display is a collection of windows that together make up one unique view in the game.
Different parts of the game may have different displays: loading screen, game screen,
end credits, etc...
'''

from colors import WHITE


class Displays(dict):

    def __setitem__(self, display_name, windows):
        '''This is just type validation for the displays'''
        if not isinstance(display_name, str):
            raise TypeError('Display names must be strings.')
        if not isinstance(windows, dict):
            raise TypeError('Display values must be a dictionary of Windows.')
        for key, item in windows.iteritems():
            if not isinstance(key, str):
                raise TypeError('Display windows must be given a string key')
            if not isinstance(item, list) or len(item) not in [2, 3]:
                raise TypeError('Display windows must be defined with a list of 2 or 3 parameters.')
            if len(item) == 2:
                windows[key].append(WHITE)

        dict.__setitem__(self, display_name, windows)
