import unittest

from mock import MagicMock, Mock

from robot.ai.state.move_to_island_state import MoveToIslandState
from robot.ai.state.pickup_treasure_state import PickupTreasureState


class TestPickupTreasureState(unittest.TestCase):
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
        self.magnet_controller = Mock()
        self.pickup_treasure_state = PickupTreasureState(self.controller, self.movement_controller,
                                                         self.magnet_controller)

    def test_calls_next_state_at_the_end(self):
        self.pickup_treasure_state.is_picked_up = MagicMock()
        self.pickup_treasure_state.is_picked_up.return_value = True

        self.pickup_treasure_state.handle()

        self.controller.set_state.assert_called_with(MoveToIslandState)
        self.controller.activate.assert_called_with()

    def test_moves_towards_treasure_if_not_picked_up(self):
        self.movement_controller.is_near_treasure = self.one_false

        self.pickup_treasure_state.handle()

        self.movement_controller.move_towards_treasure.assert_called_once_with()
