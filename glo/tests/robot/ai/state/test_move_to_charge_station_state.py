import unittest

from mock import MagicMock, Mock

from robot.ai.state.charge_state import ChargeState
from robot.ai.state.move_to_charge_station_state import MoveToChargeStationState


class TestMoveToChargeStationState(unittest.TestCase):
    called_times = 0

    def one_false(self, *args):
        if self.called_times == 0:
            self.called_times += 1
            return False
        else:
            return True

    def setUp(self):
        self.controller = Mock()
        self.movement_controller = Mock()
        self.pathfinding = Mock()
        self.move_to_charge_station_state = MoveToChargeStationState(self.controller, self.movement_controller)
        self.pathfinding.calculate_dijkstra_path = MagicMock()
        self.treasure_position = Mock(Y=0)
        self.pathfinding.calculate_dijkstra_path.return_value = [[], self.treasure_position]
        self.controller.pathfinding = self.pathfinding
        self.controller.position = {"x": 0, "y": 0, "w": 0}

    def test_calls_next_state_at_the_end(self):
        self.move_to_charge_station_state.has_arrived = MagicMock()
        self.move_to_charge_station_state.has_arrived.return_value = True

        self.move_to_charge_station_state.handle()

        self.controller.set_state.assert_called_with(ChargeState)
        self.controller.activate.assert_called_with()

    def test_calls_move_if_not_arrived(self):
        self.movement_controller.is_at_position = self.one_false
        self.move_to_charge_station_state.handle()
        self.movement_controller.move.assert_called_once_with(self.move_to_charge_station_state.charge_station_position,
                                                              self.move_to_charge_station_state.waypoints,
                                                              self.controller.position)

    def test_should_face_top_wall(self):
        self.movement_controller.is_at_position = self.one_false
        self.move_to_charge_station_state.handle()
        self.movement_controller.face_wall.assert_called_once_with('top', self.controller.position)
