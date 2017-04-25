import unittest

from basestation.vision.world_number_of_sides_island_strategy import WorldNumberOfSidesIslandStrategy
from tests.basestation.vision.island_detection_strategy_tester import IslandDetectionStrategyTester


class TestNumberOfSidesStrategy(unittest.TestCase):
    strategy = WorldNumberOfSidesIslandStrategy()

    def test_databank_tests(self):
        tester = IslandDetectionStrategyTester(self.strategy)
        tester.test(self)
