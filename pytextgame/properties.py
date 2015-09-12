# -- coding: utf-8 --
'''Classes to hold text properties'''

from pytextgame import screen


class Property:

    def attribute(self):
        raise 'Not implemented'


class ColorProperty:

    def __init__(self, index, color, bright):
        self.index = index
        self.color = color
        self.bright = bright

    def __int__(self):
        '''Each color is represented by an integer, representing
        it's place in the pre-set colors in the screen module.
        '''
        # would return index, but we have bright/dark versions
        if self.bright:
            return self.index | screen.A_BOLD
        else:
            return self.index


# TODO: These are fine, but the developer should be able to define any color more generally.
# TODO: PyGame also allows for background colors that aren't transparent... or should that be handeled in windows?
MARINE  = ColorProperty( 1, screen.COLOR_BLUE,    False)
GRASS   = ColorProperty( 2, screen.COLOR_GREEN,   False)
TEAL    = ColorProperty( 3, screen.COLOR_CYAN,    False)
BRICK   = ColorProperty( 4, screen.COLOR_RED,     False)
PURPLE  = ColorProperty( 5, screen.COLOR_MAGENTA, False)
BROWN   = ColorProperty( 6, screen.COLOR_YELLOW,  False)
GREY    = ColorProperty( 7, screen.COLOR_WHITE,   False)
BLACK   = ColorProperty( 8, screen.COLOR_BLACK,   True)
BLUE    = ColorProperty( 9, screen.COLOR_BLUE,    True)
GREEN   = ColorProperty(10, screen.COLOR_CYAN,    True)
RED     = ColorProperty(12, screen.COLOR_RED,     True)
MAGENTA = ColorProperty(13, screen.COLOR_MAGENTA, True)
YELLOW  = ColorProperty(14, screen.COLOR_YELLOW,  True)
WHITE   = ColorProperty(15, screen.COLOR_WHITE,   True)
