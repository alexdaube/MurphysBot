import unittest

from mock.mock import Mock, MagicMock

from basestation.communication.base_station_api import BaseStationAPI, BadDestinationError, BadTreasuresError, \
    BadVoltageError, BadTrajectoryError, BadLogError
from common.communication.base_api import NotJSONException


class TestBaseStationAPI(unittest.TestCase):
    flask_app = None
    base_station_api = None
    handler = {None: {404: None, 400: None}}
    INVALID_TRAJECTORY_DATA = {"some": "data"}
    TRAJECTORY_DATA = {"trajectory": "data"}
    INVALID_VOLTAGE_DATA = {"some": "data"}
    VOLTAGE_DATA = {"voltage": "data"}
    LOG_DATA = {'log': "data"}
    INVALID_LOG_DATA = {'some': 'data'}
    TREASURE_DATA = {'treasures': []}
    INVALID_TREASURE_DATA = {"some": "data"}
    DESTINATION_DATA = {"letter": "data", "description": "data"}
    DESTINATION_DATA_WITHOUT_DESCRIPTION = {"letter": "data"}
    DESTINATION_DATA_WITHOUT_LETTER = {"description": "data"}
    INVALID_DATA = {}
    RESPONSE_MESSAGE = {}
    SUCCESS_CODE = 200

    def __get_handler(self, accessor):
        return self.handler[accessor]

    def __set_handler(self, accessor, val):
        self.handler[accessor] = val

    def setUp(self):
        self.flask_app = Mock()
        self.utils = Mock()
        self.flask_app.error_handler_spec = MagicMock(spec_set=dict)
        self.flask_app.error_handler_spec.__getitem__.side_effect = self.__get_handler
        self.flask_app.error_handler_spec.__setitem__.side_effect = self.__set_handler
        self.base_station_api = BaseStationAPI(self.flask_app, {}, self.utils)

    def test_api_should_raise_NotJSONException_for_destination_update_if_request_data_is_not_valid(self):
        self.utils.get_request_json.return_value = self.INVALID_DATA
        self.assertRaises(NotJSONException, self.base_station_api.receive_destination)

    def test_api_should_raise_BadDestinationError_for_destination_update_if_description_is_missing(self):
        self.utils.get_request_json.return_value = self.DESTINATION_DATA_WITHOUT_DESCRIPTION
        self.assertRaises(BadDestinationError, self.base_station_api.receive_destination)

    def test_api_should_raise_BadDestinationError_for_destination_update_if_letter_is_missing(self):
        self.utils.get_request_json.return_value = self.DESTINATION_DATA_WITHOUT_LETTER
        self.assertRaises(BadDestinationError, self.base_station_api.receive_destination)

    def test_api_should_return_success_message_after_successful_destination_update(self):
        self.utils.get_request_json.return_value = self.DESTINATION_DATA
        self.utils.to_json.return_value = self.RESPONSE_MESSAGE

        self.base_station_api.receive_destination()

        self.flask_app.make_response.assert_called_once_with((self.RESPONSE_MESSAGE, self.SUCCESS_CODE))

    def test_api_should_raise_NotJSONException_for_voltage_update_if_request_data_is_not_valid(self):
        self.utils.get_request_json.return_value = self.INVALID_DATA
        self.assertRaises(NotJSONException, self.base_station_api.receive_voltage)

    def test_api_should_raise_BadVoltageError_for_voltage_update_if_voltage_is_missing(self):
        self.utils.get_request_json.return_value = self.INVALID_VOLTAGE_DATA
        self.assertRaises(BadVoltageError, self.base_station_api.receive_voltage)

    def test_api_should_return_success_message_after_successful_voltage_update(self):
        self.utils.get_request_json.return_value = self.VOLTAGE_DATA
        self.utils.to_json.return_value = self.RESPONSE_MESSAGE

        self.base_station_api.receive_voltage()

        self.flask_app.make_response.assert_called_once_with((self.RESPONSE_MESSAGE, self.SUCCESS_CODE))

    def test_api_should_raise_NotJSONException_for_trajectory_update_if_request_data_is_not_valid(self):
        self.utils.get_request_json.return_value = self.INVALID_DATA
        self.assertRaises(NotJSONException, self.base_station_api.receive_trajectory)

    def test_api_should_raise_BadTrajectoryError_for_trajectory_update_if_trajectory_is_missing(self):
        self.utils.get_request_json.return_value = self.INVALID_TRAJECTORY_DATA
        self.assertRaises(BadTrajectoryError, self.base_station_api.receive_trajectory)

    def test_api_should_return_success_message_after_successful_trajectory_update(self):
        self.utils.get_request_json.return_value = self.TRAJECTORY_DATA

        self.utils.to_json.return_value = self.RESPONSE_MESSAGE

        self.base_station_api.receive_trajectory()

        self.flask_app.make_response.assert_called_once_with((self.RESPONSE_MESSAGE, self.SUCCESS_CODE))

    def test_api_should_raise_NotJSONException_for_log_if_request_data_is_not_valid(self):
        self.utils.get_request_json.return_value = self.INVALID_DATA
        self.assertRaises(NotJSONException, self.base_station_api.receive_log)

    def test_api_should_raise_BadLogError_when_log_is_missing_when_receiving_a_log(self):
        self.utils.get_request_json.return_value = self.INVALID_LOG_DATA
        self.assertRaises(BadLogError, self.base_station_api.receive_log)

    def test_api_should_return_success_message_after_successful_log_request(self):
        self.utils.get_request_json.return_value = self.LOG_DATA

        self.utils.to_json.return_value = self.RESPONSE_MESSAGE

        self.base_station_api.receive_log()

        self.flask_app.make_response.assert_called_once_with((self.RESPONSE_MESSAGE, self.SUCCESS_CODE))

    def test_api_should_raise_NotJSONException_while_receiving_treasures_if_request_data_is_not_valid(self):
        self.utils.get_request_json.return_value = self.INVALID_DATA
        self.assertRaises(NotJSONException, self.base_station_api.receive_treasures)

    def test_api_should_raise_BadTreasuresError_if_treasures_are_missing_while_receiving_treasures(self):
        self.utils.get_request_json.return_value = self.INVALID_TREASURE_DATA
        self.assertRaises(BadTreasuresError, self.base_station_api.receive_treasures)

    def test_api_should_return_success_message_after_successfully_receiving_treasures(self):
        self.utils.get_request_json.return_value = self.TREASURE_DATA

        self.utils.to_json.return_value = self.RESPONSE_MESSAGE

        self.base_station_api.receive_treasures()

        self.flask_app.make_response.assert_called_once_with((self.RESPONSE_MESSAGE, self.SUCCESS_CODE))
