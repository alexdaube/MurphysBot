import unittest

from mock import Mock

from robot.vision.robot_vision import RobotVision


class TestRobotVision(unittest.TestCase):
    def setUp(self):
        self.island_detector = Mock()
        self.treasure_detector = Mock()
        self.charge_station_detector = Mock()
        self.camera = Mock()
        self.vision = RobotVision(self.island_detector, self.treasure_detector,
                                  self.charge_station_detector, self.camera)

    def test_can_get_average_point(self):
        points = [[1, 3], [5, 3], [12, 0]]
        average_point = self.vision.get_average_point(points)
        self.assertListEqual([6, 2], average_point)

    def test_can_get_treasures(self):
        picture = Mock()
        self.camera.get_current_frame.return_value = picture
        self.treasure_detector.detect_treasures.return_value = [[[1, 3], [5, 3], [12, 0]]]

        result_treasures, result_picture = self.vision.detect_treasures()

        self.assertEquals(picture, result_picture)
        self.assertListEqual([[[1, 3], [5, 3], [12, 0]]], result_treasures)

    def test_can_get_treasures_with_average_point(self):
        picture = Mock()
        self.camera.get_current_frame.return_value = picture
        self.treasure_detector.detect_treasures.return_value = [[[1, 3], [5, 3], [12, 0]]]

        result_treasures, result_picture = self.vision.detect_treasures(True)

        self.assertEquals(picture, result_picture)
        self.assertListEqual([[6, 2]], result_treasures)
