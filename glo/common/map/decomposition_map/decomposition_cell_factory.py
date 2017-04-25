from common.map.decomposition_map.decomposition_cell import DecompositionCell
from common.map.decomposition_map.polygonal_cell import PolygonalCell

from common.map.position import Position


class CellFactory(object):
    def create_decomposition_cell_from_corners(self, top_left, top_right, bottom_right, bottom_left):
        return DecompositionCell(top_left, top_right, bottom_right, bottom_left)

    def create_rectangular_decomposition_cell_from_origin_size(self, origin_x, origin_y, size_x, size_y):
        bottom_left = Position(origin_x, origin_y)
        top_left = Position(origin_x, origin_y + size_y)
        top_right = Position(origin_x + size_x, origin_y + size_y)
        bottom_right = Position(origin_x + size_x, origin_y)
        return DecompositionCell(top_left, top_right, bottom_right, bottom_left)

    def create_polygonal_cell_from_corner_list(self, corner_list):
        return PolygonalCell(corner_list)
