import unittest
from pytextgame.geometry import Position


class TestCube(unittest.TestCase):

    def setUp(self):
        pass

    def test_position_attributes(self):
        posi = Position(5, 7)
        self.assertEqual(posi.x, 5)
        self.assertEqual(posi.y, 7)

    def test_position_distance_x(self):
        pos1 = Position(5, 0)
        pos2 = Position(10, 0)
        self.assertEqual(pos1.distance(pos2), 5)


if __name__ == '__main__':
    unittest.main()
