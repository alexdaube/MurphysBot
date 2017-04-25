from abc import ABCMeta, abstractmethod


class DijkstraPathFindingImplementor(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def calculate_dijkstra_path(self, robot_position, objective_type):
        pass
