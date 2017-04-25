from robot.ai.pathfinding.pathfinding_strategy import PathFindingStrategy


class DijkstraPathFindingStrategy(PathFindingStrategy):
    __map = None

    def __init__(self, dijkstra_path_finding_map):
        self.__map = dijkstra_path_finding_map

    def calculate_path(self, robot_position, objective_type):
        return self.__map.calculate_dijkstra_path(robot_position, objective_type)
