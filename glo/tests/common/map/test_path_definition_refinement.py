import unittest

import common.map.path_definition_refinement as path_definition_refinement
from common.map.position import Position


class TestPathDefinitionRefinement(unittest.TestCase):
    SMALL_MAX_DISTANCE_BETWEEN_WAYPOINTS = 100
    MAX_DISTANCE_BETWEEN_WAYPOINTS = 380
    VERY_HIGH_MAX_DISTANCE_BETWEEN_WAYPOINTS = 100000
    EMPTY_LENGTH = 0
    HIGH_THRESHOLD = 0.5

    way_point_3 = Position(0, 0)
    way_point_4 = Position(0, -500)

    way_point_5 = Position(0, 0)
    way_point_6 = Position(0.000001, -500)

    def test_path_empty(self):
        way_points = list()
        result = path_definition_refinement.generate_way_point_list_with_max_distance(way_points,
                                                                                      self.MAX_DISTANCE_BETWEEN_WAYPOINTS)
        self.assertEqual(self.EMPTY_LENGTH, len(result))

    def test_path_with_waypoint_distance_smaller_than_max_distance(self):
        way_points = list()
        way_point_1 = Position(0, 0)
        way_point_2 = Position(500, 500)

        way_points.append(way_point_1)
        way_points.append(way_point_2)
        result = path_definition_refinement.generate_way_point_list_with_max_distance(way_points,
                                                                                      self.VERY_HIGH_MAX_DISTANCE_BETWEEN_WAYPOINTS)
        self.assertEqual(2, len(result))
        self.assertEqual(way_point_1, result[0])
        self.assertEqual(way_point_2, result[1])

    def test_path_with_waypoint_distance_higher_than_max_distance(self):
        way_points = list()
        way_point_1 = Position(0, 0)
        way_point_2 = Position(500, 500)
        intermediary_way_point = Position(250, 250)
        way_points.append(way_point_1)
        way_points.append(way_point_2)
        result = path_definition_refinement.generate_way_point_list_with_max_distance(way_points,
                                                                                      self.MAX_DISTANCE_BETWEEN_WAYPOINTS)
        self.assertEqual(3, len(result))
        self.assertEqual(way_point_1, result[0])
        self.assertEqual(intermediary_way_point, result[1])
        self.assertEqual(way_point_2, result[2])

    def test_path_with_waypoint_distance_higher_than_max_distance_small_distance(self):
        way_points = list()
        way_point_1 = Position(0, 0)
        way_point_2 = Position(500, 500)

        # sqrt(500^2 + 500^2) ~= 707.10678118654752440084436210484903928483593768847404
        # => 8 splits as default no_split_threshold is used

        distance = 500.0 / 7
        intermediate_1 = Position(distance, distance)
        intermediate_2 = Position(distance * 2, distance * 2)
        intermediate_3 = Position(distance * 3, distance * 3)
        intermediate_4 = Position(distance * 4, distance * 4)
        intermediate_5 = Position(distance * 5, distance * 5)
        intermediate_6 = Position(distance * 6, distance * 6)
        intermediate_7 = Position(distance * 7, distance * 7)

        way_points.append(way_point_1)
        way_points.append(way_point_2)
        result = path_definition_refinement.generate_way_point_list_with_max_distance(way_points,
                                                                                      self.SMALL_MAX_DISTANCE_BETWEEN_WAYPOINTS)
        self.assertEqual(9, len(result))
        self.assertEqual(way_point_1, result[0])
        self.assertEqual(intermediate_1, result[1])
        self.assertEqual(intermediate_2, result[2])
        self.assertEqual(intermediate_3, result[3])
        self.assertEqual(intermediate_4, result[4])
        self.assertEqual(intermediate_5, result[5])
        self.assertEqual(intermediate_6, result[6])
        self.assertEqual(intermediate_7, result[7])
        self.assertEqual(way_point_2, result[8])

    def test_path_with_waypoint_distance_higher_than_max_distance_small_distance_with_y_origin(self):
        way_points = list()
        way_point_1 = Position(0, 500)
        way_point_2 = Position(500, 0)

        # sqrt(500^2 + 500^2) ~= 707.10678118654752440084436210484903928483593768847404
        # => 8 splits as default no_split_threshold is used

        distance = 500.0 / 8
        intermediate_1 = Position(distance, distance * 7)
        intermediate_2 = Position(distance * 2, distance * 6)
        intermediate_3 = Position(distance * 3, distance * 5)
        intermediate_4 = Position(distance * 4, distance * 4)
        intermediate_5 = Position(distance * 5, distance * 3)
        intermediate_6 = Position(distance * 6, distance * 2)
        intermediate_7 = Position(distance * 7, distance)

        way_points.append(way_point_1)
        way_points.append(way_point_2)
        result = path_definition_refinement.generate_way_point_list_with_max_distance(way_points,
                                                                                      self.SMALL_MAX_DISTANCE_BETWEEN_WAYPOINTS)
        self.assertEqual(9, len(result))
        self.assertEqual(way_point_1, result[0])
        self.assertEqual(intermediate_1, result[1])
        self.assertEqual(intermediate_2, result[2])
        self.assertEqual(intermediate_3, result[3])
        self.assertEqual(intermediate_4, result[4])
        self.assertEqual(intermediate_5, result[5])
        self.assertEqual(intermediate_6, result[6])
        self.assertEqual(intermediate_7, result[7])
        self.assertEqual(way_point_2, result[8])

    def test_path_with_waypoint_distance_higher_than_max_distance_small_distance(self):
        way_points = list()
        way_point_1 = Position(0, 0)
        way_point_2 = Position(500, 500)

        # sqrt(500^2 + 500^2) ~= 707.10678118654752440084436210484903928483593768847404
        # => 7 splits as no_split_threshold = HIGH_THRESHOLD is used

        distance = 500.0 / 7
        intermediate_1 = Position(distance, distance)
        intermediate_2 = Position(distance * 2, distance * 2)
        intermediate_3 = Position(distance * 3, distance * 3)
        intermediate_4 = Position(distance * 4, distance * 4)
        intermediate_5 = Position(distance * 5, distance * 5)
        intermediate_6 = Position(distance * 6, distance * 6)

        way_points.append(way_point_1)
        way_points.append(way_point_2)
        result = path_definition_refinement.generate_way_point_list_with_max_distance(way_points,
                                                                                      self.SMALL_MAX_DISTANCE_BETWEEN_WAYPOINTS,
                                                                                      self.HIGH_THRESHOLD)
        self.assertEqual(8, len(result))
        self.assertEqual(way_point_1, result[0])
        self.assertEqual(intermediate_1, result[1])
        self.assertEqual(intermediate_2, result[2])
        self.assertEqual(intermediate_3, result[3])
        self.assertEqual(intermediate_4, result[4])
        self.assertEqual(intermediate_5, result[5])
        self.assertEqual(intermediate_6, result[6])
        self.assertEqual(way_point_2, result[7])

    def test_path_with_waypoint_distance_higher_than_max_distance_negative_slope(self):
        way_points = list()
        way_point_1 = Position(0, 0)
        way_point_2 = Position(500, -500)
        intermediary_way_point = Position(250, -250)
        way_points.append(way_point_1)
        way_points.append(way_point_2)
        result = path_definition_refinement.generate_way_point_list_with_max_distance(way_points,
                                                                                      self.MAX_DISTANCE_BETWEEN_WAYPOINTS)
        self.assertEqual(3, len(result))
        self.assertEqual(way_point_1, result[0])
        self.assertEqual(intermediary_way_point, result[1])
        self.assertEqual(way_point_2, result[2])

    def test_path_with_waypoint_distance_higher_than_max_distance_inverted(self):
        way_points = list()
        way_point_1 = Position(0, 0)
        way_point_2 = Position(-500, 500)
        intermediary_way_point = Position(-250, 250)
        way_points.append(way_point_1)
        way_points.append(way_point_2)
        result = path_definition_refinement.generate_way_point_list_with_max_distance(way_points,
                                                                                      self.MAX_DISTANCE_BETWEEN_WAYPOINTS)
        self.assertEqual(3, len(result))
        self.assertEqual(way_point_1, result[0])
        self.assertEqual(intermediary_way_point, result[1])
        self.assertEqual(way_point_2, result[2])

    def test_path_with_waypoint_distance_higher_than_max_distance_inverted_negative_slope(self):
        way_points = list()
        way_point_1 = Position(0, 0)
        way_point_2 = Position(-500, -500)
        intermediary_way_point = Position(-250, -250)
        way_points.append(way_point_1)
        way_points.append(way_point_2)
        result = path_definition_refinement.generate_way_point_list_with_max_distance(way_points,
                                                                                      self.MAX_DISTANCE_BETWEEN_WAYPOINTS)
        self.assertEqual(3, len(result))
        self.assertEqual(way_point_1, result[0])
        self.assertEqual(intermediary_way_point, result[1])
        self.assertEqual(way_point_2, result[2])

    def test_path_with_waypoint_distance_higher_than_max_distance_on_y_axis(self):
        way_points = list()
        way_point_1 = Position(0, 0)
        way_point_2 = Position(0, -500)
        intermediary_way_point = Position(0, -250)
        way_points.append(way_point_1)
        way_points.append(way_point_2)
        result = path_definition_refinement.generate_way_point_list_with_max_distance(way_points,
                                                                                      self.MAX_DISTANCE_BETWEEN_WAYPOINTS)
        self.assertEqual(3, len(result))
        self.assertEqual(way_point_1, result[0])
        self.assertEqual(intermediary_way_point, result[1])
        self.assertEqual(way_point_2, result[2])

    def test_path_with_waypoint_distance_higher_than_max_distance_on_y_axis_inverted(self):
        way_points = list()
        way_point_1 = Position(0, 0)
        way_point_2 = Position(0, 500)
        intermediary_way_point = Position(0, 250)
        way_points.append(way_point_1)
        way_points.append(way_point_2)
        result = path_definition_refinement.generate_way_point_list_with_max_distance(way_points,
                                                                                      self.MAX_DISTANCE_BETWEEN_WAYPOINTS)
        self.assertEqual(3, len(result))
        self.assertEqual(way_point_1, result[0])
        self.assertEqual(intermediary_way_point, result[1])
        self.assertEqual(way_point_2, result[2])

    def test_path_with_waypoint_distance_higher_than_max_distance_on_y_axis_limit(self):
        way_points = list()
        way_point_1 = Position(0, 0)
        way_point_2 = Position(0.00000001, 500)
        intermediary_way_point = Position(0.00000001 / 2, 250)
        way_points.append(way_point_1)
        way_points.append(way_point_2)
        result = path_definition_refinement.generate_way_point_list_with_max_distance(way_points,
                                                                                      self.MAX_DISTANCE_BETWEEN_WAYPOINTS)
        self.assertEqual(3, len(result))
        self.assertEqual(way_point_1, result[0])
        self.assertEqual(intermediary_way_point, result[1])
        self.assertEqual(way_point_2, result[2])

    def test_path_with_waypoint_distance_higher_than_max_distance_on_y_axis_limit(self):
        way_points = list()
        way_point_1 = Position(0, 0)
        way_point_2 = Position(-0.00000001, 500)
        intermediary_way_point = Position(-0.00000001 / 2, 250)
        way_points.append(way_point_1)
        way_points.append(way_point_2)
        result = path_definition_refinement.generate_way_point_list_with_max_distance(way_points,
                                                                                      self.MAX_DISTANCE_BETWEEN_WAYPOINTS)
        self.assertEqual(3, len(result))
        self.assertEqual(way_point_1, result[0])
        self.assertEqual(intermediary_way_point, result[1])
        self.assertEqual(way_point_2, result[2])
