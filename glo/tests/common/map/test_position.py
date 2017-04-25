import unittest

from common.map.position import Position


class TestPosition(unittest.TestCase):
    position1 = Position(0, 0)
    position2 = Position(5, 0)
    position3 = Position(0, -5)
    position4 = Position(-5, 5)
    position5 = Position(-5, 0)
    position6 = Position(5, 5)
    position7 = Position(-5, -5)
    position8 = Position(5, -5)
    distance1 = 5

    def test_calculate_distance_between_two_position_return_right_result(self):
        self.assertEqual(self.distance1, self.position1.calculate_distance(self.position2))

    def test_when_position_equal_then_return_true(self):
        self.assertTrue(self.position1.__eq__(self.position1))

    def test_when_position_different_in_X_then_return_false(self):
        self.assertFalse(self.position1.__eq__(self.position2))

    def test_when_position_different_in_Y_then_return_false(self):
        self.assertFalse(self.position1.__eq__(self.position3))

    def test_when_position_different_in_X_and_Y_then_return_false(self):
        self.assertFalse(self.position1.__eq__(self.position4))

    def test_angle(self):
        self.assertEqual(0, self.position1.calculate_angle(self.position1))
        self.assertEqual(90, self.position1.calculate_angle(self.position2))
        self.assertEqual(-90, self.position1.calculate_angle(self.position5))
        self.assertEqual(180, self.position1.calculate_angle(self.position3))
        self.assertEqual(-45, self.position1.calculate_angle(self.position4))
        self.assertEqual(45, self.position1.calculate_angle(self.position6))
        self.assertEqual(-135, self.position1.calculate_angle(self.position7))
        self.assertEqual(135, self.position1.calculate_angle(self.position8))
