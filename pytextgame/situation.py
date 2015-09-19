'''Minimal sketch of pytextgame apps'''


# TODO: You can have multiple Displays, and each display might have multiple possible situations.
class Situation(object):

    def __init__(self, model):
        # TODO: consider chaning the name model to game
        self._model = model

    def model(self):
        '''Return the model, a subclass of Game'''
        return self._model

    # TODO: Why bother?
    def allow_other_actions(self):
        return True

    def resolve(self):
        '''resolve the current situation in game'''
        self.model().resolve_situation(self)

    def available_actions(self):
        '''Return a collection of valid actions'''
        raise 'Not implemented'
