'''General action classes.'''

import sys


# TODO: Perhaps _model would be more clear if it were _app or _game.
class Action(object):

    def __init__(self, situation, name, suffix=None):
        # situation is like "outdoors" or "indoors"
        self.situation = situation

        # model is subclass of game
        self._model = None if situation is None else situation.game()

        self.name   = name
        self.suffix = suffix

    # TODO: Where is this used?
    def set_situation(self, situation):
        '''Set the containing situation for this action'''
        self.situation = situation
        self._model = situation.game()

    def model(self):
        '''getting for model (a subclass o game)'''
        return self._model

    def info(self):
        '''placeholder: generic return a string describing this action'''
        return ''

    # TODO: While swapping out GUIs/Windows, will this still be meaningful?
    def always_known(self):
        '''Is this action Always Known in this game?'''
        return False

    def can_do(self):
        '''Each action will have to define a method that determines
        if the action is currently valid or not.
        '''
        raise 'Not implemented'

    def do(self):
        '''Each Action will have to define a method that will
        actually perform some changes to the Game or UI
        '''
        raise 'Not implemented'

    def execute(self):
        '''Convience method, checks if the action can be performed,
        if so it does it.
        '''
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
        '''You can always exit the program.
        Break this functionality, and your users will hate you.
        '''
        return True

    def do(self):
        '''In this simple implementation, no window pops up
        to ask you if you're sure or if you want to save the game first.
        '''
        sys.exit()


class NullAction(Action):

    def __init__(self, situtation):
        Action.__init__(self, situtation, 'Do Nothing')

    def can_do(self):
        '''Doing nothing is always an option.'''
        return True

    def do(self):
        '''Sometimes the best thing you can do is nothing.'''
        pass
