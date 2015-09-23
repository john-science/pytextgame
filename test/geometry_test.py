import unittest
from pytextgame.geometry import Position


class TestCube(unittest.TestCase):

    def setUp(self):
        pass

    def test_number_4(self):
        self.assertEqual(64, 64)

    def test_negative_one(self):
        self.assertEqual(-1, -1)


if __name__ == '__main__':
    unittest.main()
