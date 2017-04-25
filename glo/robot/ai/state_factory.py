from robot.ai.state.charge_state import ChargeState
from robot.ai.state.command_injection_state import CommandInjectionState
from robot.ai.state.drop_treasure_state import DropTreasureState
from robot.ai.state.find_treasures_state import FindTreasuresState
from robot.ai.state.move_to_charge_station_state import MoveToChargeStationState
from robot.ai.state.move_to_island_state import MoveToIslandState
from robot.ai.state.move_to_treasure_state import MoveToTreasureState
from robot.ai.state.pickup_treasure_state import PickupTreasureState
from robot.ai.state.read_code_state import ReadCodeState
from robot.ai.state.stopped_state import StoppedState


class StateFactory(object):
    states_to_execute = list()

    def __init__(self):
        self.states_to_execute = list()

    def get_state(self, state_type, controller):
        if len(self.states_to_execute) > 0:
            state_type = self.states_to_execute.pop(0)

        if state_type is ChargeState:
            return ChargeState(controller)

        elif state_type is DropTreasureState:
            return DropTreasureState(controller)

        elif state_type is MoveToChargeStationState:
            return MoveToChargeStationState(controller)

        elif state_type is MoveToIslandState:
            return MoveToIslandState(controller)

        elif state_type is MoveToTreasureState:
            return MoveToTreasureState(controller)

        elif state_type is PickupTreasureState:
            return PickupTreasureState(controller)

        elif state_type is ReadCodeState:
            return ReadCodeState(controller)

        elif state_type is FindTreasuresState:
            return FindTreasuresState(controller)

        elif state_type is CommandInjectionState:
            return CommandInjectionState(controller)

        else:
            return StoppedState(controller)

    def set_states_to_execute_in_order(self, state_list):
        self.states_to_execute = list(state_list)
