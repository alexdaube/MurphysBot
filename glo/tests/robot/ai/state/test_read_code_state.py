import unittest

from mock import Mock

from robot.ai.state.move_to_treasure_state import MoveToTreasureState
from robot.ai.state.read_code_state import ReadCodeState


class TestReadCodeState(unittest.TestCase):
    LETTER = ''
    DESTINATION_FROM_API = {}

    def setUp(self):
        self.controller = Mock()
        self.manchester_decoder = Mock()
        self.movement_controller = Mock()
        self.client = Mock()
        self.read_code_state = ReadCodeState(self.controller, self.manchester_decoder, self.movement_controller,
                                             self.client)

    def test_calls_next_state_at_the_end(self):
        self.read_code_state.handle()

        self.controller.set_state.assert_called_with(MoveToTreasureState)
        self.controller.activate.assert_called_with()

    def test_gets_destination_from_island_api(self):
        self.read_code_state.send_letter(self.LETTER)
        self.client.get_destination.assert_called_with(self.LETTER)

    def test_sends_destination_to_base_station(self):
        self.client.get_destination.return_value = self.DESTINATION_FROM_API
        self.read_code_state.send_letter(self.LETTER)
        destination = {'letter': self.LETTER, 'description': self.DESTINATION_FROM_API}
        self.client.send_destination.assert_called_with(destination)
