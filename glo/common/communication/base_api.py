from threading import Thread

import requests
from werkzeug import exceptions

from common.communication.flask_utils_wrapper import FlaskUtilsWrapper


class NotJSONException(exceptions.HTTPException):
    name = "Not JSON Exception"
    message = 'Format must be JSON and not empty'
    code = 455

    def __init__(self, error_location=""):
        self.name = "{0} -- {1}".format(self.name, error_location)


class BaseAPI(object):
    HOST = '0.0.0.0'
    PORT = 5000
    CONTENT_TYPE = 'application/json'
    ACCESS_CONTROL_ALLOW_ORIGIN = '*'
    ACCESS_CONTROL_ALLOW_HEADERS = "Origin, X-Requested-With, Content-Type, Accept"
    ACCESS_CONTROL_ALLOW_METHODS = 'GET, POST, PUT, DELETE'
    BAD_REQUEST_ERROR_MESSAGE = {'error': 'Bad request sent'}
    NOT_FOUND_ERROR_MESSAGE = {'error': 'Not Found'}
    NOT_IMPLEMENTED_MESSAGE = "Please implement this method"
    START_THREAD_MESSAGE = "Server is starting on a new thread"
    SERVER_SHUTDOWN_MESSAGE = "Server is gracefully shutting down!"
    WERKZEUG_RUNTIME_MESSAGE = 'Not running with the Werkzeug Server'
    thread = None

    def __init__(self, api_app, flask_utils=FlaskUtilsWrapper()):
        self.app = api_app
        self.utils = flask_utils
        self.__configure_application()

    def run(self, host=None, port=None):
        if host:
            self.HOST = host
        if port:
            self.PORT = port
        self.app.logger.info(self.START_THREAD_MESSAGE)
        self.thread = Thread(target=self.app.run, args=(self.HOST, self.PORT))
        self.thread.start()

    def stop(self):
        self.app.logger.warning(self.SERVER_SHUTDOWN_MESSAGE)
        requests.post('http://{0}:{1}/shutdown'.format(self.HOST, self.PORT), timeout=1)

    def __shutdown_server(self):
        func = self.utils.get_shutdown_function()
        if func is None:
            raise RuntimeError(self.WERKZEUG_RUNTIME_MESSAGE)
        func()

    def __shutdown(self):
        self.__shutdown_server()
        return ''

    def _make_response(self, message_dictionary, status_code):
        message = self.utils.to_json(message_dictionary)
        return self.app.make_response((message, status_code))

    def _bad_request(self, error):
        self.app.logger.error(error)
        return self._make_response(self.BAD_REQUEST_ERROR_MESSAGE, 400)

    def _not_found(self, error):
        self.app.logger.error(error)
        return self._make_response(self.NOT_FOUND_ERROR_MESSAGE, 404)

    def _custom_error(self, error):
        self.app.logger.error(error)
        return self._make_response({'error': error.message}, 455)

    def _after_request(self, data):
        response = self.app.make_response(data)
        response.headers['Content-Type'] = self.CONTENT_TYPE
        response.headers['Access-Control-Allow-Origin'] = self.ACCESS_CONTROL_ALLOW_ORIGIN
        response.headers['Access-Control-Allow-Headers'] = self.ACCESS_CONTROL_ALLOW_HEADERS
        response.headers['Access-Control-Allow-Methods'] = self.ACCESS_CONTROL_ALLOW_METHODS
        return response

    def _define_routes(self):
        raise NotImplementedError(self.NOT_IMPLEMENTED_MESSAGE)

    def __configure_application(self):
        self.__set_error_handlers()
        self.app.after_request(self._after_request)
        self.app.debug = False
        self.app.use_reloader = False
        self.app.add_url_rule('/shutdown', '__shutdown', self.__shutdown, methods=['POST'])

    def __set_error_handlers(self):
        self.app.error_handler_spec[None][404] = self._not_found
        self.app.error_handler_spec[None][400] = self._bad_request
        self.app.error_handler_spec[None][455] = self._custom_error
