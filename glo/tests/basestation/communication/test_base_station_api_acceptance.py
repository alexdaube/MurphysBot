import json
import unittest

from flask import Flask

from basestation.communication.base_station_api import BaseStationAPI


class TestBaseStationAPIAcceptance(unittest.TestCase):
    DESTINATION_PATH = '/destination'
    VOLTAGE_PATH = '/voltage'
    TRAJECTORY_PATH = '/trajectory'
    INVALID_DATA = {}
    VALID_DATA = {"y": 1}
    SUCCESS_CODE = 200
    CUSTOM_ERROR_CODE = 455
    JSON_CONTENT_TYPE = 'application/json'
    INVALID_TRAJECTORY_DATA = {"some": "data"}
    TRAJECTORY_DATA = {"trajectory": "data"}
    INVALID_VOLTAGE_DATA = {"some": "data"}
    VOLTAGE_DATA = {"voltage": "data"}
    LOG_DATA = {'log': "data"}
    DESTINATION_DATA = {"letter": "data", "description": "data"}
    DESTINATION_DATA_WITHOUT_DESCRIPTION = {"letter": "data"}
    DESTINATION_DATA_WITHOUT_LETTER = {"description": "data"}

    def setUp(self):
        self.app = Flask("BaseStationAPI")
        self.api = BaseStationAPI(self.app, {})
        self.api.app.config['TESTING'] = True
        self.client = self.api.app.test_client()

    def test_receives_and_updates_destination(self):
        response = self.client.put(self.DESTINATION_PATH, data=json.dumps(self.DESTINATION_DATA),
                                   content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, self.SUCCESS_CODE)

    def test_let_client_knows_that_the_data_format_should_be_json_upon_destination_update(self):
        response = self.client.put(self.DESTINATION_PATH, data=json.dumps(self.INVALID_DATA),
                                   content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, self.CUSTOM_ERROR_CODE)

    def test_let_client_knows_that_the_data_format_should_include_description_and_letter_upon_destination_update(self):
        response = self.client.put(self.DESTINATION_PATH, data=json.dumps(self.DESTINATION_DATA_WITHOUT_DESCRIPTION),
                                   content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, self.CUSTOM_ERROR_CODE)

    def test_receives_and_updates_voltage(self):
        response = self.client.put(self.VOLTAGE_PATH, data=json.dumps(self.VOLTAGE_DATA),
                                   content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, self.SUCCESS_CODE)

    def test_let_client_knows_that_the_data_format_should_be_json_upon_voltage_update(self):
        response = self.client.put(self.VOLTAGE_PATH, data=json.dumps(self.INVALID_DATA),
                                   content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, self.CUSTOM_ERROR_CODE)

    def test_let_client_knows_that_the_data_format_should_include_voltage_upon_voltage_update(self):
        response = self.client.put(self.DESTINATION_PATH, data=json.dumps(self.INVALID_VOLTAGE_DATA),
                                   content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, self.CUSTOM_ERROR_CODE)

    def test_receives_and_updates_trajectory(self):
        response = self.client.put(self.TRAJECTORY_PATH, data=json.dumps(self.TRAJECTORY_DATA),
                                   content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, self.SUCCESS_CODE)

    def test_let_client_knows_that_the_data_format_should_be_json_upon_trajectory_update(self):
        response = self.client.put(self.TRAJECTORY_PATH, data=json.dumps(self.INVALID_DATA),
                                   content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, self.CUSTOM_ERROR_CODE)

    def test_let_client_knows_that_the_data_format_should_include_trajectory_upon_trajectory_update(self):
        response = self.client.put(self.DESTINATION_PATH, data=json.dumps(self.INVALID_TRAJECTORY_DATA),
                                   content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, self.CUSTOM_ERROR_CODE)


if __name__ == '__main__':
    unittest.main()
