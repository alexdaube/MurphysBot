import unittest

from mock.mock import Mock, MagicMock
from shapely.geometry import LineString

from common.map.decomposition_map.decomposition_cell import DecompositionCell
from common.map.position import Position


class TestDecompositionCell(unittest.TestCase):
    top_left = Position(0, 15)
    top_right = Position(15, 15)
    bottom_right = Position(15, 0)
    bottom_left = Position(0, 0)

    over_top = Position(7, 20)
    below_bottom = Position(7, -5)
    position_on_right = Position(25, 7)
    position_on_left = Position(-7, 7)

    cell = None
    cell_intersecting = DecompositionCell(top_left, top_right, Position(15, 25), Position(0, 25))
    cell_not_intersecting = DecompositionCell(Position(100, 100), Position(100, 125), Position(90, 125),
                                              Position(90, 100))

    position_center = Position(15.0 / 2, 15.0 / 2)

    position_inside_cell = Position(5, 5)
    position_on_the_edge_of_cell = Position(0, 0)
    position_outside_cell = Position(150, 250)

    def setUp(self):
        self.cell = DecompositionCell(self.top_left, self.top_right, self.bottom_right, self.bottom_left)

    def test_after_initialisation_cell_contain_points(self):
        self.assertEqual(self.bottom_left, self.cell.bottom_left)
        self.assertEqual(self.bottom_right, self.cell.bottom_right)
        self.assertEqual(self.top_left, self.cell.top_left)
        self.assertEqual(self.top_right, self.cell.top_right)

    def test_after_initialisation_cell_passed_through_is_false(self):
        self.assertFalse(self.cell.has_passed_through())

    def test_after_set_has_passed_through_cell_passed_through_is_true(self):
        self.cell.set_has_passed_through()
        self.assertTrue(self.cell.has_passed_through())

    def test_after_reset_passed_through_cell_passed_through_is_false(self):
        self.cell.passed_through = True
        self.cell.reset_pass_through()
        self.assertFalse(self.cell.has_passed_through())

    def test_when_checking_if_position_inside_or_border_call_polygon_contain(self):
        self.cell.polygon = MagicMock()
        self.cell.contain_position_inside_cell_and_borders(self.position_inside_cell)
        assert self.cell.polygon.contains.called, "contains() call not found"

    def test_when_checking_if_position_inside_or_border_call_with_position_on_edge_call_intersects(self):
        self.cell.polygon = MagicMock()
        self.cell.polygon.contains.return_value = False
        self.cell.contain_position_inside_cell_and_borders(self.position_inside_cell)
        assert self.cell.polygon.intersects.called, "intersects() call not found"

    def test_when_checking_if_on_cell_border_call_intersects(self):
        self.cell.polygon = MagicMock()
        self.cell.contain_position_on_cell_borders(self.position_on_the_edge_of_cell)
        assert self.cell.polygon.intersects.called, "intersects() call not found"

    def test_when_checking_if_on_cell_border_call_contains(self):
        self.cell.polygon = MagicMock()
        self.cell.contain_position_on_cell_borders(self.position_on_the_edge_of_cell)
        assert self.cell.polygon.contains.called, "contains() call not found"

    def test_when_checking_if_cell_within_another_cell_call_contains(self):
        self.cell.polygon = MagicMock()
        self.cell.contain_cell(self.cell)
        assert self.cell.polygon.contains.called, "contains() call not found"

    def test_when_getting_cell_center_return_calculated_cell_center(self):
        self.assertEqual(self.position_center, self.cell.get_cell_center())

    def test_calculating_center_of_intersection_2_cell_call_polygon_intersection(self):
        polygon1_mock = Mock()
        self.cell.polygon = polygon1_mock
        self.cell.get_two_cell_intersection_center(self.cell_intersecting)
        polygon1_mock.intersection.assert_called_with(self.cell_intersecting.polygon)

    def test_calculating_center_of_intersection_of_2_cell(self):
        self.assertEqual(Position(7.5, 15), self.cell.get_two_cell_intersection_center(self.cell_intersecting))

    def test_calculating_center_of_intersection_of_2_cell_not_intersection_return_none(self):
        self.assertIsNone(self.cell.get_two_cell_intersection_center(self.cell_not_intersecting))

    def test_is_cell_intersection_line_call_polygon_intersecting(self):
        cell_polygon_mock = Mock()
        cell_polygon_mock.intersects.return_value = False
        position1 = Position(1.0, 1.0)
        position2 = Position(2.0, 2.0)
        self.cell.polygon = cell_polygon_mock

        self.cell.is_cell_intersecting_line(position1, position2)
        assert cell_polygon_mock.intersects.called, "intersects() call not found"

    def test_when_is_intersection_a_line_call_redirect_call_to_polygon_intersection(self):
        self.cell.polygon = MagicMock()
        position1 = Position(1.0, 1.0)
        position2 = Position(2.0, 2.0)
        self.cell.is_intersection_a_line(position1, position2)

        assert self.cell.polygon.intersection.called, "intersection() call not found"

    def test_when_is_intersection_a_line_call_and_intersection_is_a_line_return_true(self):
        self.cell.polygon = MagicMock()
        position1 = Position(1.0, 1.0)
        position2 = Position(2.0, 2.0)
        line = LineString([[position1.X, position1.Y], [position2.X, position2.Y]])
        self.cell.polygon.intersection.return_value = line

        self.assertTrue(self.cell.is_intersection_a_line(position1, position2))

    def test_when_is_intersection_a_line_call_and_intersection_is_not_a_line_return_false(self):
        self.cell.polygon = MagicMock()
        position1 = Position(1.0, 1.0)
        position2 = Position(2.0, 2.0)
        self.cell.polygon.intersection.return_value = position1

        self.assertFalse(self.cell.is_intersection_a_line(position1, position2))

    def test_when_is_line_passing_only_on_border_return_false(self):
        self.assertFalse(self.cell.is_line_passing_only_on_cell_border(self.bottom_left, self.top_right))

    def test_when_is_line_passing_only_on_border_call_polygon_intersection(self):
        self.cell.polygon = MagicMock()
        self.cell.is_line_passing_only_on_cell_border(self.bottom_left, self.top_right)
        assert self.cell.polygon.intersection.called, "intersection() call not found"

    def test_when_is_line_passing_only_on_border_while_not_intersection_found_dosent_call_contains(self):
        self.cell.polygon = MagicMock()
        self.cell.polygon.intersection.return_value = None
        self.cell.is_line_passing_only_on_cell_border(self.bottom_left, self.top_right)

        assert not self.cell.polygon.contains.called, "intersection() called while it shall ne be"

    def test_when_is_line_passing_only_on_border_with_intersection_found(self):
        self.cell.polygon = MagicMock()
        intersection_line = LineString([(self.bottom_left.X, self.bottom_left.Y), (self.top_left.X, self.top_left.Y)])
        self.cell.polygon.intersection.return_value = intersection_line
        self.cell.is_line_passing_only_on_cell_border(self.bottom_left, self.top_right)
        assert self.cell.polygon.contains.called, "contains() call not found"

    def test_when_is_line_passing_only_on_border_with_line_only_on_border_return_true(self):
        self.assertTrue(self.cell.is_line_passing_only_on_cell_border(self.bottom_left, self.top_left))

    def test_when_is_line_passing_only_on_border_with_line_only_not_on_border_return_false(self):
        self.assertFalse(self.cell.is_line_passing_only_on_cell_border(self.bottom_left, self.top_right))

    def test_when_is_line_passing_only_on_border_with_point_intersection_only_on_border_return_false(self):
        self.assertTrue(self.cell.is_line_passing_only_on_cell_border(self.bottom_left, Position(-100, -100)))

    def test_when_is_line_passing_only_on_border_while_not_intersection_found_return_false(self):
        self.cell.polygon = MagicMock()
        self.cell.polygon.intersection.return_value = None
        self.cell.is_line_passing_only_on_cell_border(self.bottom_left, self.top_right)

    def test_when_calculate_distance_between_cells_certers_call_second_cell_get_cell_center(self):
        second_cell_mock = Mock()
        second_cell_mock.get_cell_center.return_value = self.position_outside_cell

        self.cell.calculate_distance_between_cell_center(second_cell_mock)

        assert second_cell_mock.get_cell_center.called, "get_cell_center() call not found"

    def test_when_is_cell_crossing_top_or_down_with_line_crossing_both_return_true(self):
        self.assertTrue(self.cell.is_line_crossing_cell_top_or_bottom(self.over_top, self.below_bottom))

    def test_when_is_cell_crossing_top_or_down_with_line_crossing_only_top_return_true(self):
        self.assertTrue(self.cell.is_line_crossing_cell_top_or_bottom(self.over_top, self.position_inside_cell))

    def test_when_is_cell_crossing_top_or_down_with_line_crossing_only_bottom_return_true(self):
        self.assertTrue(self.cell.is_line_crossing_cell_top_or_bottom(self.below_bottom, self.position_inside_cell))

    def test_when_is_cell_crossing_top_or_down_with_line_crossing_none_return_false(self):
        self.assertFalse(
            self.cell.is_line_crossing_cell_top_or_bottom(self.position_on_left, self.position_inside_cell))

    def test_when_is_line_crossing_cell_right_and_line_crossing_return_true(self):
        self.assertTrue(self.cell.is_line_crossing_cell_right(self.position_on_right, self.position_inside_cell))

    def test_when_is_line_crossing_cell_right_and_line_crossing_return_false(self):
        self.assertFalse(self.cell.is_line_crossing_cell_right(self.over_top, self.position_inside_cell))

    def test_when_is_line_crossing_cell_left_and_line_crossing_return_true(self):
        self.assertTrue(self.cell.is_line_crossing_cell_left(self.position_on_left, self.position_inside_cell))

    def test_when_is_line_crossing_cell_left_and_line_crossing_return_false(self):
        self.assertFalse(self.cell.is_line_crossing_cell_left(self.over_top, self.position_inside_cell))

    def test_when_is_cell_intersecting_cell_call_polygon_intersect(self):
        polygon_mock = MagicMock()
        cell_mock = MagicMock()
        self.cell.polygon = polygon_mock
        self.cell.is_cell_intersecting_cell(cell_mock)
        assert polygon_mock.intersects.called, "intersects() call not found"

    def test_distance_from_position_call_polygon_distance(self):
        polygon_mock = MagicMock()
        self.cell.polygon = polygon_mock
        self.cell.distance_from_position(self.position_outside_cell)
        assert polygon_mock.distance.called, "distance() call not found"
