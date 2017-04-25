import unittest

import numpy as np

from robot.vision.treasure_detection_by_wall_contrast_strategy import TreasureDetectionByWallContrastStrategy
from tests.robot.vision.treasure_detection_strategy_tester import TreasureDetectionStrategyTester


class TestTreasureContrastStrategy(unittest.TestCase):
    strategy = TreasureDetectionByWallContrastStrategy()

    def test_databank_tests(self):
        tester = TreasureDetectionStrategyTester(self.strategy)
        tester.test(self)

    def test_can_detect_if_shape_is_within_wall(self):
        wall = [make_np_array([0, 0], [0, 200], [200, 200], [200, 0])]
        shape = make_np_array([40, 200], [80, 200], [80, 180], [40, 180])

        self.assertTrue(self.strategy.shape_is_within_wall(wall, shape))

    def test_can_detect_if_shape_is_not_within_wall(self):
        wall = [make_np_array([0, 0], [0, 200], [200, 200], [200, 0])]
        shape = make_np_array([40, 240], [80, 240], [80, 210], [40, 210])

        self.assertFalse(self.strategy.shape_is_within_wall(wall, shape))

    def test_can_remove_duplicate_points(self):
        first_point = [5, 4]
        duplicate_first_point = [4, 5]
        second_point = [5, 22]
        third_point = [22, 4]
        duplicate_third_point = [24, 2]
        points = make_np_array(first_point, duplicate_first_point, second_point, third_point, duplicate_third_point)

        filtered_points = self.strategy.eliminate_identical_points(points.squeeze(axis=1).tolist())

        self.assertListEqual(filtered_points, [first_point, second_point, third_point])


def make_np_array(*kargs):
    return np.array([[item] for item in kargs])
