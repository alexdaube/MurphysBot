import unittest

from mock import MagicMock, Mock

from robot.ai.state.drop_treasure_state import DropTreasureState
from robot.ai.state.stopped_state import StoppedState


class TestDropTreasureState(unittest.TestCase):
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
        self.prehensor_controller = Mock()
        self.drop_treasure_state = DropTreasureState(self.controller, self.movement_controller,
                                                     self.prehensor_controller)

    def test_calls_next_state_at_the_end(self):
        self.movement_controller.is_aligned_with_island = MagicMock()
        self.movement_controller.is_aligned_with_island.return_value = True

        self.drop_treasure_state.handle()

        self.controller.set_state.assert_called_with(StoppedState)
        self.controller.activate.assert_called_with()

    def test_if_not_aligned_with_island_move_towards_island(self):
        self.movement_controller.is_aligned_with_island = self.one_false
        self.controller.island_description = "Description"
        self.controller.island_color = "Color"

        self.drop_treasure_state.handle()

        self.movement_controller.fall_into_line_with_island.assert_called_once_with(
            "Description", "Color")
