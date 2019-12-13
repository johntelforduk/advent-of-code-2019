# Unit tests for day 10 of AOC 2019, "Monitoring Station".
# https://adventofcode.com/2019/day/10


from asteroid_field import translation, rotation, angle_from_origin, angle, distance
from math import pi
import unittest


class TestTranslation(unittest.TestCase):

    def test_translation(self):
        self.assertEqual(translation((0, 0), (1, 2)), (1, 2))
        self.assertEqual(translation((-2, 3), (-1, -5)), (-3, -2))

    def test_rotation(self):
        self.assertEqual(rotation(vertex=(0, 0), rotation_radians=pi), (0, 0))
        self.assertEqual(rotation(vertex=(1, 1), rotation_radians=-pi / 2), (-1, 1))    # Anti-clockwise 180 degrees.
        self.assertEqual(rotation(vertex=(5, 2), rotation_radians=pi), (-5, -2))        # Anti-clockwise 180 degrees.
        self.assertEqual(rotation(vertex=(-1, -1), rotation_radians=-pi / 2), (1, -1))  # Anti-clockwise 90 degrees.

    def test_angle_from_origin(self):
        self.assertEqual(angle_from_origin(vertex=(0, 0)), 0)                           # Nowhere.
        self.assertEqual(angle_from_origin(vertex=(1, 1)), pi / 4)                      # North West.
        self.assertEqual(angle_from_origin(vertex=(0, 1)), 0)                           # North.
        self.assertEqual(angle_from_origin(vertex=(1, 0)), pi / 2)                      # East.
        self.assertEqual(angle_from_origin(vertex=(0, -1)), pi)                         # South.
        self.assertEqual(angle_from_origin(vertex=(-1, 0)), 3 * pi / 2)                 # West.
        self.assertEqual(angle_from_origin(vertex=(2, -2)), 3 * pi / 4)                 # South East.
        self.assertEqual(angle_from_origin(vertex=(-5, -5)), 5 * pi / 4)                # South West.
        self.assertEqual(angle_from_origin(vertex=(-11, 11)), 7 * pi / 4)               # North West.

    def test_angle(self):
        self.assertEqual(angle((0, 0), (0, 5)), 0)                                      # North
        self.assertEqual(angle((2, 3), (2, 5)), 0)                                      # North
        self.assertEqual(angle((2, 3), (2, 1)), pi)                                     # South
        self.assertEqual(angle((5, 2), (6, 3)), pi / 4)                                 # North East.
        self.assertEqual(angle((5, 6), (3, 6)), 3 * pi / 2)                             # West.
        self.assertEqual(angle((2, 2), (1, 3)), 7 * pi / 4)                             # North West.

    def test_distance(self):
        self.assertEqual(distance((0, 0), (3, 4)), 5.0)
        self.assertEqual(distance((10, 100), (15, 112)), 13.0)


if __name__ == '__main__':
    unittest.main()
