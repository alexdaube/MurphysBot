import unittest

from mock import Mock

from common.map.point_of_interest.island.square_island import SquareIsland
from common.map.point_of_interest.point_of_interest_type import PointOfInterestType


class TestSquareIsland(unittest.TestCase):
    island = None
    position = Mock()
    matching_form = PointOfInterestType.SQUARE_ISLAND
    matching_color = PointOfInterestType.BLUE_COLOR
    different_form = PointOfInterestType.CIRCLE_ISLAND
    different_color = PointOfInterestType.YELLOW_COLOR
    security_zone = 70

    def setUp(self):
        self.island = SquareIsland(self.matching_color, self.position, self.security_zone)

    def test_has_point_of_interest_type_with_matching_color_return_true(self):
        self.assertTrue(self.island.has_point_of_interest_type(self.matching_color))

    def test_has_point_of_interest_type_with_matching_formtype_return_true(self):
        self.assertTrue(self.island.has_point_of_interest_type(self.matching_form))

    def test_has_point_of_interest_type_with_different_color_return_false(self):
        self.assertFalse(self.island.has_point_of_interest_type(self.different_color))

    def test_has_point_of_interest_type_with_different_formtype_return_false(self):
        self.assertFalse(self.island.has_point_of_interest_type(self.different_form))
