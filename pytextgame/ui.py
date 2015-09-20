# -- coding: utf-8 --
'''Simple UIs for Text Games in Python,
built on pygame
'''

from pytextgame import screen
from pytextgame.window import Window, Windows
from colors import WHITE


class TextUI(object):

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
        raise Exception("Not Implemented")

    def run(self):
        raise Exception("Not Implemented")


class TextGameUI(TextUI):

    def __init__(self, game):
        TextUI.__init__(self, game.num_rows, game.num_cols, game.icon)
        self.game = game
        self._null_key = False
        self.windows = Windows()
        self.fresh_displays = {}

    def init(self):
        pass

    def run(self):
        '''just filling the superclasses method with game logic'''
        self.do_game()

    def do_game(self):
        '''master method to handle rendering displaying,
        modifying game state, and handling user input
        '''
        self.game.start()

        # TODO: Along with new UI, I need to provide a new situation, which can swap out the available keys/actions.
        while True:
            if self.game.new_ui():
                # UI-switching logic
                if self.game.new_ui():
                    self.update_windows(self.game.new_ui())
                    self.game._new_ui = False  # TODO: sigh... setters and getters...
            self.game.do_turn()
            self.do_turn()

    def prepare_turn(self):
        '''setup whatever you need for this turn'''
        raise Exception("Not Implemented")

    def do_turn(self):
        '''Do a single turn of render-input
        Allow to render using memoized data from last pull,
        if no user-input is given.
        '''
        # setup information necessary to render
        self.prepare_turn()

        # render screen
        if self._null_key:
            # if only null user input, render using memoized screen
            self.display_last()  # TODO: Why do I have to re-render at all? Why not just let it be?
            self._null_key = False
        else:
            # render fresh screen
            self.display()

        # look for user input and perform necessary actions
        self.act()

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

    def create_window(self, kind, rect, border=WHITE):
        '''Helper method to add a subwindow to the screen'''
        return kind(self, self.stdscr, self.game, rect, border)

    def update_windows(self, display):
        '''Update the display of all windows on the screen
        '''
        self.windows = Windows()
        self.stdscr.clear()
        for wname, wlst in self.fresh_displays[display].iteritems():
            if len(wlst) == 2:
                self.windows[wname] = self.create_window(wlst[0], wlst[1])
            elif len(wlst) == 3:
                self.windows[wname] = self.create_window(wlst[0], wlst[1], wlst[2])
            else:
                raise ValueError('TODO: Is there a better way? Type checking on fresh_displays?')

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

            # TODO: This loop seems unnecessary... just have a dictionary of actions, right?
            actions = self.game.available_actions()
            for action in actions:
                if self.key_for(action) == key:
                    acted = action.execute()

    def add_window(self, key_name, window):
        '''Helper method to correctly build a dictionary of Windows'''
        key_name = str(key_name)
        if not isinstance(window, Window):
            raise TypeError('You cannot add that, because it is not a Window.')

        self.windows[key_name] = window

    def displayed_windows(self):
        '''Return a list of subwindows'''
        return self.windows.values()

    def window(self, name):
        '''Get a window using it's name key'''
        return self.windows.get(name, None)
