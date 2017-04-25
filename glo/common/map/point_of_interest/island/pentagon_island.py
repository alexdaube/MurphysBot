from common.map.point_of_interest.island import island

from common.map.point_of_interest.point_of_interest_type import PointOfInterestType


class PentagonIsland(island.Island):
    def __init__(self, color, position, security_zone):
        super(PentagonIsland, self).__init__(PointOfInterestType.PENTAGON_ISLAND, color, position, security_zone)
