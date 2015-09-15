'''General action classes.'''

import sys


class Action:

    def __init__(self, situation, name, suffix = None):
        # situation is like "outdoors" or "indoors"
        self.situation = situation

        # TODO: A better default in Situation would remove this 'if' block.
        # model is subclass of game
        if situation is None:
            self._model = None
        else:
            self._model = situation.model()

        self.name   = name
        self.suffix = suffix

    def set_situation(self, situation):
        self.situation = situation
        self._model    = situation.model()

    def model(self):
        return self._model

    def info(self):
        return ''

    def always_known(self):
        return False

    def can_do(self):
        raise 'Not implemented'

    def do(self):
        raise 'Not implemented'

    def execute(self):
        if not self.can_do():
            return False

        self.do()

        return True

    def __str__(self):
        if self.suffix is None:
            return self.name

        return '%s: %s' % (self.name, self.suffix)


class QuitAction(Action):

    def __init__(self, situtation):
        Action.__init__(self, situtation, 'Quit')

    def can_do(self):
        return True

    def do(self):
        sys.exit()


class NullAction(Action):

    def __init__(self, situtation):
        Action.__init__(self, situtation, 'Do Nothing')

    def can_do(self):
        return True

    def do(self):
        pass
