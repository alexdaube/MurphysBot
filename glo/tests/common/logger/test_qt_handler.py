import logging
import unittest

from mock.mock import Mock, ANY
from testfixtures import LogCapture

from common.logger.qt_handler import QtHandler


class QtHandlerTest(unittest.TestCase):
    MESSAGE = 'message'

    def setUp(self):
        self.queue = Mock()
        self.handler = QtHandler(self.queue)
        self.capture = LogCapture(names="test")
        logging.getLogger("test").info(self.MESSAGE)

    def tearDown(self):
        self.capture.uninstall()

    def test_put_log_message_in_qt_message_queue(self):
        record = self.capture.records[-1]
        self.handler.emit(record)
        self.queue.put.assert_called_once_with(ANY)
