
import unittest
from pytextgame.geometry import Direction, Position, Rectangle


class TestGeometry(unittest.TestCase):

    def setUp(self):
        self.pos1 = Position(5, 0)
        self.pos2 = Position(10, 0)
        self.pos3 = Position(9, 3)
        self.dir1 = Direction(1, 1)
        self.dir2 = Direction(5, 0)
        self.dir3 = Direction(7, 14)
        self.rect1 = Rectangle(0, 0, 5, 5)
        self.rect2 = Rectangle(5, 10, 65, 60)

    def test_position_attributes(self):
        self.assertEqual(self.pos1.x, 5)
        self.assertEqual(self.pos1.y, 0)

    def test_position_distance_x(self):
        self.assertEqual(self.pos1.distance(self.pos2), 5)

    def test_position_distance_345(self):
        self.assertEqual(self.pos1.distance(self.pos3), 5.0)

    def test_translate_five(self):
        self.pos1.translate(self.dir2)
        self.assertEqual(self.pos1.x, self.pos2.x)
        self.assertEqual(self.pos1.y, self.pos2.y)

    def test_direction_of_position(self):
        direct = self.pos2.direction()
        self.assertEqual(direct.dx, 10)
        self.assertEqual(direct.dy, 0)

    def test_direction_to_position(self):
        direct = self.pos2.direction_to(self.pos3)
        self.assertEqual(direct.dx, -1)
        self.assertEqual(direct.dy, 3)

    def test_rectangle_area(self):
        self.assertEqual(self.rect1.area(), 25)

    def test_rectangle_diagonal(self):
        self.assertEqual(self.rect2.diagonal().dx, 65)
        self.assertEqual(self.rect2.diagonal().dy, 60)

    def test_direction_invert(self):
        self.dir1.invert()
        self.assertEqual(self.dir1.dx, -1)
        self.assertEqual(self.dir1.dy, -1)

    def test_direction_scale(self):
        self.dir2.scale(2)
        self.assertEqual(self.dir2.dx, 10)
        self.assertEqual(self.dir2.dy, 0)

    def test_direction_descale(self):
        self.dir3.descale(7)
        self.assertEqual(self.dir3.dx, 1)
        self.assertEqual(self.dir3.dy, 2)


if __name__ == '__main__':
    unittest.main()
