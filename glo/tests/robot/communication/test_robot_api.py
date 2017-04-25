import unittest

from mock.mock import Mock, MagicMock

from common.communication.base_api import NotJSONException
from robot.communication import addresses
from robot.communication.robot_api import RobotAPI, BadRobotPositionCoordinate, BadStateListToExecuteError, BadCommand


class TestRobotAPI(unittest.TestCase):
    HANDLER = {None: {404: None, 400: None}}
    VALID_DATA = {"triangle": "north"}
    INVALID_DATA = {}
    RESPONSE_MESSAGE = {}
    EXECUTION_STATES_LIST = {"states": ["FindTreasuresState"]}
    BAD_EXECUTION_STATES_LIST = {"no_state": ["FindTreasuresState"]}
    MISSING_X_POSITION_DATA = {"x": 1}
    MISSING_Y_POSITION_DATA = {"y": 1}
    POSITION_DATA = {"x": 1, "y": 1, "w": 1}
    SUCCESS_CODE = 200
    BASE_STATION_ADDRESS = '0.0.0.0'
    INVALID_COMMAND_DATA = {"some": "data"}
    QUIT_COMMAND = {'command': 'quit'}
    MAGNET_COMMAND = {'command': 'magnet', 'enable': True}
    MAGNET_COMMAND_MISSING_ENABLE = {'command': 'magnet'}
    PREHENSOR_COMMAND = {'command': 'prehensor', 'position': True}
    PREHENSOR_COMMAND_MISSING_POSITION = {'command': 'prehensor'}
    MOVE_CAMERA_COMMAND = {'command': 'move_camera', 'vertical_angle': 30, 'horizontal_angle': 30}
    MOVE_CAMERA_COMMAND_MISSING_VERTICAL_ANGLE = {'command': 'move_camera', 'horizontal_angle': 30}
    MOVE_CAMERA_COMMAND_MISSING_HORIZONTAL_ANGLE = {'command': 'move_camera', 'vertical_angle': 30}
    MOVE_ROBOT_COMMAND = {'command': 'move_robot', 'x': 30, 'y': 30}
    MOVE_ROBOT_COMMAND_MISSING_X = {'command': 'move_robot', 'y': 30}
    MOVE_ROBOT_COMMAND_MISSING_Y = {'command': 'move_robot', 'x': 30}

    def __get_handler(self, accessor):
        return self.HANDLER[accessor]

    def __set_handler(self, accessor, val):
        self.HANDLER[accessor] = val

    def __raise_typeerror(self):
        raise TypeError

    def setUp(self):
        addresses.BASE_STATION_ADDRESS = ""
        self.robot_controller = MagicMock()
        self.flask_app = Mock()
        self.utils = Mock()
        self.flask_app.error_handler_spec = MagicMock(spec_set=dict)
        self.flask_app.error_handler_spec.__getitem__.side_effect = self.__get_handler
        self.flask_app.error_handler_spec.__setitem__.side_effect = self.__set_handler
        self.robot_api = RobotAPI(self.flask_app, self.robot_controller, self.utils)

    def test_robot_should_send_success_message_upon_successful_activation(self):
        self.robot_api.utils.to_json.return_value = self.RESPONSE_MESSAGE
        self.robot_api.utils.get_request_json = self.__raise_typeerror
        self.robot_api.start_robot_execution()
        self.flask_app.make_response.assert_called_once_with((self.RESPONSE_MESSAGE, self.SUCCESS_CODE))

    def test_robot_should_update_base_station_address_upon_activation(self):
        self.assertEqual(addresses.BASE_STATION_ADDRESS, "")
        self.robot_api.utils.get_request_json = self.__raise_typeerror
        self.robot_api.utils.remote_address.return_value = self.BASE_STATION_ADDRESS
        self.robot_api.start_robot_execution()
        self.assertEqual(addresses.BASE_STATION_ADDRESS, self.BASE_STATION_ADDRESS)

    def test_robot_should_call_set_execution_state_on_robot_controller(self):
        self.robot_api.utils.get_request_json.return_value = self.__raise_typeerror
        self.robot_api.utils.remote_address.return_value = self.BASE_STATION_ADDRESS
        self.robot_api.start_robot_execution()
        self.robot_controller.assert_has_calls(self.robot_controller.set_execution_states)

    def test_robot_should_raise_NotJSONException_for_start_robot_if_request_data_not_json(self):
        self.robot_api.utils.get_request_json.return_value = None
        self.robot_api.utils.remote_address.return_value = self.BASE_STATION_ADDRESS
        self.assertRaises(NotJSONException, self.robot_api.start_robot_execution_with_states)

    def test_robot_should_raise_BadStateListToExecuteError_for_start_robot_if_request_data_is_not_valid(self):
        self.robot_api.utils.get_request_json.return_value = self.BAD_EXECUTION_STATES_LIST
        self.robot_api.utils.remote_address.return_value = self.BASE_STATION_ADDRESS
        self.assertRaises(BadStateListToExecuteError, self.robot_api.start_robot_execution_with_states)

    def test_robot_should_call_set_execution_states_on_robot_controller_for_start_robot_if_request_data_valid(self):
        self.robot_api.utils.get_request_json.return_value = self.EXECUTION_STATES_LIST
        self.robot_api.utils.remote_address.return_value = self.BASE_STATION_ADDRESS
        self.robot_api.start_robot_execution()
        self.robot_controller.assert_has_calls(self.robot_controller.set_execution_states)

    def test_robot_should_send_success_message_if_request_data_valid_upon_successful_activation(self):
        self.robot_api.utils.to_json.return_value = self.RESPONSE_MESSAGE
        self.robot_api.utils.get_request_json.return_value = self.EXECUTION_STATES_LIST
        self.robot_api.utils.remote_address.return_value = self.BASE_STATION_ADDRESS
        self.robot_api.start_robot_execution()
        self.flask_app.make_response.assert_called_once_with((self.RESPONSE_MESSAGE, self.SUCCESS_CODE))

    def test_robot_should_raise_NotJSONException_for_island_positions_update_if_request_data_is_not_valid(self):
        self.robot_api.utils.get_request_json.return_value = self.INVALID_DATA
        self.assertRaises(NotJSONException, self.robot_api.receive_island_positions)

    def test_robot_should_initiate_island_positions_update_after_successful_data_validation(self):
        self.robot_api.utils.get_request_json.return_value = self.VALID_DATA
        self.robot_api.utils.to_json(self.VALID_DATA)

        self.robot_api.receive_island_positions()

        self.robot_api.robot_controller.update_island_positions.assert_called_once_with(self.VALID_DATA)

    def test_robot_should_return_success_message_after_successful_island_positions_update(self):
        self.robot_api.utils.get_request_json.return_value = self.VALID_DATA
        self.robot_api.utils.to_json.return_value = self.RESPONSE_MESSAGE

        self.robot_api.receive_island_positions()

        self.flask_app.make_response.assert_called_once_with((self.RESPONSE_MESSAGE, self.SUCCESS_CODE))

    def test_robot_should_raise_NotJSONException_for_robot_position_update_if_request_data_is_not_valid(self):
        self.robot_api.utils.get_request_json.return_value = self.INVALID_DATA
        self.assertRaises(NotJSONException, self.robot_api.receive_robot_position)

    def test_robot_should_raise_BadRobotPositionCoordinate_for_robot_position_update_if_x_position_is_missing(self):
        self.robot_api.utils.get_request_json.return_value = self.MISSING_X_POSITION_DATA
        self.assertRaises(BadRobotPositionCoordinate, self.robot_api.receive_robot_position)

    def test_robot_should_raise_BadRobotPositionCoordinate_for_robot_position_update_if_y_position_is_missing(self):
        self.robot_api.utils.get_request_json.return_value = self.MISSING_Y_POSITION_DATA
        self.assertRaises(BadRobotPositionCoordinate, self.robot_api.receive_robot_position)

    def test_robot_should_initiate_robot_position_update_after_successful_data_validation(self):
        self.robot_api.utils.get_request_json.return_value = self.POSITION_DATA
        self.robot_api.utils.to_json.return_value = self.POSITION_DATA

        self.robot_api.receive_robot_position()

        self.robot_controller.update_position.assert_called_once_with(self.POSITION_DATA['x'], self.POSITION_DATA['y'],
                                                                      self.POSITION_DATA["w"])

    def test_robot_should_return_success_message_after_successful_robot_position_update(self):
        self.robot_api.utils.get_request_json.return_value = self.POSITION_DATA
        self.robot_api.utils.to_json.return_value = self.RESPONSE_MESSAGE

        self.robot_api.receive_robot_position()

        self.flask_app.make_response.assert_called_once_with((self.RESPONSE_MESSAGE, self.SUCCESS_CODE))

    def test_should_return_NotJSONException_when_no_json_is_received_on_a_command_reception(self):
        self.robot_api.utils.get_request_json.return_value = self.INVALID_DATA
        self.assertRaises(NotJSONException, self.robot_api.receive_command)

    def test_should_raise_BadCommand_if_no_command_is_received(self):
        self.robot_api.utils.get_request_json.return_value = self.INVALID_COMMAND_DATA
        self.assertRaises(BadCommand, self.robot_api.receive_command)

    def test_inject_command_when_the_quit_command_is_received(self):
        self.robot_api.utils.get_request_json.return_value = self.QUIT_COMMAND
        self.robot_api.receive_command()
        self.robot_controller.inject_command.assert_called_once_with(self.QUIT_COMMAND)

    # MAGNET_COMMAND_MISSING_ENABLE = {'command': 'magnet'}
    def test_inject_command_when_the_magnet_command_is_received_and_has_enable_field(self):
        self.robot_api.utils.get_request_json.return_value = self.MAGNET_COMMAND
        self.robot_api.receive_command()
        self.robot_controller.inject_command.assert_called_once_with(self.MAGNET_COMMAND)

    def test_raise_BadCommand_when_the_magnet_command_is_received_without_enable_field(self):
        self.robot_api.utils.get_request_json.return_value = self.MAGNET_COMMAND_MISSING_ENABLE
        self.assertRaises(BadCommand, self.robot_api.receive_command)

    def test_inject_command_when_the_prehensor_command_is_received_and_has_position(self):
        self.robot_api.utils.get_request_json.return_value = self.PREHENSOR_COMMAND
        self.robot_api.receive_command()
        self.robot_controller.inject_command.assert_called_once_with(self.PREHENSOR_COMMAND)

    def test_raise_BadCommand_when_the_prehensor_command_is_received_without_position(self):
        self.robot_api.utils.get_request_json.return_value = self.PREHENSOR_COMMAND_MISSING_POSITION
        self.assertRaises(BadCommand, self.robot_api.receive_command)

    def test_inject_command_when_the_move_camera_command_is_received_and_has_horizontal_and_vertical_angle(self):
        self.robot_api.utils.get_request_json.return_value = self.MOVE_CAMERA_COMMAND
        self.robot_api.receive_command()
        self.robot_controller.inject_command.assert_called_once_with(self.MOVE_CAMERA_COMMAND)

    def test_raise_BadCommand_when_the_move_camera_command_is_received_without_horizontal_angle(self):
        self.robot_api.utils.get_request_json.return_value = self.MOVE_CAMERA_COMMAND_MISSING_HORIZONTAL_ANGLE
        self.assertRaises(BadCommand, self.robot_api.receive_command)

    def test_raise_BadCommand_when_the_move_camera_command_is_received_without_vertical_angle(self):
        self.robot_api.utils.get_request_json.return_value = self.MOVE_CAMERA_COMMAND_MISSING_VERTICAL_ANGLE
        self.assertRaises(BadCommand, self.robot_api.receive_command)

    def test_inject_command_when_the_move_robot_command_is_received_and_has_x_and_y_positions(self):
        self.robot_api.utils.get_request_json.return_value = self.MOVE_ROBOT_COMMAND
        self.robot_api.receive_command()
        self.robot_controller.inject_command.assert_called_once_with(self.MOVE_ROBOT_COMMAND)

    def test_raise_BadCommand_when_the_move_robot_command_is_received_without_x_position(self):
        self.robot_api.utils.get_request_json.return_value = self.MOVE_ROBOT_COMMAND_MISSING_X
        self.assertRaises(BadCommand, self.robot_api.receive_command)

    def test_raise_BadCommand_when_the_move_robot_command_is_received_without_y_position(self):
        self.robot_api.utils.get_request_json.return_value = self.MOVE_ROBOT_COMMAND_MISSING_Y
        self.assertRaises(BadCommand, self.robot_api.receive_command)
