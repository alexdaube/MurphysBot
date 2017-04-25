from werkzeug import exceptions

import addresses
from common.communication.base_api import BaseAPI, NotJSONException
from common.communication.flask_utils_wrapper import FlaskUtilsWrapper
from robot.ai.state.move_to_charge_station_state import MoveToChargeStationState
from robot.ai.state.stopped_state import StoppedState
from robot.ai.string_to_state_type import string_to_state_type


class BadRobotPositionCoordinate(exceptions.HTTPException):
    message = 'The position must have an x, y and w value'
    code = 455
    name = "Bad Robot Coordinate Error"


class BadStateListToExecuteError(exceptions.HTTPException):
    message = 'The state to execute must have an state value'
    code = 455
    name = "Bad State To Execute Error"


class BadCommand(exceptions.HTTPException):
    message = 'The state to execute must have an state value'
    code = 455
    name = "Bad command"


class RobotAPI(BaseAPI):
    ROBOT_ACTIVATION_SUCCESS_MESSAGE = {"success": "The robot has started it's execution!"}
    ISLAND_POSITIONS_UPDATE_SUCCESS_MESSAGE = {"success": "The island positions have been updated!"}
    ROBOT_POSITION_UPDATE_SUCCESS_MESSAGE = {"success": "The robot position has been updated!"}

    def __init__(self, api_app, controller, utils=FlaskUtilsWrapper()):
        super(RobotAPI, self).__init__(api_app, utils)
        self.robot_controller = controller
        self._define_routes()

    def start_robot_execution(self):
        addresses.BASE_STATION_ADDRESS = self.utils.remote_address()
        self.app.logger.debug("The base station address is : {0}".format(addresses.BASE_STATION_ADDRESS))
        self.robot_controller.set_state(MoveToChargeStationState)
        self.robot_controller.activate()
        self.app.logger.info(self.ROBOT_ACTIVATION_SUCCESS_MESSAGE["success"])

        return self.app.make_response((self.utils.to_json(self.ROBOT_ACTIVATION_SUCCESS_MESSAGE), 200))

    def start_robot_execution_with_states(self):
        addresses.BASE_STATION_ADDRESS = self.utils.remote_address()
        self.app.logger.debug("The base station address is : {0}".format(addresses.BASE_STATION_ADDRESS))
        self.__set_execution_state()
        self.robot_controller.activate()
        self.app.logger.info(self.ROBOT_ACTIVATION_SUCCESS_MESSAGE["success"])
        return self.app.make_response((self.utils.to_json(self.ROBOT_ACTIVATION_SUCCESS_MESSAGE), 200))

    def __set_execution_state(self):
        request_json = self.utils.get_request_json()
        if not request_json:
            raise NotJSONException("While setting Execution State...")
        else:
            if 'states' not in request_json:
                raise BadStateListToExecuteError
            state_list = list()
            for state in request_json['states']:
                state_list.append(string_to_state_type(state))
            state_list.append(StoppedState)
            first_state = state_list[0]
            self.robot_controller.set_execution_states(state_list)
        self.robot_controller.set_state(first_state)

    def receive_island_positions(self):
        request_json = self.utils.get_request_json()
        if not request_json:
            raise NotJSONException("While receiving island positions...")
        self.robot_controller.update_island_positions(request_json)
        self.app.logger.info(self.ISLAND_POSITIONS_UPDATE_SUCCESS_MESSAGE["success"])
        return self._make_response(self.ISLAND_POSITIONS_UPDATE_SUCCESS_MESSAGE, 200)

    def receive_robot_position(self):
        request_json = self.utils.get_request_json()
        if not request_json:
            raise NotJSONException("While receiving robot position...")
        if 'x' not in request_json or 'y' not in request_json or 'w' not in request_json:
            raise BadRobotPositionCoordinate
        self.robot_controller.update_position(request_json['x'], request_json['y'], request_json['w'])
        self.app.logger.info(self.ROBOT_POSITION_UPDATE_SUCCESS_MESSAGE["success"])
        return self._make_response(self.ROBOT_POSITION_UPDATE_SUCCESS_MESSAGE, 200)

    def receive_command(self):
        request_json = self.utils.get_request_json()
        if not request_json:
            raise NotJSONException("While receiving commands...")
        if 'command' not in request_json:
            raise BadCommand
        if request_json['command'] == "quit":
            self.robot_controller.inject_command(request_json)
        elif request_json['command'] == "magnet":
            if 'enable' not in request_json:
                raise BadCommand
            self.robot_controller.inject_command(request_json)
        elif request_json['command'] == "prehensor":
            if 'position' not in request_json:
                raise BadCommand
            self.robot_controller.inject_command(request_json)
        elif request_json['command'] == "move_camera":
            if 'vertical_angle' not in request_json or 'horizontal_angle' not in request_json:
                raise BadCommand
            self.robot_controller.inject_command(request_json)
        elif request_json['command'] == "move_robot":
            if 'x' not in request_json or 'y' not in request_json:
                raise BadCommand
            self.robot_controller.inject_command(request_json)
        else:
            raise BadCommand

    def _define_routes(self):
        self.app.add_url_rule('/start_robot', 'start_robot_execution', self.start_robot_execution, methods=['POST'])
        self.app.add_url_rule('/start_robot_with_execution_states', 'start_robot_execution_with_states',
                              self.start_robot_execution_with_states,
                              methods=['PUT'])
        self.app.add_url_rule('/island_positions', 'receive_island_positions', self.receive_island_positions,
                              methods=['PUT'])
        self.app.add_url_rule('/robot_position', 'receive_robot_position', self.receive_robot_position, methods=['PUT'])
        self.app.add_url_rule('/send_command', 'receive_command', self.receive_command, methods=['PUT'])


if __name__ == '__main__':
    pass
