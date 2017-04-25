from common.map.decomposition_map.decomposition_cell_factory import CellFactory
from common.map.position import Position


class DecompositionCellSplitter:
    cell_factory = None

    def __init__(self, decomposition_cell_factory=CellFactory()):
        self.cell_factory = decomposition_cell_factory

    def split_cell(self, cell, left, right):
        new_cells = list()

        if not cell.is_intersection_a_line(left, right) \
                or cell.is_line_passing_only_on_cell_border(left, right):
            # edge does not pass through cell
            pass
        elif cell.contain_position_inside_cell(left) and cell.contain_position_inside_cell(right):
            self.__all_side_cell_splitting(new_cells, cell, left, right)
        else:
            left_crossing, right_crossing = self.__bound_line_to_cell(cell, left, right)
            if left_crossing.X is right_crossing.X:
                self.__left_right_cell_splitting(new_cells, cell, left_crossing, right_crossing)
            elif cell.contain_position_inside_cell(left_crossing) \
                    and not cell.contain_position_inside_cell(right_crossing):
                if cell.is_line_crossing_cell_top_or_bottom(left_crossing, right_crossing) \
                        and not cell.is_line_crossing_cell_right(left_crossing, right_crossing):
                    self.__all_side_cell_splitting(new_cells, cell, left_crossing, right_crossing)
                else:
                    self.__left_up_down_cell_splitting(new_cells, cell, left_crossing, right_crossing)
            elif cell.contain_position_inside_cell(right_crossing) \
                    and not cell.contain_position_inside_cell(left_crossing):
                if cell.is_line_crossing_cell_top_or_bottom(left_crossing, right_crossing) \
                        and not cell.is_line_crossing_cell_left(left_crossing, right_crossing):
                    self.__all_side_cell_splitting(new_cells, cell, left_crossing, right_crossing)
                else:
                    self.__right_up_down_cell_splitting(new_cells, cell, left_crossing, right_crossing)
            else:
                if cell.is_line_crossing_cell_right(left_crossing, right_crossing) \
                        and cell.is_line_crossing_cell_left(left_crossing, right_crossing):
                    self.__up_down_cell_splitting(new_cells, cell, left_crossing, right_crossing)
                elif cell.is_line_crossing_cell_top_or_bottom(left_crossing, right_crossing):
                    if cell.is_line_crossing_cell_left(left_crossing, right_crossing):
                        self.__right_up_down_cell_splitting(new_cells, cell, left_crossing, right_crossing)
                    elif cell.is_line_crossing_cell_right(left_crossing, right_crossing):
                        self.__left_up_down_cell_splitting(new_cells, cell, left_crossing, right_crossing)
                    else:
                        self.__all_side_cell_splitting(new_cells, cell, left_crossing, right_crossing)
        return new_cells

    def __bound_line_to_cell(self, cell, left, right):
        position1, position2 = cell.get_intersection_line(left, right)
        if position1.X >= position2.X:
            return position2, position1
        else:
            return position1, position2

    def __all_side_cell_splitting(self, new_cells, cell, left, right):
        top_ratio = float(cell.top_left.Y - cell.top_right.Y) / float(cell.top_left.X - cell.top_right.X)
        bottom_ratio = float(cell.bottom_left.Y - cell.bottom_right.Y) / float(cell.bottom_left.X - cell.bottom_right.X)

        left_top_y = cell.top_left.Y + top_ratio * (left.X - cell.top_left.X)
        right_top_y = cell.top_left.Y + top_ratio * (right.X - cell.top_left.X)
        left_bottom_y = cell.bottom_left.Y + bottom_ratio * (left.X - cell.bottom_left.X)
        right_bottom_y = cell.bottom_left.Y + bottom_ratio * (right.X - cell.bottom_left.X)

        left_top_position = Position(left.X, left_top_y)
        right_top_position = Position(right.X, right_top_y)
        left_bottom_position = Position(left.X, left_bottom_y)
        right_bottom_position = Position(right.X, right_bottom_y)

        left_cell = self.cell_factory.create_decomposition_cell_from_corners(cell.top_left, left_top_position,
                                                                             left_bottom_position,
                                                                             cell.bottom_left)
        top_cell = self.cell_factory.create_decomposition_cell_from_corners(left_top_position, right_top_position,
                                                                            right,
                                                                            left)
        bottom_cell = self.cell_factory.create_decomposition_cell_from_corners(left, right, right_bottom_position,
                                                                               left_bottom_position)
        right_cell = self.cell_factory.create_decomposition_cell_from_corners(right_top_position, cell.top_right,
                                                                              cell.bottom_right,
                                                                              right_bottom_position)

        new_cells.append(left_cell)
        new_cells.append(top_cell)
        new_cells.append(bottom_cell)
        new_cells.append(right_cell)

    def __left_up_down_cell_splitting(self, new_cells, cell, left, right):
        top_ratio = float(cell.top_left.Y - cell.top_right.Y) / float(cell.top_left.X - cell.top_right.X)
        bottom_ratio = float(cell.bottom_left.Y - cell.bottom_right.Y) / float(
            cell.bottom_left.X - cell.bottom_right.X)

        top_y = cell.top_left.Y + top_ratio * (left.X - cell.top_left.X)
        bottom_y = cell.bottom_left.Y + bottom_ratio * (left.X - cell.bottom_left.X)

        middle_top_position = Position(left.X, top_y)
        middle_bottom_position = Position(left.X, bottom_y)

        left_cell = self.cell_factory.create_decomposition_cell_from_corners(cell.top_left, middle_top_position,
                                                                             middle_bottom_position,
                                                                             cell.bottom_left)
        top_cell = self.cell_factory.create_decomposition_cell_from_corners(middle_top_position, cell.top_right,
                                                                            right, left)
        bottom_cell = self.cell_factory.create_decomposition_cell_from_corners(left, right,
                                                                               cell.bottom_right,
                                                                               middle_bottom_position)

        new_cells.append(left_cell)
        new_cells.append(top_cell)
        new_cells.append(bottom_cell)

    def __right_up_down_cell_splitting(self, new_cells, cell, left, right):
        top_ratio = float(cell.top_left.Y - cell.top_right.Y) / float(cell.top_left.X - cell.top_right.X)
        bottom_ratio = float(cell.bottom_left.Y - cell.bottom_right.Y) / float(
            cell.bottom_left.X - cell.bottom_right.X)
        top_y = cell.top_left.Y + top_ratio * (right.X - cell.top_left.X)
        bottom_y = cell.bottom_left.Y + bottom_ratio * (right.X - cell.bottom_left.X)

        middle_top_position = Position(right.X, top_y)
        middle_bottom_position = Position(right.X, bottom_y)

        top_cell = self.cell_factory.create_decomposition_cell_from_corners(cell.top_left, middle_top_position, right,
                                                                            left)
        bottom_cell = self.cell_factory.create_decomposition_cell_from_corners(left, right,
                                                                               middle_bottom_position,
                                                                               cell.bottom_left)
        right_cell = self.cell_factory.create_decomposition_cell_from_corners(middle_top_position, cell.top_right,
                                                                              cell.bottom_right,
                                                                              middle_bottom_position)

        new_cells.append(top_cell)
        new_cells.append(bottom_cell)
        new_cells.append(right_cell)

    def __left_right_cell_splitting(self, new_cells, cell, left, right):
        top_ratio = float(cell.top_left.Y - cell.top_right.Y) / float(cell.top_left.X - cell.top_right.X)
        bottom_ratio = float(cell.bottom_left.Y - cell.bottom_right.Y) / float(
            cell.bottom_left.X - cell.bottom_right.X)

        top_y = cell.top_left.Y + top_ratio * (left.X - cell.top_left.X)
        bottom_y = cell.bottom_left.Y + bottom_ratio * (left.X - cell.bottom_left.X)

        middle_top_position = Position(left.X, top_y)
        middle_bottom_position = Position(left.X, bottom_y)

        left_cell = self.cell_factory.create_decomposition_cell_from_corners(cell.top_left, middle_top_position,
                                                                             middle_bottom_position, cell.bottom_left)
        right_cell = self.cell_factory.create_decomposition_cell_from_corners(middle_top_position, cell.top_right,
                                                                              cell.bottom_right, middle_bottom_position)

        new_cells.append(left_cell)
        new_cells.append(right_cell)

    def __up_down_cell_splitting(self, new_cells, cell, left, right):
        top_cell = self.cell_factory.create_decomposition_cell_from_corners(cell.top_left, cell.top_right, right,
                                                                            left)
        bottom_cell = self.cell_factory.create_decomposition_cell_from_corners(left, right,
                                                                               cell.bottom_right, cell.bottom_left)

        new_cells.append(top_cell)
        new_cells.append(bottom_cell)
