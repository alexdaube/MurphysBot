import unittest

from mock.mock import patch

from basestation.communication import addresses
from basestation.communication.base_station_client import BaseStationClient


class TestBaseStationClient(unittest.TestCase):
    ROBOT_EXECUTION_URL = "http://127.0.0.1:80/start_robot"
    ROBOT_WITH_STATES_TO_EXECUTE_LIST_URL = "http://127.0.0.1:80/start_robot_with_execution_states"
    ROBOT_POSITION_URL = "http://127.0.0.1:80/robot_position"
    ISLAND_POSITIONS_URL = "http://127.0.0.1:80/island_positions"
    SEND_COMMAND_URL = "http://127.0.0.1:80/send_command"
    VALID_DATA = {"some": "data"}
    ADDRESS = "127.0.0.1"
    PORT = 80

    def setUp(self):
        self.client = BaseStationClient()
        addresses.ROBOT_ADDRESS = self.ADDRESS
        addresses.ROBOT_PORT = self.PORT

    @patch('requests.post')
    def test_should_send_post_request_to_signal_robot_execution(self, mock_post):
        self.client.start_robot_execution()
        mock_post.assert_called_once_with(self.ROBOT_EXECUTION_URL, timeout=2)

    @patch('requests.put')
    def test_should_send_put_request_to_send_updated_robot_position(self, mock_put):
        self.client.send_robot_position(self.VALID_DATA)
        mock_put.assert_called_once_with(self.ROBOT_POSITION_URL, json=self.VALID_DATA, timeout=2)

    @patch('requests.put')
    def test_should_send_put_request_to_send_updated_island_positions(self, mock_put):
        self.client.send_island_positions(self.VALID_DATA)
        mock_put.assert_called_once_with(self.ISLAND_POSITIONS_URL, json=self.VALID_DATA, timeout=2)

    @patch('requests.put')
    def test_should_send_post_request_to_signal_robot_execution(self, mock_put):
        self.client.start_robot_execution_with_state_list(self.VALID_DATA)
        mock_put.assert_called_once_with(self.ROBOT_WITH_STATES_TO_EXECUTE_LIST_URL, json=self.VALID_DATA,
                                         timeout=2)

    @patch('requests.put')
    def test_should_send_post_request_to_send_command(self, mock_put):
        self.client.send_command(self.VALID_DATA)
        mock_put.assert_called_once_with(self.SEND_COMMAND_URL, json=self.VALID_DATA,
                                         timeout=2)
