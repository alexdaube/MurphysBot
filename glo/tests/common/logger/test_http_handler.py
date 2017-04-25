import logging
import unittest

from mock.mock import Mock, ANY
from testfixtures import LogCapture

from common.logger.http_handler import HttpHandler


class HttpHandlerTest(unittest.TestCase):
    MESSAGE = 'message'

    def setUp(self):
        self.client = Mock()
        self.handler = HttpHandler(self.client)
        self.capture = LogCapture(names="test")
        logging.getLogger("test").info(self.MESSAGE)

    def tearDown(self):
        self.capture.uninstall()

    def test_sends_logs_to_remote_server(self):
        record = self.capture.records[-1]
        self.handler.emit(record)
        self.client.send_log.assert_called_once_with(ANY)
