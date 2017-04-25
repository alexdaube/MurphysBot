import unittest

from mock import MagicMock, Mock

from common.constants import TABLE_HEIGHT
from robot.ai.state.find_treasures_state import FindTreasuresState
from robot.ai.state.move_to_charge_station_state import MoveToChargeStationState


class TestFindTreasuresState(unittest.TestCase):
    def setUp(self):
        self.controller = Mock()
        self.robot_vision = Mock()
        self.camera_controller = Mock()
        self.wheel_controller = Mock()
        self.find_treasures_state = FindTreasuresState(self.controller, self.robot_vision, self.camera_controller,
                                                       self.wheel_controller)

    def test_calls_next_state_at_the_end(self):
        self.robot_vision.detect_treasures = MagicMock()
        self.robot_vision.detect_treasures.return_value = [[], [[]]]

        self.find_treasures_state.handle()

        self.controller.set_state.assert_called_with(MoveToChargeStationState)
        self.controller.activate.assert_called_with()

    def test_can_average_treasure_positions(self):
        treasures = [[0, 250], [0, 240], [0, 245]]
        average_treasures = self.find_treasures_state.average_found_treasure_positions(treasures)
        self.assertListEqual(average_treasures, [[0, 245]])

    def test_average_treasures_will_not_group_treasures_too_far(self):
        treasures = [[0, 200], [0, 300]]
        average_treasures = self.find_treasures_state.average_found_treasure_positions(treasures)
        self.assertListEqual(average_treasures, [[0, 200], [0, 300]])

    def test_can_find_treasures_in_first_quadrant(self):
        self.controller.position = {"x": 500, "y": 200, "w": 180}
        position = self.find_treasures_state.get_treasure_position(85)
        self.assertListEqual(position, [423, 0])

    def test_can_find_treasures_in_back_wall(self):
        self.controller.position = {"x": 500, "y": 200, "w": 180}
        position = self.find_treasures_state.get_treasure_position(5)
        self.assertListEqual(position, [0, 162])

    def test_can_find_treasures_in_back_wall2(self):
        self.controller.position = {"x": 500, "y": 200, "w": 180}
        position = self.find_treasures_state.get_treasure_position(-10)
        self.assertListEqual(position, [0, 278])

    def test_can_find_treasures_in_second_quadrant(self):
        self.controller.position = {"x": 500, "y": 200, "w": 180}
        position = self.find_treasures_state.get_treasure_position(-85)
        self.assertListEqual(position, [357, TABLE_HEIGHT])

    def test_can_find_treasures_in_third_quadrant(self):
        self.controller.position = {"x": 500, "y": 200, "w": 0}
        position = self.find_treasures_state.get_treasure_position(85)
        self.assertListEqual(position, [643, TABLE_HEIGHT])

    def test_can_find_treasures_in_fourth_quadrant(self):
        self.controller.position = {"x": 500, "y": 200, "w": 0}
        position = self.find_treasures_state.get_treasure_position(-85)
        self.assertListEqual(position, [577, 0])
