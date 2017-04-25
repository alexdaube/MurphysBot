from abc import ABCMeta, abstractmethod


class PointOfInterest(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_position(self):
        pass

    @abstractmethod
    def get_position_descriptors(self):
        pass

    @abstractmethod
    def has_point_of_interest_type(self, point_of_interest_type):
        pass
