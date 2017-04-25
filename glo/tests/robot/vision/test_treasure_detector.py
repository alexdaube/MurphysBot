import unittest

from mock import Mock

from robot.vision.treasure_detector import TreasureDetector


class TestTreasureDetector(unittest.TestCase):
    def setUp(self):
        self.strategy = Mock()
        self.detector = TreasureDetector(self.strategy)

    def test_can_detect_treasures(self):
        picture = Mock()
        picture.__len__ = Mock(return_value=16)
        self.strategy.detect.return_value = [
            [[0, 1], [2, 1], [1, 3], [1, 0]],
            [[10, 10], [10, 12], [12, 10], [12, 12]]
        ]

        result = self.detector.detect_treasures(picture, False)

        self.assertListEqual([[[0, 1], [2, 1], [1, 3], [1, 0]], [[10, 10], [10, 12], [12, 10], [12, 12]]], result)
