import time
import unittest

from mock.mock import Mock, patch

from common.map.decomposition_map.decomposition_map import DecompositionMap
from common.map.point_of_interest.island.island_factory import IslandFactory
from common.map.point_of_interest.point_of_interest_type import PointOfInterestType
from common.map.point_of_interest.treasure import Treasure
from common.map.position import Position
from robot.ai.robot_controller import RobotController


class TestRobotController(unittest.TestCase):
    def setUp(self):
        self.robot_client = Mock()
        self.state = Mock()
        self.state_factory = Mock()
        self.robot_vision = Mock()
        self.pathfinding = Mock()
        self.state_factory.get_state.return_value = self.state
        self.controller = RobotController(self.robot_client, self.robot_vision, Mock, self.state_factory,
                                          self.pathfinding)

    def test_activating_calls_first_state(self):
        self.controller.activate()
        time.sleep(0.1)
        self.state.handle.assert_called_once_with()

    def test_can_set_state(self):
        new_state = Mock()
        self.state_factory.get_state.return_value = new_state

        self.controller.set_state(type(Mock))

        self.assertEqual(new_state, self.controller.current_state)

    @patch('common.map.decomposition_map.decomposition_map.DecompositionMap.__new__')
    def test_updating_islands_creates_new_map(self, decomp_map):
        decomp_map.return_value = Mock()
        self.controller.update_island_positions([])
        decomp_map.assert_called_with(DecompositionMap, 0, 0)

    @patch('common.map.point_of_interest.island.island_factory.IslandFactory.create_island')
    @patch('common.map.decomposition_map.decomposition_map.DecompositionMap.__new__')
    def test_can_create_islands_in_map(self, decomp_map, create_island):
        self.robot_vision.get_average_point.return_value = [5, 6]
        decomp_map.return_value = Mock()

        self.controller.update_island_positions([{"points": [], "POIType": PointOfInterestType.TRIANGLE_ISLAND,
                                                  "POIColor": "color"}])

        create_island.assert_called_with(PointOfInterestType.TRIANGLE_ISLAND, "color", Position(5, 6))

    @patch('common.map.point_of_interest.island.island_factory.IslandFactory.create_island')
    @patch('common.map.decomposition_map.decomposition_map.DecompositionMap.__new__')
    def test_can_update_islands(self, decomp_map_new, create_island):
        decomp_map = Mock()
        decomp_map_new.return_value = decomp_map
        island = Mock()
        create_island.return_value = island
        self.robot_vision.get_average_point.return_value = [5, 6]

        self.controller.update_island_positions([{"points": [], "POIType": "", "POIColor": ""}])

        decomp_map.add_island.assert_called_with(island)

    @patch('common.map.point_of_interest.treasure.Treasure.__new__')
    def test_can_add_treasures(self, treasure_new):
        treasure = Mock()
        treasure_new.return_value = treasure

        self.controller.add_treasures([[1, 2]])

        treasure_new.assert_called_once_with(Treasure, Position(1, 2))
        self.pathfinding.add_treasure.assert_called_once_with(treasure)

    def test_set_execution_states_call_state_factory_set_states_to_execute_in_order(self):
        list_of_states = Mock()
        self.controller.set_execution_states(list_of_states)

        self.state_factory.set_states_to_execute_in_order.assert_called_once_with(list_of_states)

    def test_can_update_robot_position(self):
        self.controller.update_position(1, 1, None)
        self.controller.update_position(1, 1, 1)
        self.controller.update_position(10, 10, 10)
        self.controller.update_position(10, 10, 10)
        self.controller.update_position(3, 5, 3)
        self.controller.update_position(4, 3, 6)
        self.controller.update_position(1, 1, 1)

        self.assertEqual(self.controller.position["x"], 4)
        self.assertEqual(self.controller.position["y"], 5)
        self.assertEqual(self.controller.position["w"], 6)

    def test_can_set_destination(self):
        self.pathfinding.point_of_interest_list = [
            IslandFactory.create_island(PointOfInterestType.CIRCLE_ISLAND,
                                        PointOfInterestType.BLUE_COLOR, Position(0, 0))]

        self.controller.set_destination(PointOfInterestType.BLUE_COLOR)

        self.assertEqual(self.controller.island_color, PointOfInterestType.BLUE_COLOR)
        self.assertEqual(self.controller.island_description, PointOfInterestType.CIRCLE_ISLAND)

    def test_can_send_voltage(self):
        prehensor_controller = Mock()
        prehensor_controller.get_capacitor_tension.side_effect = [45, None]

        self.controller.send_voltage(prehensor_controller)

        self.assertEqual(self.controller.voltage, 45)
        self.robot_client.send_voltage.assert_called_once_with({"voltage": 45})

    def test_can_send_path(self):
        self.controller.position = {"x": 0, "y": 0, "w": 0}
        self.controller.send_path([Position(100, 0), Position(100, 100)], Position(200, 200))

        self.robot_client.send_trajectory.assert_called_once_with({"trajectory": [[0, 0], [100, 0],
                                                                                  [100, 100], [200, 200]]})
