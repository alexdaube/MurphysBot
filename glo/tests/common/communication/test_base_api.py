import unittest

from mock.mock import Mock, MagicMock, patch

from common.communication.base_api import BaseAPI


class TestBaseAPI(unittest.TestCase):
    HOST = "0.0.0.0"
    PORT = 5000
    HANDLER = {None: {404: None, 400: None}}
    MESSAGE = {}
    NOT_FOUND_ERROR_CODE = 404
    BAD_REQUEST_ERROR_CODE = 400
    NOT_JSON_ERROR_CODE = 455
    SHUTDOWN_URL = "http://0.0.0.0:5000/shutdown"

    def __get_handler(self, accessor):
        return self.HANDLER[accessor]

    def __set_handler(self, accessor, val):
        self.HANDLER[accessor] = val

    def setUp(self):
        self.api_app = Mock()
        self.api_utils = Mock()
        self.error = Mock()
        self.api_app.error_handler_spec = MagicMock(spec_set=dict)
        self.api_app.error_handler_spec.__getitem__.side_effect = self.__get_handler
        self.api_app.error_handler_spec.__setitem__.side_effect = self.__set_handler
        self.api = BaseAPI(self.api_app, self.api_utils)
        self.api.HOST = self.HOST
        self.api.PORT = self.PORT

    def test_starting_api_server(self):
        self.api.run()
        self.api_app.run.assert_called_once_with(self.HOST, self.PORT)

    @patch('requests.post')
    def test_stopping_api_server(self, mock_post):
        self.api.stop()
        mock_post.assert_called_once_with(self.SHUTDOWN_URL, timeout=1)

    def test_define_routes_should_be_abstract(self):
        self.assertRaises(NotImplementedError, self.api._define_routes)

    def test_bad_request_returns_an_error_message_with_proper_400_status_code(self):
        self.api_utils.to_json.return_value = self.MESSAGE
        self.api._bad_request(self.error)
        self.api_app.make_response.assert_called_once_with((self.MESSAGE, self.BAD_REQUEST_ERROR_CODE))

    def test_not_found_returns_an_error_message_with_proper_404_status_code(self):
        self.api_utils.to_json.return_value = self.MESSAGE
        self.api._not_found(self.error)
        self.api_app.make_response.assert_called_once_with((self.MESSAGE, self.NOT_FOUND_ERROR_CODE))

    def test_bad_json_returns_an_error_message_with_custom_455_status_code(self):
        self.api_utils.to_json.return_value = self.MESSAGE
        self.api._custom_error(self.error)
        self.api_app.make_response.assert_called_once_with((self.MESSAGE, self.NOT_JSON_ERROR_CODE))
