import unittest

from common.communication.base_client import BaseClient


class TestBaseClient(unittest.TestCase):
    ADDRESS = "127.0.0.1"
    PORT = 80
    RELATIVE_PATH = "relative"
    URL_WITH_PATH = "http://127.0.0.1:80/relative"
    URL_WITHOUT_PATH = "http://127.0.0.1:80/"

    def setUp(self):
        self.client = BaseClient()

    def test_a_url_should_be_formed_of_base_url_and_relative_path(self):
        self.assertEqual(self.client._url(self.ADDRESS, self.PORT, self.RELATIVE_PATH),
                         self.URL_WITH_PATH)

    def test_a_base_url_is_provided_when_relative_path_is_omitted(self):
        self.assertEqual(self.client._url(self.ADDRESS, self.PORT), self.URL_WITHOUT_PATH)
