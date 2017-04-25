import math as math

from common.map.point_of_interest.island import island
from common.map.point_of_interest.point_of_interest_type import PointOfInterestType

CENTER_CALCULUS_CONSTANT = 1 / 6 * math.sqrt(3)


class TriangleIsland(island.Island):
    def __init__(self, color, position, security_zone):
        super(TriangleIsland, self).__init__(PointOfInterestType.TRIANGLE_ISLAND, color, position, security_zone)
