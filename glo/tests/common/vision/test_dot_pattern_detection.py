import unittest

import cv2
import yaml

from common.vision.dot_pattern_detection_strategy import DotPatternDetectionStrategy


class TestDotPatternDetection(unittest.TestCase):
    def test_it_detects_robot_pose_in_real_world_images(self):
        self._prepare_detection_with_colors_for_real_world_image()
        image = cv2.imread('./data/world_pictures/robot/6pm/world_0.png')
        expected_x = 1315
        expected_y = 478
        expected_orientation = 259.6
        tolerance = 1

        robot = self.detection.detect(image)

        self.assertTrue(expected_x - tolerance <= robot['x'] <= expected_x + tolerance)
        self.assertTrue(expected_y - tolerance <= robot['y'] <= expected_y + tolerance)
        self.assertTrue(expected_orientation - tolerance <= robot['w'] <= expected_orientation + tolerance)

    def _prepare_detection_with_colors_for_real_world_image(self):
        f = open('./tests/data/dot_pattern.yml')
        dot_pattern = yaml.safe_load(f)
        f.close()
        f = open('./tests/data/world_colors.yml')
        dot_colors = yaml.safe_load(f)
        f.close()
        self.detection = DotPatternDetectionStrategy(dot_pattern, dot_colors)
