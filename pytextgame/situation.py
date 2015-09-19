'''Minimal sketch of pytextgame apps'''


class Situation(object):

    def __init__(self, game):
        # TODO: consider chaning the name model to game
        self._game = game

    def game(self):
        '''Return the current subclass of Game'''
        return self._game

    def allow_other_actions(self):
        '''This is for special cases, like the final credit screen,
        where the only optinon it to quit the game.
        '''
        return True

    def resolve(self):
        '''resolve the current situation in game'''
        self.game().resolve_situation(self)

    def available_actions(self):
        '''Return a collection of valid actions'''
        raise 'Not implemented'
