
import unittest
from pytextgame.colors import *
from pytextgame.actions import Action, ActionKeys


class TestActions(unittest.TestCase):

    def test_add_one_action(self):
        actions = ActionKeys()
        actions['quit'] = ord('Q')
        self.assertEqual(actions.keys(), ['quit'])
        self.assertEqual(actions['quit'], ord('Q'))

    def test_add_broken_key(self):
        actions = ActionKeys()
        with self.assertRaises(TypeError):
            actions[123] = ord('Q')

    def test_add_broken_value(self):
        actions = ActionKeys()
        with self.assertRaises(TypeError):
            actions['faux'] = 'broken'


if __name__ == '__main__':
    unittest.main()
