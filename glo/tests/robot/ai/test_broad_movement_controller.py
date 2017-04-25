import math
import unittest

from mock import Mock, MagicMock

from common.map.position import Position
from robot.ai.broad_movement_controller import BroadMovementController


class TestBroadMovementController(unittest.TestCase):
    def setUp(self):
        self.wheel_controller = Mock()
        self.controller = BroadMovementController(self.wheel_controller)

    def test_can_move_to_point_straight_forward(self):
        robot_pos = {"x": 0, "y": 0, "w": 0}

        self.controller.move(Position(1000, 0), [], robot_pos)

        self.wheel_controller.move_lateral_polar.assert_called_once_with(0, self.controller.MAXIMUM_MOVE / 1000,
                                                                         self.controller.MOVE_SPEED)

    def test_can_move_to_point_straight_backwards(self):
        robot_pos = {"x": 1000, "y": 0, "w": 0}

        self.controller.move(Position(0, 0), [], robot_pos)

        self.wheel_controller.move_lateral_polar.assert_called_once_with(-180, self.controller.MAXIMUM_MOVE / 1000,
                                                                         self.controller.MOVE_SPEED)

    def test_can_move_to_point_at_minus_45_degrees(self):
        robot_pos = {"x": 0, "y": 0, "w": 0}

        self.controller.move(Position(1000, 1000), [], robot_pos)

        self.wheel_controller.move_lateral_polar.assert_called_once_with(-45, self.controller.MAXIMUM_MOVE / 1000,
                                                                         self.controller.MOVE_SPEED)

    def test_can_move_to_point_at_60_degrees(self):
        robot_pos = {"x": 5000, "y": 5000, "w": 180}
        ratio = math.tan(math.radians(60))

        self.controller.move(Position(4000, 5000 + 1000 * ratio), [], robot_pos)

        self.wheel_controller.move_lateral_polar.assert_called_once_with(60, self.controller.MAXIMUM_MOVE / 1000,
                                                                         self.controller.MOVE_SPEED)

    def test_can_move_to_point_at_170_degrees(self):
        robot_pos = {"x": 500, "y": 500, "w": 180}
        ratio = math.tan(math.radians(10))

        self.controller.move(Position(1500, 500 + 1000 * ratio), [], robot_pos)

        self.wheel_controller.move_lateral_polar.assert_called_once_with(170, self.controller.MAXIMUM_MOVE / 1000,
                                                                         self.controller.MOVE_SPEED)

    def test_can_move_to_next_waypoint(self):
        robot_pos = {"x": 0, "y": 0, "w": 0}
        self.controller.move(Position(1000, 0), [Position(0, 1000)], robot_pos)
        self.wheel_controller.move_lateral_polar.assert_called_once_with(-90, self.controller.MAXIMUM_MOVE / 1000,
                                                                         self.controller.MOVE_SPEED)

    def test_move_skips_next_waypoint_if_it_is_already_there(self):
        robot_pos = {"x": 0, "y": 0, "w": 0}
        self.controller.move(Position(0, 1000), [Position(0, 0)], robot_pos)
        self.wheel_controller.move_lateral_polar.assert_called_once_with(-90, self.controller.MAXIMUM_MOVE / 1000,
                                                                         self.controller.MOVE_SPEED)

    def test_can_rotate_to_face_top_wall(self):
        robot_pos = {"x": 0, "y": 0, "w": 45}
        self.controller.rotate = MagicMock()

        self.controller.face_wall('top', robot_pos)

        self.controller.rotate.assert_called_once_with(270, robot_pos)

    def test_can_rotate_to_face_bottom_wall(self):
        robot_pos = {"x": 0, "y": 0, "w": 45}
        self.controller.rotate = MagicMock()

        self.controller.face_wall('bottom', robot_pos)

        self.controller.rotate.assert_called_once_with(90, robot_pos)

    def test_can_rotate_to_face_back_wall(self):
        robot_pos = {"x": 0, "y": 0, "w": 45}
        self.controller.rotate = MagicMock()

        self.controller.face_wall('back', robot_pos)

        self.controller.rotate.assert_called_once_with(180, robot_pos)

    def test_can_rotate_to_face_point(self):
        robot_pos = {"x": 0, "y": 0, "w": 270}
        self.controller.rotate = MagicMock()
        self.controller.face_point(Position(0, 100), robot_pos)
        self.controller.rotate.assert_called_once_with(90, robot_pos)

    def test_can_rotate_to_face_point2(self):
        robot_pos = {"x": 0, "y": 0, "w": 270}
        self.controller.rotate = MagicMock()
        self.controller.face_point(Position(100, 100), robot_pos)
        self.controller.rotate.assert_called_once_with(45, robot_pos)

    def test_can_rotate_to_face_point3(self):
        robot_pos = {"x": 0, "y": 0, "w": 90}
        self.controller.rotate = MagicMock()
        self.controller.face_point(Position(100, 100), robot_pos)
        self.controller.rotate.assert_called_once_with(45, robot_pos)

    def test_can_determine_if_robot_is_at_position(self):
        robot_pos = {"x": 0, "y": 0, "w": 90}
        self.assertTrue(self.controller.is_at_position(robot_pos, Position(100, 0), 100))

    def test_can_determine_if_robot_is_not_at_position(self):
        robot_pos = {"x": 0, "y": 0, "w": 90}
        self.assertFalse(self.controller.is_at_position(robot_pos, Position(101, 0), 100))
