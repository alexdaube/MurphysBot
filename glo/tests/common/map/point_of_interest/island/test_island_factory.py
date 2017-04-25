import unittest

from mock.mock import Mock

from common.map.point_of_interest.island.circle_island import CircleIsland
from common.map.point_of_interest.island.island_factory import IslandFactory
from common.map.point_of_interest.island.pentagon_island import PentagonIsland
from common.map.point_of_interest.island.square_island import SquareIsland
from common.map.point_of_interest.island.triangle_island import TriangleIsland
from common.map.point_of_interest.island.undefine_island_type_error import UndefineIslandTypeError
from common.map.point_of_interest.point_of_interest_type import PointOfInterestType


class TestIslandFactory(unittest.TestCase):
    island_factory = None

    def setUp(self):
        self.island_factory = IslandFactory()

    def test_create_island_with_circle_island_then_return_circle_island(self):
        result = self.island_factory.create_island(PointOfInterestType.CIRCLE_ISLAND, Mock(), Mock())
        self.assertEqual(CircleIsland, type(result))

    def test_create_island_with_triangle_island_then_return_triangle_island(self):
        result = self.island_factory.create_island(PointOfInterestType.TRIANGLE_ISLAND, Mock(), Mock())
        self.assertEqual(TriangleIsland, type(result))

    def test_create_island_with_square_island_then_return_square_island(self):
        result = self.island_factory.create_island(PointOfInterestType.SQUARE_ISLAND, Mock(), Mock())
        self.assertEqual(SquareIsland, type(result))

    def test_create_island_with_pentagon_island_then_return_pentagon_island(self):
        result = self.island_factory.create_island(PointOfInterestType.PENTAGON_ISLAND, Mock(), Mock())
        self.assertEqual(PentagonIsland, type(result))

    def test_create_island_with_unknow_type_raise_undefine_island_type_error(self):
        self.assertRaises(UndefineIslandTypeError, self.island_factory.create_island, Mock(), Mock(), Mock())
