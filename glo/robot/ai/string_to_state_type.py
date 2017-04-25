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


def string_to_state_type(string):
    if string == "ChargeState":
        return ChargeState

    elif string == "DropTreasureState":
        return DropTreasureState

    elif string == "MoveToChargeStationState":
        return MoveToChargeStationState

    elif string == "MoveToIslandState":
        return MoveToIslandState

    elif string == "MoveToTreasureState":
        return MoveToTreasureState

    elif string == "PickupTreasureState":
        return PickupTreasureState

    elif string == "ReadCodeState":
        return ReadCodeState

    elif string == "FindTreasuresState":
        return FindTreasuresState

    elif string == "CommandInjectionState":
        return CommandInjectionState

    else:
        return StoppedState
