import unittest

from common.map.decomposition_map.decomposition_cell import DecompositionCell
from common.map.decomposition_map.decomposition_cell_factory import CellFactory
from common.map.position import Position


class TestDecompositionCell(unittest.TestCase):
    top_left = Position(0, 15)
    top_right = Position(15, 15)
    bottom_right = Position(15, 0)
    bottom_left = Position(0, 0)

    cell_factory = None

    def setUp(self):
        self.cell_factory = CellFactory()

    def test_when_creating_cell_from_corner_then_return_a_cell(self):
        result = self.cell_factory.create_decomposition_cell_from_corners(self.top_left, self.top_right,
                                                                          self.bottom_right,
                                                                          self.bottom_left)
        self.assertEqual(DecompositionCell, type(result))

    def test_when_creating_cell_from_origin_and_size_then_return_a_cell(self):
        result = self.cell_factory.create_rectangular_decomposition_cell_from_origin_size(self.bottom_left.X,
                                                                                          self.bottom_left.Y,
                                                                                          self.top_right.X,
                                                                                          self.top_right.Y)
        self.assertEqual(DecompositionCell, type(result))
