import unittest

from robot.ai.state.charge_state import ChargeState
from robot.ai.state.drop_treasure_state import DropTreasureState
from robot.ai.state.find_treasures_state import FindTreasuresState
from robot.ai.state.move_to_charge_station_state import MoveToChargeStationState
from robot.ai.state.move_to_island_state import MoveToIslandState
from robot.ai.state.move_to_treasure_state import MoveToTreasureState
from robot.ai.state.pickup_treasure_state import PickupTreasureState
from robot.ai.state.read_code_state import ReadCodeState
from robot.ai.state.stopped_state import StoppedState
from robot.ai.string_to_state_type import string_to_state_type


class TestStringToStateClassType(unittest.TestCase):
    def test_MoveToIslandState_return_MoveToIslandState_type(self):
        self.assertEqual(MoveToIslandState, string_to_state_type("MoveToIslandState"))

    def test_ChargeState_return_ChargeState_type(self):
        self.assertEqual(ChargeState, string_to_state_type("ChargeState"))

    def test_DropTreasureState_return_DropTreasureState_type(self):
        self.assertEqual(DropTreasureState, string_to_state_type("DropTreasureState"))

    def test_MoveToChargeStationState_return_MoveToChargeStationState_type(self):
        self.assertEqual(MoveToChargeStationState, string_to_state_type("MoveToChargeStationState"))

    def test_MoveToTreasureState_return_MoveToTreasureState_type(self):
        self.assertEqual(MoveToTreasureState, string_to_state_type("MoveToTreasureState"))

    def test_PickupTreasureState_return_PickupTreasureState_type(self):
        self.assertEqual(PickupTreasureState, string_to_state_type("PickupTreasureState"))

    def test_ReadCodeState_return_ReadCodeState_type(self):
        self.assertEqual(ReadCodeState, string_to_state_type("ReadCodeState"))

    def test_FindTreasuresState_return_FindTreasuresState_type(self):
        self.assertEqual(FindTreasuresState, string_to_state_type("FindTreasuresState"))

    def test_StoppedState_return_StoppedState_type(self):
        self.assertEqual(StoppedState, string_to_state_type("StoppedState"))

    def test_Unrecognized_string_return_StoppedState_type(self):
        self.assertEqual(StoppedState, string_to_state_type("StoppedState"))
