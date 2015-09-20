'''Basic event classes.'''


class Event(object):

    def __init__(self, source, target):
        self._target = target
        self._source = source
        self._game = None
        if source is not None:
            self._game = source.game()

    def game(self):
        '''Returns the current subclass of Game'''
        return self._game

    def source(self):
        '''The source is typically a subclass of Position,
        something like a location or enemy
        '''
        return self._source

    def target(self):
        '''The target is typically a subclass of Position,
        Something like the player
        '''
        return self._target

    def description(self):
        raise Exception("Not Implemented")

    def do(self):
        raise Exception("Not Implemented in " + str(self))
