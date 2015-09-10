'''Curses-like attributes.'''

from pytextgame import cursesemu


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
        it's place in the pre-set colors in cursesemu.
        '''
        # would return index, but we have bright/dark versions
        if self.bright:
            return self.index | cursesemu.A_BOLD
        else:
            return self.index


# TODO: Make sure I can use dark and bright colors correctly.
# TODO: These are fine, but the developer should be able to provide 3 numbers to define any old color.
# TODO: PyGame also allows for background colors that aren't transparent... or should that be handeled in windows?
MARINE  = ColorProperty( 1, cursesemu.COLOR_BLUE,    False)
GRASS   = ColorProperty( 2, cursesemu.COLOR_GREEN,   False)
TEAL    = ColorProperty( 3, cursesemu.COLOR_CYAN,    False)
BRICK   = ColorProperty( 4, cursesemu.COLOR_RED,     False)
PURPLE  = ColorProperty( 5, cursesemu.COLOR_MAGENTA, False)
BROWN   = ColorProperty( 6, cursesemu.COLOR_YELLOW,  False)
GREY    = ColorProperty( 7, cursesemu.COLOR_WHITE,   False)
BLACK   = ColorProperty( 8, cursesemu.COLOR_BLACK,   True)
BLUE    = ColorProperty( 9, cursesemu.COLOR_BLUE,    True)
GREEN   = ColorProperty(10, cursesemu.COLOR_GREEN,   True)
CYAN    = ColorProperty(11, cursesemu.COLOR_CYAN,    True)
RED     = ColorProperty(12, cursesemu.COLOR_RED,     True)
MAGENTA = ColorProperty(13, cursesemu.COLOR_MAGENTA, True)
YELLOW  = ColorProperty(14, cursesemu.COLOR_YELLOW,  True)
WHITE   = ColorProperty(15, cursesemu.COLOR_WHITE,   True)
