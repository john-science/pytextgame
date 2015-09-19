'''Basic event classes.'''


class Event(object):

    def __init__(self, source, target):
        if source is not None:
            self._model = source.model()

        self._source = source
        self._target = target

    def model(self):
        '''Returns the current subclass of Game'''
        return self._model

    def source(self):
        '''TODO'''
        return self._source

    def target(self):
        '''TODO'''
        return self._target

    def description(self):
        raise 'Not implemented'

    def do(self):
        raise 'Not implemented in ' + str(self)
