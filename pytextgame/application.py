'''Minimal sketch of pytextgame apps'''


class Application(object):

    def __init__(self):
        self._new_ui = False
        self._events  = []

    # TODO: Is this method, and self._running an artifact of the minimal number of game screens?
    #       Does this need to go when we have more than play/do_scores?
    def new_ui(self):
        '''TODO: Is the application currently running, or is the game over?'''
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

    def current_situation(self):
        '''What is the current situation?'''
        raise 'Not implemented'

    # TODO: What does this do again? Resolve a sequence of events?
    def resolve_situation(self, situation):
        raise 'Not implemented'

    def available_actions(self):
        '''Return a list of actions that are currently valid'''
        raise 'Not implemented'


# TODO: Game seems to be designed for two game states: the game itself and the score/end/win/loss screen.
#       This seems very limiting. I need to open this up to multiple screens.
class Game(Application):

    def __init__(self):
        Application.__init__(self)

        self._won = False

    # TODO: a bit archaic, should be part of the UI switching system
    def has_won(self):
        '''Returns a stored boolean that says if the game has been won'''
        return self._won

    def win(self):
        '''Once you win the game, flip the switch and stop the game'''
        self._won = True
        self.stop()

    def do_turn(self):
        '''The meat of the game logic will go here'''
        raise 'Not implemented'

    # TODO: This is a remnant of the time before UI switching
    def score(self):
        '''perform the scoreboard logic'''
        raise 'Not implemented'


# TODO: Possibly move this to it's own module.
# TODO: You can have multiple Displays, and each display might have multiple possible situations.
class Situation(object):

    def __init__(self, model, name=None):
        # model is a subclass of Game
        self._model = model
        self._name  = name

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

    def __str__(self):
        return self.name()
