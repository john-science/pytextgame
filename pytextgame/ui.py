# -- coding: utf-8 --
'''Simple UIs for Text Games in Python,
built on pygame
'''

import string
import sys
from pytextgame import screen
from pytextgame.displays import Displays
from pytextgame.actions import ActionKeys
from pytextgame.window import Window, Windows
from colors import WHITE
if sys.version_info[0] < 3: chr = unichr


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
        self.printable = string.printable.translate(None, "\r\n\t\x0b\x0c")
        self.text_entry_specials = u'\u0114\r\x08\x7f'
        self._null_key = False
        self.action_keys = ActionKeys()
        self.windows = Windows()
        self.fresh_displays = Displays()

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

        while True:
            # UI-switching logic
            if self.game.new_ui():
                self.update_windows(self.game.new_ui())
                self.game.set_new_ui(False)
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
            # if only null user input (like screen resize), render using memoized screen content
            self.display_last()
            self._null_key = False
        else:
            # render fresh screen
            self.display()

        # look for user input and perform necessary actions
        self.act()

    def act(self):
        '''wait for user input and perform any actions necessary
        if a null key is returned, no actions are necessary
        '''
        acted = False

        # TODO: Allow for the GUI to change even when the user doesn't press a key.
        while not acted:
            key = self.get_key()

            # null key is for screen re-sizing, quiting the game, etc
            if key == screen.NULL_KEY:
                self._null_key = True
                return
            elif key in [self.stdscr.key_size_up, self.stdscr.key_size_down]:
                self.resize_window(key)
                return

            self.display()
            acted = self._act_on_key(key)

    def _act_on_key(self, key):
        '''execute actions based on the user's input key'''
        acted = False

        if self.game.text_entry:
            if chr(key) not in self.printable + self.text_entry_specials:
                return acted
            # use the Game's built-in text entry functionality
            action = self.game.text_entry_action(key)
            acted = action.execute()
        else:
            # find the string for each action and see if the key is in the action_keys dict
            actions = self.game.available_actions()
            for action in actions:
                if self.key_for(action) == key:
                    acted = action.execute()

        return acted

    def resize_window(self, key):
        '''Resize the window up or down'''
        if key == self.stdscr.key_size_up:
            self.stdscr._font_size += 1
            self.stdscr.reset_font()
        elif key == self.stdscr.key_size_down:
            if self.stdscr._font_size > 5:
                self.stdscr._font_size -= 1
                self.stdscr.reset_font()

    def key_for(self, action):
        '''Determine if the key in question is for a particular action'''
        raise Exception('Not Implemented')

    def displayed_windows(self):
        '''Return a list of subwindows'''
        return self.windows.values()

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
