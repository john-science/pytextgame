# -- coding: utf-8 --
'''Simple UIs for Text Games in Python,
built on pygame
'''

from pytextgame import screen


class TextUI:

    def __init__(self, num_rows, num_cols, icon):
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._icon = icon

    def main(self):
        '''Start the PyGame screen'''
        screen.wrapper(lambda stdscr: self.set_up_and_run(stdscr),
                       self._num_rows, self._num_cols, self._icon)

    def set_up_and_run(self, stdscr):
        '''Set up and run the UI, though this class does not implement
        the details necessary to do so.
        '''
        self.stdscr = stdscr
        self.init()
        self.run()

    def get_key(self):
        '''Get a key that has been pressed using the
        pygame interface.
        '''
        return self.stdscr.getch()

    def init(self):
        raise 'Not implemented'

    def run(self):
        raise 'Not implemented'


class TextGameUI(TextUI):

    def __init__(self, model):
        TextUI.__init__(self, model.num_rows, model.num_cols, model.icon)
        self.model = model
        self._null_key = False

    def init(self):
        pass

    def run(self):
        '''just filling the superclasses method with game logic'''
        self.do_game()

    def do_game(self):
        '''master method to handle rendering displaying,
        modifying game state, and handling user input
        '''
        self.model.start()

        while self.model.is_running():
            self.model.do_turn()
            self.do_turn()

    def prepare_turn(self):
        pass

    def do_turn(self):
        '''Do a single turn of render-input
        Allow to render using memoized data from last pull,
        if no user-input is given.
        '''
        # pull information necessary to render
        self.prepare_turn()

        # render screen
        if self._null_key:
            # if only null user input, render using memoized screen
            self.display_last()
            self._null_key = False
        else:
            # render fresh screen
            self.display()

        # look for user input and perform necessary actions
        self.act()

    def do_scores(self):
        # TODO: Just scores? We need better support for multiple menus.
        pass

    def display(self):
        '''display every window in this UI'''
        # re-draw every sub-window
        for window in self.displayed_windows():
            window.display()

        self.stdscr.refresh()

    def display_last(self):
        '''In the situation where a null input was recieved from user
        (window resize, etc), simply re-draw the last screen
        using the memoized data
        '''
        for window in self.displayed_windows():
            window.stdscr.refresh()

    def create_window(self, kind, rect, border=True):
        '''Helper method to add a subwindow to the screen'''
        return kind(self, self.stdscr, self.model, rect, border)

    def act(self):
        '''wait for user input and perform any actions necessary
        if a null key is returned, no actions are necessary
        '''
        acted = False

        # TODO: This and the 'screen.getch' need to be combined.
        #       We want to allow for the GUI to change even when the user doesn't press a key.
        while not acted:
            key = self.get_key()

            # null key is for screen re-sizing, quiting the game, etc
            if key == screen.NULL_KEY:
                self._null_key = True
                return

            self.display()

            actions = self.model.available_actions()
            for action in actions:
                if self.key_for(action) == key:
                    acted = action.execute()

    # TODO: Must be implemented by the specific GameUI... make sure this is convenient.
    def char_for(self, action):
        raise 'Not implemented'

    # TODO: Must be implemented by the specific GameUI... make sure this is convenient.
    def key_for(self, action):
        raise 'Not implemented'

    # TODO: Must be implemented by the specific GameUI... make sure this is convenient.
    def group_for(self, action):
        '''Get an action name from the GROUP dict'''
        raise 'Not implemented'

    def displayed_windows(self):
        '''Return a list of subwindows'''
        raise 'Not implemented'

    def window(self, name):
        '''Get a window based on it's name key'''
        raise 'Not implemented'
