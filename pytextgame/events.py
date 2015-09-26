'''Basic event classes.'''


class Event(object):

    def __init__(self, source, target):
        self._target = target
        self._source = source
        # _game could also be anything that includes a reference to the game object
        self._game = source.game() if source is not None else None

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


class ClockTickEvent(Event):

    def __init__(self, source, target, event_rate):
        Event.__init__(self, source, target)
        self.event_rate = event_rate  # units in ms
        self.time_passed = 1          # units in ms
