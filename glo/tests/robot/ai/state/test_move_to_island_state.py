import unittest

from mock import MagicMock, Mock

from robot.ai.state.drop_treasure_state import DropTreasureState
from robot.ai.state.move_to_island_state import MoveToIslandState


class TestMoveToIslandState(unittest.TestCase):
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
        self.move_to_island_state = MoveToIslandState(self.controller, self.movement_controller)
        self.pathfinding.calculate_dijkstra_path = MagicMock()
        self.pathfinding.calculate_dijkstra_path.return_value = [[], 0]
        self.controller.pathfinding = self.pathfinding
        self.controller.position = {"x": 0, "y": 0, "w": 0}

    def test_calls_next_state_at_the_end(self):
        self.move_to_island_state.has_arrived = MagicMock()
        self.move_to_island_state.has_arrived.return_value = True

        self.move_to_island_state.handle()

        self.controller.set_state.assert_called_with(DropTreasureState)
        self.controller.activate.assert_called_with()

    def test_calls_move_if_not_arrived(self):
        self.movement_controller.is_at_position = self.one_false
        self.move_to_island_state.handle()
        self.movement_controller.move.assert_called_once_with(self.move_to_island_state.island_position,
                                                              self.move_to_island_state.waypoints,
                                                              self.controller.position)
