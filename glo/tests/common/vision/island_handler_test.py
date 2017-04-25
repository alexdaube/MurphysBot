import unittest

from common.vision.island_handler import IslandHandler


class TestIslandHandler(unittest.TestCase):
    def test_can_remove_intermediate_points(self):
        first_point = [[3, 3]]
        duplicate_point = [[3, 3]]
        second_point = [[69, 69]]
        between_point = [[200, 69]]
        third_point = [[300, 69]]
        shape = [first_point, duplicate_point, second_point, between_point, third_point]

        filtered_shape = IslandHandler.remove_intermediate_points(shape)

        self.assertListEqual(filtered_shape.tolist(), [first_point, second_point, third_point])
