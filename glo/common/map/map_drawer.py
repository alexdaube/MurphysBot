from abc import ABCMeta, abstractmethod


class MapDrawer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def draw_map(self, painter):
        pass
