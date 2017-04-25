import unittest

from common.logger.dynamic_file_handler import DynamicFileHandler


class DynamicFileHandlerTest(unittest.TestCase):
    DIRECTORY = '/dummy_dir'
    MODE = 'w+'
    LOG_DIRECTORY = '/logs'

    def setUp(self):
        self.handler = DynamicFileHandler(self.DIRECTORY, self.MODE, delay=1)

    def test_puts_log_files_in_the_proper_directory(self):
        path = self.LOG_DIRECTORY + self.DIRECTORY
        assert path in self.handler.baseFilename
