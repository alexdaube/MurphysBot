from common import constants
from common.map.point_of_interest.island.circle_island import CircleIsland
from common.map.point_of_interest.island.pentagon_island import PentagonIsland
from common.map.point_of_interest.island.square_island import SquareIsland
from common.map.point_of_interest.island.triangle_island import TriangleIsland
from common.map.point_of_interest.island.undefine_island_type_error import UndefineIslandTypeError
from common.map.point_of_interest.point_of_interest_type import PointOfInterestType


class IslandFactory:
    @staticmethod
    def create_island(island_type, island_color, island_position,
                      security_zone=constants.OBSTACLE_RADIUS_ADJUSTMENT):
        if island_type == PointOfInterestType.CIRCLE_ISLAND:
            return CircleIsland(island_color, island_position, security_zone)
        if island_type == PointOfInterestType.TRIANGLE_ISLAND:
            return TriangleIsland(island_color, island_position, security_zone)
        if island_type == PointOfInterestType.SQUARE_ISLAND:
            return SquareIsland(island_color, island_position, security_zone)
        if island_type == PointOfInterestType.PENTAGON_ISLAND:
            return PentagonIsland(island_color, island_position, security_zone)
        else:
            raise UndefineIslandTypeError()
