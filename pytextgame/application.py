'''Minimal sketch of pytextgame apps'''


class Application(object):

    def __init__(self):
        self._situations = {}
        self.situation = None
        self._new_ui = False
        self._events  = []

    def new_ui(self):
        '''returns False or a string keyword for the new UI'''
        return self._new_ui

    def set_new_ui(self, ui_str):
        '''Setter for new UI representative string'''
        self._new_ui = ui_str

    def start(self):
        '''Start the game'''
        self._new_ui = False
        self.do_start()

    def stop(self):
        '''Stop the game'''
        self.do_stop()
        self._new_ui = False

    def do_start(self):
        '''Perform initial setup of the Game and state'''
        pass

    def do_stop(self):
        '''A convience method, perhaps you always want to save
        when the game is stopped, or you need to clean up your
        cache/database. Do so here.
        '''
        pass

    def add_events(self, events):
        '''Add events to the queue'''
        self._events += events

    def new_events(self):
        '''Pull all possible events and clear out the queue'''
        events = self._events
        self._events = []

        return events

    def set_situation(self, situation_str):
        '''TODO'''
        self.situation = self._situations[situation_str](self)

    def resolve_situation(self, situation):
        '''TODO'''
        raise 'Not implemented'

    def available_actions(self):
        '''Return a list of actions that are currently valid'''
        raise 'Not implemented'


class Game(Application):

    def __init__(self):
        Application.__init__(self)

    def do_turn(self):
        '''The meat of the game logic will go here'''
        raise 'Not implemented'


# TODO: Possibly move this to it's own module.
# TODO: You can have multiple Displays, and each display might have multiple possible situations.
class Situation(object):

    def __init__(self, model):
        # TODO: consider chaning the name model to game
        self._model = model

    def model(self):
        '''Return the model, a subclass of Game'''
        return self._model

    # TODO: Why do I need this?
    def allow_other_actions(self):
        return True

    def resolve(self):
        '''resolve the current situation in game'''
        self.model().resolve_situation(self)

    def available_actions(self):
        '''Return a collection of valid actions'''
        raise 'Not implemented'
