import unittest

from mock import Mock

from common.map.point_of_interest.point_of_interest_type import PointOfInterestType
from robot.ai.fine_movement_controller import FineMovementController


class TestFineMovementController(unittest.TestCase):
    def setUp(self):
        self.vision = Mock()
        self.camera_controller = Mock()
        self.wheel_controller = Mock()
        self.controller = FineMovementController(self.vision, self.camera_controller, self.wheel_controller)

    def test_can_back_away(self):
        self.controller.back_away()
        self.camera_controller.reset_orientation.assert_called_once_with()
        self.wheel_controller.move_forward.assert_called_once_with(0.075, 0.1)

    def test_can_complete_approach(self):
        self.controller.ram_it()
        self.camera_controller.reset_orientation.assert_called_once_with()
        self.wheel_controller.move_forward.assert_called_once_with(-0.06, 0.1)

    def test_can_move_towards_charge_station(self):
        picture = Mock()
        picture.__len__ = Mock(return_value=640)
        self.vision.detect_recharge_station.return_value = {"x": 320, "y": 500}, [picture]

        # self.controller.move_towards_charge_station()

        self.wheel_controller.move_forward.assert_called_once_with(-0.01, 0.15)

    def test_sets_camera_orientation_before_charge_station_approach(self):
        picture = Mock()
        picture.__len__ = Mock(return_value=640)
        self.vision.detect_recharge_station.return_value = {"x": 320, "y": 500}, [picture]

        # self.controller.move_towards_charge_station()

        self.camera_controller.set_orientation.assert_called_with(-30, 0)

    def test_can_move_right_when_off_course_to_charge_station(self):
        picture = Mock()
        picture.__len__ = Mock(return_value=640)
        self.vision.detect_recharge_station.side_effect = [[{"x": 400, "y": 500}, [picture]],
                                                           [{"x": 320, "y": 500}, [picture]]]

        self.controller.move_towards_charge_station()

        self.wheel_controller.move_lateral_cart.assert_called_once_with(0.01, 0, 0.1)

    def test_can_move_left_when_off_course_to_charge_station(self):
        picture = Mock()
        picture.__len__ = Mock(return_value=640)
        self.vision.detect_recharge_station.side_effect = [[{"x": 300, "y": 500}, [picture]],
                                                           [{"x": 320, "y": 500}, [picture]]]

        self.controller.move_towards_charge_station()

        self.wheel_controller.move_lateral_cart.assert_called_once_with(-0.01, 0, 0.1)

    def test_can_reorient_camera_when_no_charge_station_is_detected_on_approach(self):
        picture = Mock()
        picture.__len__ = Mock(return_value=640)
        self.vision.detect_recharge_station.side_effect = [[{}, [picture]],
                                                           [{"x": 320, "y": 500}, [picture]]]

        self.controller.move_towards_charge_station()

        self.camera_controller.set_orientation.assert_called_with(-35, 0)

    def test_can_move_towards_treasure(self):
        picture = Mock()
        picture.__len__ = Mock(return_value=640)
        self.vision.detect_treasures.return_value = [[350, 500]], [picture]

        self.controller.move_towards_treasure()

        self.wheel_controller.move_forward.assert_called_once_with(-0.02, 0.15)

    def test_sets_camera_orientation_before_treasure_approach(self):
        picture = Mock()
        picture.__len__ = Mock(return_value=640)
        self.vision.detect_treasures.return_value = [[350, 500]], [picture]

        self.controller.move_towards_treasure()

        self.camera_controller.set_orientation.assert_called_with(-60, 0)

    def test_can_move_right_when_off_course_to_treasure(self):
        picture = Mock()
        picture.__len__ = Mock(return_value=640)
        self.vision.detect_treasures.side_effect = [[[[400, 500]], [picture]],
                                                    [[[350, 500]], [picture]]]

        self.controller.move_towards_treasure()

        self.wheel_controller.move_lateral_cart.assert_called_once_with(0.01, 0, 0.15)

    def test_can_move_left_when_off_course_to_treasure(self):
        picture = Mock()
        picture.__len__ = Mock(return_value=640)
        self.vision.detect_treasures.side_effect = [[[[300, 500]], [picture]],
                                                    [[[350, 500]], [picture]]]

        self.controller.move_towards_treasure()

        self.wheel_controller.move_lateral_cart.assert_called_once_with(-0.01, 0, 0.15)

    def test_can_reorient_camera_when_no_treasures_are_detected_on_approach(self):
        picture = Mock()
        picture.__len__ = Mock(return_value=640)
        self.vision.detect_treasures.side_effect = [[[], [picture]],
                                                    [[[350, 500]], [picture]]]

        self.controller.move_towards_treasure()

        self.camera_controller.set_orientation.assert_called_with(-65, 0)

    def test_moves_backwards_before_verifying_treasure_grab(self):
        self.vision.detect_treasures.return_value = [self.controller.magnet_position], None
        self.controller.verify_treasure_grab()
        self.wheel_controller.move_forward.assert_called_once_with(0.075, 0.1)

    def test_sets_camera_orientation_before_verifying_treasure_grab(self):
        self.vision.detect_treasures.return_value = [self.controller.magnet_position], None
        self.controller.verify_treasure_grab()
        self.camera_controller.set_orientation.assert_called_once_with(-90, 0)

    def test_can_verify_treasure_grab(self):
        self.vision.detect_treasures.return_value = [self.controller.magnet_position], None
        self.assertTrue(self.controller.verify_treasure_grab())

    def test_can_verify_treasure_not_grabbed(self):
        self.vision.detect_treasures.return_value = [[0, 0]], None
        self.assertFalse(self.controller.verify_treasure_grab())

    def test_sets_camera_orientation_before_verifying_if_treasure_is_near(self):
        self.vision.detect_treasures.return_value = [[0, self.controller.magnet_position[1] + 300]], None
        self.controller.is_near_treasure()
        self.camera_controller.set_orientation.assert_called_once_with(-90, 0)

    def test_can_verify_if_is_near_treasure(self):
        self.vision.detect_treasures.return_value = [[self.controller.magnet_position[0],
                                                      self.controller.magnet_position[1] + 300]], None
        self.assertTrue(self.controller.is_near_treasure())

    def test_can_verify_if_is_not_near_treasure(self):
        self.vision.detect_treasures.return_value = [[0, self.controller.magnet_position[1] - 300]], None
        self.assertFalse(self.controller.is_near_treasure())

    def test_can_verify_if_is_aligned_with_island(self):
        self.vision.detect_island.return_value = [{"POIColor": PointOfInterestType.RED_COLOR,
                                                   "points": self.controller.magnet_position}], None
        self.assertTrue(self.controller.is_aligned_with_island(PointOfInterestType.RED_COLOR))

    def test_can_verify_if_is_not_aligned_with_island(self):
        self.vision.detect_island.return_value = [{"POIColor": PointOfInterestType.RED_COLOR,
                                                   "points": [0, 0]},
                                                  {"POIColor": PointOfInterestType.BLUE_COLOR,
                                                   "points": self.controller.magnet_position}], None
        self.assertFalse(self.controller.is_aligned_with_island(PointOfInterestType.RED_COLOR))

    def test_can_move_towards_island(self):
        self.vision.detect_island.return_value = {"points": self.controller.magnet_position}, None
        self.controller.fall_into_line_with_island(PointOfInterestType.CIRCLE_ISLAND,
                                                   PointOfInterestType.RED_COLOR)
        self.wheel_controller.move_forward.assert_called_once_with(-0.025, 0.15)

    def test_sets_camera_orientation_before_island_approach(self):
        self.vision.detect_island.return_value = {"points": self.controller.magnet_position}, None
        self.controller.fall_into_line_with_island(PointOfInterestType.CIRCLE_ISLAND,
                                                   PointOfInterestType.RED_COLOR)
        self.camera_controller.set_orientation.assert_called_with(-90, 0)

    def test_can_move_right_when_off_course_to_island(self):
        self.vision.detect_island.side_effect = [
            [{"points": [1000, 500]}, None],
            [{"points": self.controller.magnet_position}, None]
        ]
        self.controller.fall_into_line_with_island(PointOfInterestType.CIRCLE_ISLAND,
                                                   PointOfInterestType.RED_COLOR)
        self.wheel_controller.move_lateral_cart.assert_called_once_with(0.03, 0, 0.10)

    def test_can_move_left_when_off_course_to_island(self):
        self.vision.detect_island.side_effect = [
            [{"points": [0, 500]}, None],
            [{"points": self.controller.magnet_position}, None]
        ]

        self.controller.fall_into_line_with_island(PointOfInterestType.CIRCLE_ISLAND,
                                                   PointOfInterestType.RED_COLOR)

        self.wheel_controller.move_lateral_cart.assert_called_once_with(-0.03, 0, 0.10)

    def test_can_reorient_camera_when_no_islands_are_detected_on_approach(self):
        self.vision.detect_island.side_effect = [
            [None, None],
            [{"points": self.controller.magnet_position}, None]
        ]

        self.controller.fall_into_line_with_island(PointOfInterestType.CIRCLE_ISLAND,
                                                   PointOfInterestType.RED_COLOR)

        self.camera_controller.set_orientation.assert_called_with(-85, 0)
