import unittest

from mock.mock import Mock

from robot.ai.pathfinding.dijkstra_pathfinding_strategy import DijkstraPathFindingStrategy


class TestDijkstraPathFindingStrategy(unittest.TestCase):
    dijkstra_pathfinding_strategy = None
    map = None

    def setUp(self):
        self.map = Mock()
        self.dijkstra_pathfinding_strategy = DijkstraPathFindingStrategy(self.map)

    def test_redirect_call_to_the_map(self):
        position = Mock()
        objective = Mock()
        self.dijkstra_pathfinding_strategy.calculate_path(position, objective)
        self.map.calculate_dijkstra_path.assert_called_with(position, objective)
