from werkzeug import exceptions

from common.communication.base_api import BaseAPI, NotJSONException
from common.communication.flask_utils_wrapper import FlaskUtilsWrapper


class BadVoltageError(exceptions.HTTPException):
    message = 'Must have voltage value'
    code = 455
    name = "Bad Robot Coordinate Error"


class BadDestinationError(exceptions.HTTPException):
    message = 'The destination must contain the letter and description value'
    code = 455
    name = "Bad Destination Error"


class BadTrajectoryError(exceptions.HTTPException):
    message = 'Must have a trajectory value'
    code = 455
    name = "Bad Trajectory Error"


class BadTreasuresError(exceptions.HTTPException):
    message = 'Must have a treasure value'
    code = 455
    name = "Bad Treasure Error"


class BadLogError(exceptions.HTTPException):
    message = 'Must have a log value'
    code = 455
    name = "Bad Log Error"


class BaseStationAPI(BaseAPI):
    DESTINATION_SUCCESS_MESSAGE = {"success": "The destination has been properly received!"}
    VOLTAGE_SUCCESS_MESSAGE = {'success': 'The voltage has been properly received!'}
    TRAJECTORY_SUCCESS_MESSAGE = {'success': 'The trajectory has been properly received!'}

    def __init__(self, api_app, values, utils=FlaskUtilsWrapper()):
        super(BaseStationAPI, self).__init__(api_app, utils)
        self._define_routes()
        self.received_values = values

    def receive_destination(self):
        request_json = self.utils.get_request_json()
        if not request_json:
            raise NotJSONException("While receiving destination...")
        if 'letter' not in request_json or 'description' not in request_json:
            raise BadDestinationError
        self.received_values['letter'] = request_json['letter']
        self.received_values['description'] = request_json['description']
        self.app.logger.info(self.DESTINATION_SUCCESS_MESSAGE["success"])
        return self._make_response(self.DESTINATION_SUCCESS_MESSAGE, 200)

    def receive_voltage(self):
        request_json = self.utils.get_request_json()
        if not request_json:
            raise NotJSONException("While receiving voltage...")
        if 'voltage' not in request_json:
            raise BadVoltageError
        self.received_values['voltage'] = request_json['voltage']
        self.app.logger.info(self.VOLTAGE_SUCCESS_MESSAGE["success"])
        return self._make_response(self.VOLTAGE_SUCCESS_MESSAGE, 200)

    def receive_trajectory(self):
        request_json = self.utils.get_request_json()
        if not request_json:
            raise NotJSONException("While receiving trajectory...")
        if 'trajectory' not in request_json:
            raise BadTrajectoryError
        self.received_values['trajectory'] = request_json['trajectory']
        self.app.logger.info(self.TRAJECTORY_SUCCESS_MESSAGE["success"])
        return self._make_response(self.TRAJECTORY_SUCCESS_MESSAGE, 200)

    def receive_treasures(self):
        request_json = self.utils.get_request_json()
        if not request_json:
            raise NotJSONException("While receiving treasures...")
        if 'treasures' not in request_json:
            raise BadTreasuresError
        self.received_values['treasures'] = request_json['treasures']
        self.app.logger.info(self.TRAJECTORY_SUCCESS_MESSAGE["success"])
        return self._make_response(self.TRAJECTORY_SUCCESS_MESSAGE, 200)

    def receive_log(self):
        request_json = self.utils.get_request_json()
        if not request_json:
            raise NotJSONException("While receiving log...")
        if 'log' not in request_json:
            raise BadLogError
        data = request_json['log']
        self.app.logger.log(data[0], data[1])
        return self._make_response({}, 200)

    def _define_routes(self):
        self.app.add_url_rule('/destination', 'receive_destination', self.receive_destination, methods=['PUT'])
        self.app.add_url_rule('/voltage', 'receive_voltage', self.receive_voltage, methods=['PUT'])
        self.app.add_url_rule('/trajectory', 'receive_trajectory', self.receive_trajectory, methods=['PUT'])
        self.app.add_url_rule('/treasures', 'receive_treasures', self.receive_treasures, methods=['PUT'])
        self.app.add_url_rule('/log', 'receive_log', self.receive_log, methods=['POST'])


if __name__ == '__main__':
    pass
