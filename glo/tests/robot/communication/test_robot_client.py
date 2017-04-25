import unittest

from mock.mock import patch, Mock, ANY

from robot.communication import addresses
from robot.communication.robot_client import RobotClient


class TestBaseStationClient(unittest.TestCase):
    LETTER = "A"
    VOLTAGE_URL = "http://127.0.0.1:80/voltage"
    TRAJECTORY_URL = "http://127.0.0.1:80/trajectory"
    TREASURES_URL = "http://127.0.0.1:80/treasures"
    DESTINATION_URL = "http://127.0.0.1:80/destination"
    LOG_URL = "http://127.0.0.1:80/log"
    ISLAND_API_URL = "https://132.203.14.228:443/?code=A"
    VALID_DATA = {"some": "data"}
    ADDRESS = "127.0.0.1"
    PORT = 80
    ISLAND_COLOR = 'vert'
    ISLAND_SHAPE = 'triangle'
    ISLAND_COLOR_RESPONSE = {'couleur': 'vert'}
    ISLAND_SHAPE_RESPONSE = {'forme': 'triangle'}

    def setUp(self):
        self.client = RobotClient()
        addresses.BASE_STATION_ADDRESS = self.ADDRESS
        addresses.BASE_STATION_PORT = self.PORT
        self.response = Mock()

    @patch('requests.put')
    def test_should_send_put_request_to_send_updated_voltage(self, mock_put):
        self.client.send_voltage(self.VALID_DATA)
        mock_put.assert_called_once_with(self.VOLTAGE_URL, json=self.VALID_DATA, timeout=2)

    @patch('requests.put')
    def test_should_send_put_request_to_send_updated_trajectory(self, mock_put):
        self.client.send_trajectory(self.VALID_DATA)
        mock_put.assert_called_once_with(self.TRAJECTORY_URL, json=self.VALID_DATA, timeout=2)

    @patch('requests.put')
    def test_should_send_the_position_of_the_treasures(self, mock_put):
        self.client.send_treasures(self.VALID_DATA)
        mock_put.assert_called_once_with(self.TREASURES_URL, json=self.VALID_DATA, timeout=2)

    @patch('requests.put')
    def test_should_send_put_request_to_send_updated_destination(self, mock_put):
        self.client.send_destination(self.VALID_DATA)
        mock_put.assert_called_once_with(self.DESTINATION_URL, json=self.VALID_DATA, timeout=2)

    @patch('requests.get')
    def test_should_do_a_get_request_to_recuperate_destination(self, mock_get):
        self.client.get_destination(self.LETTER)
        mock_get.assert_called_with(ANY, timeout=3, verify=False)

    @patch('requests.get')
    def test_gets_island_color_when_a_color_is_returned_from_island_api(self, mock_get):
        mock_get.return_value = self.response
        self.response.json.return_value = self.ISLAND_COLOR_RESPONSE
        result = self.client.get_destination('A')
        self.assertEqual(result, self.ISLAND_COLOR)

    @patch('requests.get')
    def test_gets_island_form_when_a_form_is_returned_from_island_api(self, mock_get):
        mock_get.return_value = self.response
        self.response.json.return_value = self.ISLAND_SHAPE_RESPONSE
        result = self.client.get_destination('A')
        self.assertEqual(result, self.ISLAND_SHAPE)

    @patch('requests.post')
    def test_sends_log_message(self, mock_post):
        self.client.send_log(self.VALID_DATA)
        mock_post.assert_called_once_with(self.LOG_URL, json=self.VALID_DATA, timeout=2)
