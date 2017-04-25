import json
import unittest

from flask import Flask
from mock import Mock

from robot.communication.robot_api import RobotAPI


class TestRobotAPIAcceptance(unittest.TestCase):
    START_ROBOT_PATH = '/start_robot'
    ISLAND_POSITIONS_PATH = '/island_positions'
    ROBOT_POSITION_PATH = '/robot_position'
    START_ROBOT_WITH_EXECUTION_STATES_PATH = '/start_robot_with_execution_states'
    INVALID_DATA = {}
    EXECUTION_STATES_LIST = {"states": ["FindTreasuresState"]}
    INVALID_EXECUTION_STATES_LIST = {"nostates": ["FindTreasuresState"]}
    MISSING_X_POSITION_DATA = {"y": 1}
    MISSING_Y_POSITION_DATA = {"x": 1}
    POSITION_DATA = {"x": 1, "y": 1, "w": 1}
    SUCCESS_CODE = 200
    CUSTOM_ERROR_CODE = 455
    JSON_CONTENT_TYPE = 'application/json'

    def setUp(self):
        self.app = Flask("RobotAPI")
        self.controller = Mock()
        self.api = RobotAPI(self.app, self.controller)
        self.api.app.config['TESTING'] = True
        self.client = self.api.app.test_client()

    def test_start_robot_execution(self):
        response = self.client.post(self.START_ROBOT_PATH)
        self.assertEqual(response.status_code, self.SUCCESS_CODE)

    def test_start_robot_execution_with_state_list(self):
        response = self.client.put(self.START_ROBOT_WITH_EXECUTION_STATES_PATH,
                                   data=json.dumps(self.EXECUTION_STATES_LIST),
                                   content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, self.SUCCESS_CODE)

    def test_let_client_knows_that_the_data_format_should_be_json_upon_robot_execution_with_state_list(self):
        response = self.client.put(self.START_ROBOT_WITH_EXECUTION_STATES_PATH,
                                   data=json.dumps(self.INVALID_DATA),
                                   content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, self.CUSTOM_ERROR_CODE)

    def test_let_client_knows_that_the_data_format_should_include_a_state_upon_robot_execution_with_state_list(self):
        response = self.client.put(self.START_ROBOT_WITH_EXECUTION_STATES_PATH,
                                   data=json.dumps(self.INVALID_EXECUTION_STATES_LIST),
                                   content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, self.CUSTOM_ERROR_CODE)

    def test_receives_and_updates_island_positions(self):
        response = self.client.put(self.ISLAND_POSITIONS_PATH, data=json.dumps(self.POSITION_DATA),
                                   content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, self.SUCCESS_CODE)

    def test_let_client_knows_that_the_data_format_should_be_json_upon_island_positions_update(self):
        response = self.client.put(self.ISLAND_POSITIONS_PATH, data=json.dumps(self.INVALID_DATA),
                                   content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, self.CUSTOM_ERROR_CODE)

    def test_receives_and_updates_robot_position(self):
        response = self.client.put(self.ROBOT_POSITION_PATH, data=json.dumps(self.POSITION_DATA),
                                   content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, self.SUCCESS_CODE)

    def test_let_client_knows_that_the_data_format_should_be_json_upon_robot_position_update(self):
        response = self.client.put(self.ROBOT_POSITION_PATH, data=json.dumps(self.INVALID_DATA),
                                   content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, self.CUSTOM_ERROR_CODE)

    def test_let_client_knows_that_the_data_format_should_include_an_x_coordinate_upon_robot_position_update(self):
        response = self.client.put(self.ROBOT_POSITION_PATH, data=json.dumps(self.MISSING_X_POSITION_DATA),
                                   content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, self.CUSTOM_ERROR_CODE)

    def test_let_client_knows_that_the_data_format_should_include_an_y_coordinate_upon_robot_position_update(self):
        response = self.client.put(self.ROBOT_POSITION_PATH, data=json.dumps(self.MISSING_Y_POSITION_DATA),
                                   content_type=self.JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, self.CUSTOM_ERROR_CODE)


if __name__ == '__main__':
    unittest.main()
