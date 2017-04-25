from common.map.point_of_interest import point_of_interest
from common.map.point_of_interest.point_of_interest_type import PointOfInterestType
from common.map.position import Position


class Island(point_of_interest.PointOfInterest):
    island_form = None
    island_color = None
    position = None
    security_zone = None

    def __init__(self, form, color, position, security_zone):
        self.island_color = color
        self.island_form = form
        self.position = position
        self.security_zone = security_zone

    def has_point_of_interest_type(self, point_of_interest_type):
        if point_of_interest_type == self.island_color or point_of_interest_type == self.island_form or \
                        point_of_interest_type is PointOfInterestType.ISLAND:
            return True
        else:
            return False

    def get_position(self):
        return self.position

    def get_position_descriptors(self):
        position1 = Position(self.position.X, self.position.Y + self.security_zone)
        position2 = Position(self.position.X + self.security_zone, self.position.Y)
        position3 = Position(self.position.X, self.position.Y - self.security_zone)
        position4 = Position(self.position.X - self.security_zone, self.position.Y)

        return [position1, position2, position3, position4]
