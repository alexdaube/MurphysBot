from abc import ABCMeta, abstractmethod


class Map(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def add_treasure(self, treasure):
        pass

    @abstractmethod
    def add_recharge_station(self, recharge_station):
        pass

    @abstractmethod
    def add_island(self, island):
        pass
