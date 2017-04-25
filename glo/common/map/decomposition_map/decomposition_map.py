import heapq
from math import sqrt

import common.constants as constants
from common.map.decomposition_map.decomposition_cell_factory import CellFactory
from common.map.decomposition_map.decomposition_cell_splitter import DecompositionCellSplitter
from common.map.dijkstra_pathfinding_implementor import DijkstraPathFindingImplementor
from common.map.map import Map
from common.map.no_path_found import NoPathFoundError
from common.map.out_of_map_boundaries_error import OutOfMapBoundariesError
from common.map.point_of_interest.no_matching_point_of_interest_error import NoMatchingPointOfInterestError


class DecompositionMap(Map, DijkstraPathFindingImplementor):
    origin_x = None
    origin_y = None
    size_x = None
    size_y = None
    point_of_interest_list = list()
    cell_list = list()
    security_radius = None
    cell_factory = None
    cell_splitter = None

    def __init__(self, origin_x, origin_y, size_x=constants.TABLE_WIDTH, size_y=constants.TABLE_HEIGHT,
                 security_radius=constants.BORDER_SECURITY_RADIUS,
                 decomposition_cell_factory=CellFactory(),
                 decomposition_cell_splitter=DecompositionCellSplitter(),
                 base_horizontal_cell_count=1,
                 base_vertical_cell_count=1):
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.size_x = size_x
        self.size_y = size_y
        self.security_radius = security_radius
        self.point_of_interest_list = list()
        self.cell_list = list()
        self.cell_factory = decomposition_cell_factory
        self.cell_splitter = decomposition_cell_splitter
        self.__init_base_cells(base_horizontal_cell_count, base_vertical_cell_count)

    def __init_base_cells(self, base_horizontal_cell_count, base_vertical_cell_count):
        assert base_horizontal_cell_count >= 1
        assert base_vertical_cell_count >= 1
        assert (self.size_y - 2 * self.security_radius) % base_horizontal_cell_count == 0
        assert (self.size_x - 2 * self.security_radius) % base_vertical_cell_count == 0
        base_cell_height = (self.size_y - 2 * self.security_radius) / base_horizontal_cell_count
        base_cell_width = (self.size_x - 2 * self.security_radius) / base_vertical_cell_count
        for i in range(0, base_horizontal_cell_count):
            for j in range(0, base_vertical_cell_count):
                cell = self.cell_factory.create_rectangular_decomposition_cell_from_origin_size(
                    self.origin_x + j * base_cell_width + self.security_radius,
                    self.origin_y + i * base_cell_height + self.security_radius,
                    base_cell_width,
                    base_cell_height)
                self.cell_list.append(cell)

    def __add_point_of_interest__(self, point_of_interest):
        self.point_of_interest_list.append(point_of_interest)

    def get_cell_list(self):
        return self.cell_list

    def add_treasure(self, treasure):
        self.__add_point_of_interest__(treasure)

    def add_recharge_station(self, recharge_station):
        self.__add_point_of_interest__(recharge_station)

    def add_island(self, island):
        self.__add_point_of_interest__(island)
        self.__add_obstacle(island)

    def __add_obstacle(self, island):
        island_descriptors = island.get_position_descriptors()
        previous_position = island_descriptors[-1]
        for current_position in island_descriptors:
            self.__intersect_in_map(previous_position, current_position)
            previous_position = current_position
        self.__remove_cell_contained_by_obstacle(island)

    def __remove_cell_contained_by_obstacle(self, obstacle):
        obstacle_descriptor = obstacle.get_position_descriptors()
        obstacle_cell = self.cell_factory.create_polygonal_cell_from_corner_list(obstacle_descriptor)
        new_cell_list = list()
        for cell in self.cell_list:
            if not obstacle_cell.contain_position_inside_cell(cell.get_cell_center()):
                new_cell_list.append(cell)
        self.cell_list = new_cell_list

    def __intersect_in_map(self, previous_position, current_position):
        left = previous_position
        right = current_position
        if previous_position.X > current_position.X:
            left = current_position
            right = previous_position

        intersected_cells = list()
        for cell in self.cell_list:
            if cell.is_cell_intersecting_line(left, right):
                intersected_cells.append(cell)

        for cell in intersected_cells:
            new_cells = self.cell_splitter.split_cell(cell, left, right)
            if len(new_cells) > 0:
                self.__remove_original_cell_and_update_cell_list_with_new_cells(new_cells, cell)

    def __remove_original_cell_and_update_cell_list_with_new_cells(self, new_cells, original_cell):
        self.cell_list.remove(original_cell)
        self.cell_list += [cell for cell in new_cells if cell not in self.cell_list]

    def calculate_dijkstra_path(self, robot_position, objective_type):
        potential_objective = self.__get_objective(objective_type)
        potential_objectives_cells = self.__get_objective_cells(potential_objective)
        origin_cell = self.__get_origin_cell(robot_position)
        self.__reset_cell_pass_through()

        path_through_cells = self.__solve_path(robot_position, origin_cell, potential_objectives_cells)

        way_points_list = self.__path_to_waypoints(path_through_cells)
        objective_position = self.__objective_position_in_path(potential_objective, path_through_cells)
        return way_points_list, objective_position

    def __get_objective(self, objective_type):
        objective = list()
        for point_of_interest in self.point_of_interest_list:
            if point_of_interest.has_point_of_interest_type(objective_type):
                objective.append(point_of_interest)
        if len(objective) is 0:
            raise NoMatchingPointOfInterestError("No matching objective found!")
        return objective

    def __get_objective_cells(self, objectives):
        objective_cells = list()
        for objective in objectives:
            objective_descriptor = objective.get_position_descriptors()
            objective_cell = self.cell_factory.create_polygonal_cell_from_corner_list(objective_descriptor)
            for cell in self.cell_list:
                if cell not in objective_cells and cell.is_cell_intersecting_cell(objective_cell):
                    objective_cells.append(cell)
        if len(objective_cells) is 0:
            raise OutOfMapBoundariesError("No cell containing objective found within map boundaries")
        return objective_cells

    def __get_origin_cell(self, position):
        for cell in self.cell_list:
            if cell.contain_position_inside_cell_and_borders(position):
                return cell
        distance = sqrt(self.size_x ** 2 + self.size_y ** 2)
        closest_cell = None
        for cell in self.cell_list:
            distance_between_cell_position = cell.distance_from_position(position)
            if distance > distance_between_cell_position:
                distance = distance_between_cell_position
                closest_cell = cell
        if closest_cell is None:
            raise OutOfMapBoundariesError("No cell containing origin position found within map boundaries")
        else:
            return closest_cell

    def __reset_cell_pass_through(self):
        for cell in self.cell_list:
            cell.reset_pass_through()

    def __solve_path(self, origin_position, origin_cell, potential_objectives_cells):
        count = 1
        paths_heap = []
        path = list()
        heapq.heappush(paths_heap, (0, count, origin_position, [origin_cell]))
        path_found = False
        while path_found is False and len(paths_heap) > 0:
            (current_path_length, _, current_position, current_path) = heapq.heappop(paths_heap)
            current_cell = current_path[-1]
            if not current_cell.has_passed_through():
                current_cell.set_has_passed_through()
                if current_cell in potential_objectives_cells:
                    path_found = True
                    path = current_path
                else:
                    for cell in self.cell_list:
                        if current_cell is not cell and cell.get_two_cell_intersection_center(
                                current_cell) is not None and not cell.has_passed_through():
                            count += 1
                            next_path = []
                            next_path += current_path
                            next_path.append(cell)
                            cell_intersection_center = current_cell.get_two_cell_intersection_center(cell)
                            next_move_length = current_position.calculate_distance(cell_intersection_center)
                            next_path_length = next_move_length + current_path_length
                            heapq.heappush(paths_heap, (next_path_length, count, cell_intersection_center, next_path))
        if len(path) is 0:
            raise NoPathFoundError()
        return path

    def __path_to_waypoints(self, path_through_cells):
        waypoints = list()
        previous_cell = None
        for current_cell in path_through_cells:
            if previous_cell is None:
                pass
            else:
                intersection_center = current_cell.get_two_cell_intersection_center(previous_cell)
                if len(waypoints) > 0 and waypoints[-1].X is intersection_center.X:
                    waypoints.append(current_cell.get_cell_center())
                waypoints.append(intersection_center)
            previous_cell = current_cell
        return waypoints

    def __objective_position_in_path(self, potential_objective, path_through_cells):
        last_cell_in_path = path_through_cells[-1]
        for objective in potential_objective:
            objective_descriptor = objective.get_position_descriptors()
            objective_cell = self.cell_factory.create_decomposition_cell_from_corners(objective_descriptor[0],
                                                                                      objective_descriptor[1],
                                                                                      objective_descriptor[2],
                                                                                      objective_descriptor[3])
            if last_cell_in_path.is_cell_intersecting_cell(objective_cell):
                return objective.get_position()
