import unittest

from mock.mock import MagicMock

from common.map.decomposition_map.decomposition_map import DecompositionMap
from common.map.no_path_found import NoPathFoundError
from common.map.out_of_map_boundaries_error import OutOfMapBoundariesError
from common.map.point_of_interest.no_matching_point_of_interest_error import NoMatchingPointOfInterestError
from common.map.point_of_interest.point_of_interest_type import PointOfInterestType
from common.map.position import Position


class TestDecompositionMap(unittest.TestCase):
    map = None
    map_size_x = 100
    map_size_y = 100
    map_origin_x = 0
    map_origin_y = 0
    island_red_circle = MagicMock()
    island_blue_square = MagicMock()
    recharge_station = MagicMock()
    treasure = MagicMock()
    robot_position = MagicMock
    objective_point_of_interest_type = PointOfInterestType.TREASURE
    cell_mock = MagicMock()
    cell_factory_mock = MagicMock()
    a_position_descriptor = [Position(12, 15)]
    cell_splitter_mock = MagicMock()

    def setUp(self):
        self.cell_splitter_mock.split_cell.return_value = list()
        self.cell_factory_mock.create_cell_from_corners.return_value = self.cell_mock
        self.cell_factory_mock.create_rectangular_cell_from_origin_size.return_value = self.cell_mock
        red_circle_island_descriptors = []
        self.island_red_circle.get_position_descriptors.return_value = red_circle_island_descriptors
        self.treasure.get_position_descriptors.return_value = self.a_position_descriptor
        blue_square_island_descriptors = [Position(25, 25), Position(25, 50), Position(50, 50), Position(50, 25)]
        self.island_blue_square.get_position_descriptors.return_value = blue_square_island_descriptors
        self.map = DecompositionMap(self.map_origin_x, self.map_origin_y, self.map_size_x, self.map_size_y,
                                    security_radius=0,
                                    decomposition_cell_factory=self.cell_factory_mock,
                                    decomposition_cell_splitter=self.cell_splitter_mock)

    def test_on_init_call_cell_factory_to_create_cell_filling_world(self):
        self.cell_factory_mock.create_rectangular_decomposition_cell_from_origin_size.assert_called_with(
            self.map_origin_x, self.map_origin_y, self.map_size_x, self.map_size_y)

    def test_no_point_of_interest_in_map_when_find_path_raise_no_matching_point_of_interest_error(self):
        self.assertRaises(NoMatchingPointOfInterestError, self.map.calculate_dijkstra_path, self.robot_position,
                          self.objective_point_of_interest_type)

    def test_no_matching_point_of_interest_in_map_when_find_path_raise_no_matching_point_of_interest_error(self):
        self.recharge_station.has_point_of_interest_type.return_value = False
        self.map.add_recharge_station(self.recharge_station)

        self.assertRaises(NoMatchingPointOfInterestError, self.map.calculate_dijkstra_path, self.robot_position,
                          self.objective_point_of_interest_type)

    def test_point_of_interest_in_map_when_find_path_then_check_each_if_of_objective_point_of_interest_type(self):
        self.recharge_station.has_point_of_interest_type.return_value = False
        self.island_blue_square.has_point_of_interest_type.return_value = False
        self.map.add_recharge_station(self.recharge_station)
        self.map.add_island(self.island_blue_square)

        self.assertRaises(NoMatchingPointOfInterestError, self.map.calculate_dijkstra_path, self.robot_position,
                          self.objective_point_of_interest_type)

        self.recharge_station.has_point_of_interest_type.assert_called_with(self.objective_point_of_interest_type)
        self.island_blue_square.has_point_of_interest_type.assert_called_with(self.objective_point_of_interest_type)

    def test_point_of_interest_in_map_when_find_path_then_get_position_descriptor_of_objective(self):
        self.treasure.has_point_of_interest_type.return_value = True
        self.map.add_treasure(self.treasure)
        self.cell_mock.contain_position_inside_cell_and_borders.return_value = True
        self.cell_mock.has_passed_through.return_value = False

        try:
            self.map.calculate_dijkstra_path(self.robot_position, self.objective_point_of_interest_type)
        except NoPathFoundError:
            self.treasure.assert_has_calls(self.treasure.get_position_descriptors)

    def test_point_of_interest_in_map_when_find_path_then_retrieve_objective_descriptors(self):
        self.treasure.has_point_of_interest_type.return_value = True
        self.map.add_treasure(self.treasure)
        self.cell_mock.contain_position_inside_cell_and_borders.return_value = True
        self.cell_mock.has_passed_through.return_value = False

        try:
            self.map.calculate_dijkstra_path(self.robot_position, self.objective_point_of_interest_type)
        except NoPathFoundError:
            self.treasure.assert_has_calls(self.treasure.get_position_descriptors)

    def test_point_of_interest_in_map_when_find_path_then_check_each_cell_if_contain_objective(self):
        self.treasure.has_point_of_interest_type.return_value = True
        self.map.add_treasure(self.treasure)
        self.cell_mock.contain_position_inside_cell_and_borders.return_value = True
        self.cell_mock.has_passed_through.return_value = False

        try:
            self.map.calculate_dijkstra_path(self.robot_position, self.objective_point_of_interest_type)
        except NoPathFoundError:
            self.cell_mock.assert_has_calls(self.cell_mock.is_cell_intersecting_cell)

    def test_during_add_island_call_island_get_position_descriptors(self):
        self.map.add_island(self.island_blue_square)
        self.island_blue_square.assert_has_calls(self.island_blue_square.get_position_descriptors)

    def test_during_add_island_call_cell_splitter(self):
        self.map.add_island(self.island_blue_square)
        self.cell_splitter_mock.assert_has_calls(self.cell_splitter_mock.split_cell)

    def test_during_find_path_call_cell_reset_pass_through(self):
        self.treasure.has_point_of_interest_type.return_value = True
        self.map.add_treasure(self.treasure)
        self.cell_mock.contain_position_inside_cell_and_borders.return_value = True
        self.cell_mock.has_passed_through.return_value = False

        try:
            self.map.calculate_dijkstra_path(self.robot_position, self.objective_point_of_interest_type)
        except NoPathFoundError:
            self.cell_mock.assert_has_calls(self.cell_mock.reset_pass_through)

    def test_during_find_path_call_cell_contain_position_inside_cell_and_borders_with_robot_position(self):
        self.treasure.has_point_of_interest_type.return_value = True
        self.map.add_treasure(self.treasure)
        self.cell_mock.contain_position_inside_cell_and_borders.return_value = True
        self.cell_mock.has_passed_through.return_value = False

        try:
            self.map.calculate_dijkstra_path(self.robot_position, self.objective_point_of_interest_type)
        except NoPathFoundError:
            self.cell_mock.assert_has_calls(self.cell_mock.contain_position_inside_cell_and_borders)

    def test_during_find_path_robot_out_of_cells_call_distance_from_position(self):
        self.treasure.has_point_of_interest_type.return_value = True
        self.map.add_treasure(self.treasure)
        self.cell_mock.contain_position_inside_cell_and_borders.return_value = False
        self.cell_mock.has_passed_through.return_value = False

        try:
            self.map.calculate_dijkstra_path(self.robot_position, self.objective_point_of_interest_type)
        except NoPathFoundError:
            self.cell_mock.assert_has_calls(self.cell_mock.distance_from_position)

    def test_get_objective_cells_with_objective_not_found_in_map_cells(self):
        self.treasure.has_point_of_interest_type.return_value = True
        self.map.add_treasure(self.treasure)
        self.cell_mock.is_cell_intersecting_cell.return_value = False

        try:
            self.assertRaises(OutOfMapBoundariesError, self.map.calculate_dijkstra_path, self.robot_position,
                              self.objective_point_of_interest_type)
        except NoPathFoundError:
            pass

    def test_get_objective_cells_with_origin_not_found_in_map_cells(self):
        self.treasure.has_point_of_interest_type.return_value = True
        self.map.add_treasure(self.treasure)

        def mock_contain_position_inside_cell_and_borders(position):
            if position is self.robot_position:
                return False
            else:
                return True

        self.cell_mock.contain_position_inside_cell_and_borders = mock_contain_position_inside_cell_and_borders
        try:
            self.assertRaises(OutOfMapBoundariesError, self.map.calculate_dijkstra_path, self.robot_position,
                              self.objective_point_of_interest_type)
        except NoPathFoundError:
            pass
