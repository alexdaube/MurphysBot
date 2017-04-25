import unittest

from mock import Mock

from robot.ai.state.charge_state import ChargeState
from robot.ai.state.drop_treasure_state import DropTreasureState
from robot.ai.state.move_to_charge_station_state import MoveToChargeStationState
from robot.ai.state.move_to_island_state import MoveToIslandState
from robot.ai.state.move_to_treasure_state import MoveToTreasureState
from robot.ai.state.pickup_treasure_state import PickupTreasureState
from robot.ai.state.read_code_state import ReadCodeState
from robot.ai.state.stopped_state import StoppedState
from robot.ai.state_factory import StateFactory


class TestStateFactory(unittest.TestCase):
    state_list = [ChargeState, MoveToChargeStationState, DropTreasureState, MoveToIslandState,
                  MoveToTreasureState, PickupTreasureState, ReadCodeState, StoppedState]
    states_to_execute = [PickupTreasureState, DropTreasureState, StoppedState]

    def setUp(self):
        self.state_factory = StateFactory()

    def test_can_create_all_states(self):
        controller = Mock()
        for state_type in self.state_list:
            state = self.state_factory.get_state(state_type, controller)

            self.assertTrue(isinstance(state, state_type))
            self.assertEquals(state.controller, controller)

    def test_return_states_to_execute_in_order_when_state_to_execute_set(self):
        self.state_factory.set_states_to_execute_in_order(self.states_to_execute)
        controller = Mock()
        for state_type in self.states_to_execute:
            state = self.state_factory.get_state(state_type, controller)

            self.assertEquals(state_type, type(state))
            self.assertEquals(state.controller, controller)

    def test_after_all_states_to_execute_state_to_execute_list_should_be_empty(self):
        self.state_factory.set_states_to_execute_in_order(self.states_to_execute)
        controller = Mock()
        for state_type in self.states_to_execute:
            state = self.state_factory.get_state(state_type, controller)

        self.assertTrue(len(self.state_factory.states_to_execute) == 0)
