from abc import ABCMeta, abstractmethod


class PathFindingStrategy(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def calculate_path(self, robot_position, objective_type):
        pass
