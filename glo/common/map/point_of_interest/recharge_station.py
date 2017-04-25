from common import constants
from common.map.point_of_interest import point_of_interest

from common.map.point_of_interest.point_of_interest_type import PointOfInterestType
from common.map.position import Position


class RechargeStation(point_of_interest.PointOfInterest):
    position = None
    security_zone = None

    def __init__(self, position, security_zone=constants.BORDER_SECURITY_RADIUS):
        self.position = position
        self.security_zone = security_zone

    def has_point_of_interest_type(self, point_of_interest_type):
        if point_of_interest_type == PointOfInterestType.RECHARGE_STATION:
            return True
        else:
            return False

    def get_position(self):
        return self.position

    def get_position_descriptors(self):
        x = self.position.X
        y = self.position.Y
        return [Position(x - self.security_zone, y + self.security_zone),
                Position(x + self.security_zone, y + self.security_zone),
                Position(x + self.security_zone, y - self.security_zone),
                Position(x - self.security_zone, y - self.security_zone)]
