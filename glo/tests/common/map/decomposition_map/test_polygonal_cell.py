import unittest

from mock import MagicMock

from common.map.decomposition_map.polygonal_cell import PolygonalCell
from common.map.position import Position


class TestPolygonalCell(unittest.TestCase):
    top_left = Position(0, 15)
    top_right = Position(15, 15)
    bottom_right = Position(15, 0)
    bottom_left = Position(0, 0)

    position_inside_cell = Position(5, 5)
    position_on_the_edge_of_cell = Position(0, 0)
    position_outside_cell = Position(150, 250)

    cell = None
    polygon_mock = MagicMock()

    def setUp(self):
        self.cell = PolygonalCell([self.top_left, self.top_right, self.bottom_right, self.bottom_left])

    def test_contain_position_inside_cell_call_contains(self):
        self.cell.contain_position_inside_cell(self.position_inside_cell)
        self.cell.polygon = self.polygon_mock
        self.polygon_mock.assert_has_calls(self.polygon_mock.contains)

    def test_contain_position_inside_cell_with_position_inside_return_true(self):
        self.assertTrue(self.cell.contain_position_inside_cell(self.position_inside_cell))

    def test_contain_position_inside_cell_with_position_outside_return_false(self):
        self.assertFalse(self.cell.contain_position_inside_cell(self.position_outside_cell))

    def test_contain_position_inside_cell_with_position_on_the_edge_return_false(self):
        self.assertFalse(self.cell.contain_position_inside_cell(self.position_on_the_edge_of_cell))
