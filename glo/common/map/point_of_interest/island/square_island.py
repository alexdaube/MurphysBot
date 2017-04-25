from common.map.point_of_interest.island import island

from common.map.point_of_interest.point_of_interest_type import PointOfInterestType


class SquareIsland(island.Island):
    def __init__(self, color, position, security_zone):
        super(SquareIsland, self).__init__(PointOfInterestType.SQUARE_ISLAND, color, position, security_zone)
