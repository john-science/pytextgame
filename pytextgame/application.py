'''General sketch of running applications.'''


class Application:

    def __init__(self):
        self._running = False
        self._events  = []

    def is_running(self):
        return self._running

    def start(self):
        self._running = True
        self.do_start()

    def stop(self):
        self.do_stop()
        self._running = False

    def do_start(self):
        pass

    def do_stop(self):
        pass

    def add_events(self, events):
        self._events += events

    def new_events(self):
        events = self._events
        self._events = []

        return events

    def current_situation(self):
        raise 'Not implemented'

    def resolve_situation(self, situation):
        raise 'Not implemented'

    def available_actions(self):
        raise 'Not implemented'


# TODO: Game seems to be designed for two game states: the game itself and the score/end/win/loss screen.
#       This seems very limiting. I need to open this up to multiple screens.
class Game(Application):

    def __init__(self):
        Application.__init__(self)

        self._won = False

    def has_won(self):
        return self._won

    def win(self):
        self._won = True
        self.stop()

    def do_turn(self):
        raise 'Not implemented'

    def score(self):
        raise 'Not implemented'


# TODO: You can have multiple Displays, and each display might have multiple possible situations.
class Situation:

    def __init__(self, model, name=None):
        # model is a subclass of Game
        self._model = model
        self._name  = name

    def model(self):
        return self._model

    def allow_other_actions(self):
        return True

    def resolve(self):
        self.model().resolve_situation(self)

    def available_actions(self):
        raise 'Not implemented'

    def __str__(self):
        return self.name()
