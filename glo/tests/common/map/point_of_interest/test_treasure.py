import unittest

from mock.mock import Mock

from common.map.point_of_interest.point_of_interest_type import PointOfInterestType
from common.map.point_of_interest.treasure import Treasure


class TestBaseStation(unittest.TestCase):
    treasure = None
    treasure_position = Mock()

    def setUp(self):
        self.treasure = Treasure(self.treasure_position)

    def test_get_position_return_position(self):
        self.assertEqual(self.treasure_position, self.treasure.get_position())

    def test_has_point_of_interest_type_with_treasure_type_return_true(self):
        self.assertTrue(self.treasure.has_point_of_interest_type(PointOfInterestType.TREASURE))

    def test_has_point_of_interest_type_with_other_type_than_treasure_type_return_false(self):
        self.assertFalse(self.treasure.has_point_of_interest_type(PointOfInterestType.YELLOW_COLOR))
