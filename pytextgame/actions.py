'''General action classes.'''

import sys


class Action(object):

    def __init__(self, situation, name, suffix=None):
        '''Actions subclass nothing, but require situations to hold them'''
        # a situation is like "outdoors", "indoors", or "fighting"
        self.situation = situation
        self._game = None if situation is None else situation.game()
        # "name" is a string for the action & "suffix" is extra information. e.g. Move, North
        self.name = name
        self.suffix = suffix

    def game(self):
        '''getting the current subclass of game'''
        return self._game

    def info(self):
        '''placeholder: generic return a string describing this action'''
        return ''

    def always_known(self):
        '''Is this action Always Known in this game?'''
        return False

    def can_do(self):
        '''Each action will have to define a method that determines
        if the action is currently valid or not.
        '''
        raise Exception("Not Implemented")

    def do(self):
        '''Each Action will have to define a method that will
        actually perform some changes to the Game or UI
        '''
        raise Exception("Not Implemented")

    def execute(self):
        '''Convience method, checks if the action can be performed,
        if so it does it.
        '''
        if not self.can_do():
            return

        self.do()

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


class ActionKeys(dict):

    def __setitem__(self, key, value):
        '''Simple type-checking for the Action Key Dict'''
        if not isinstance(key, str):
            raise TypeError('The action keys key must be a string.')
        if not isinstance(value, int):
            raise TypeError('The action keys value must be an integer.')

        dict.__setitem__(self, key, value)

