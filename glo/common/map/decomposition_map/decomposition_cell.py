from shapely.geometry.point import Point
from shapely.geometry.polygon import Polygon, LineString

from common.map.position import Position


class DecompositionCell(object):
    top_left = None
    top_right = None
    bottom_right = None
    bottom_left = None

    passed_through = False
    polygon = None

    def __init__(self, top_left, top_right, bottom_right, bottom_left):
        self.top_left = top_left
        self.top_right = top_right
        self.bottom_right = bottom_right
        self.bottom_left = bottom_left
        self.polygon = Polygon([(top_left.X, top_left.Y),
                                (top_right.X, top_right.Y),
                                (bottom_right.X, bottom_right.Y),
                                (bottom_left.X, bottom_left.Y)])

    def contain_position_inside_cell_and_borders(self, position):
        point = Point(position.X, position.Y)
        return self.polygon.contains(point) or self.polygon.intersects(point)

    def contain_position_inside_cell(self, position):
        point = Point(position.X, position.Y)
        return self.polygon.contains(point)

    def contain_position_on_cell_borders(self, position):
        point = Point(position.X, position.Y)
        return self.polygon.intersects(point) and not self.polygon.contains(point)

    def contain_cell(self, cell):
        return self.polygon.contains(cell.polygon)

    def get_cell_center(self):
        return Position(self.polygon.centroid.x, self.polygon.centroid.y)

    def get_two_cell_intersection_center(self, cell):
        intersect = self.polygon.intersection(cell.polygon)
        if type(intersect) is LineString:
            return Position(intersect.centroid.x, intersect.centroid.y)
        else:
            return None

    def calculate_distance_between_cell_center(self, cell):
        return self.get_cell_center().calculate_distance(cell.get_cell_center())

    def is_intersection_a_line(self, position1, position2):
        line = self.__to_line(position1, position2)
        if self.polygon.intersects(line):
            intersection = self.polygon.intersection(line)
            if type(intersection) is LineString:
                return True
        return False

    def get_intersection_line(self, position1, position2):
        line = self.__to_line(position1, position2)
        intersection = self.polygon.intersection(line)
        return Position(intersection.xy[0][0], intersection.xy[1][0]), Position(intersection.xy[0][1],
                                                                                intersection.xy[1][1])

    def is_line_passing_only_on_cell_border(self, position1, position2):
        line = self.__to_line(position1, position2)
        intersection = self.polygon.intersection(line)
        if type(intersection) is LineString or type(intersection) is Point:
            return not self.polygon.contains(intersection)
        else:
            return True

    def is_cell_intersecting_line(self, position1, position2):
        line = self.__to_line(position1, position2)
        return self.polygon.intersects(line)

    def is_cell_intersecting_cell(self, cell):
        if self.polygon.intersects(cell.polygon):
            intersection = self.polygon.intersection(cell.polygon)
            if type(intersection) is LineString or type(intersection) is Polygon:
                return True
        return False

    def is_line_crossing_cell_top_or_bottom(self, position1, position2):
        line = self.__to_line(position1, position2)
        return self.__is_line_crossing_cell_bottom(line) or self.__is_line_crossing_cell_top(line)

    def distance_from_position(self, position):
        point = Point(position.X, position.Y)
        return self.polygon.distance(point)

    def __is_line_crossing_cell_top(self, line):
        top_line = self.__to_line(self.top_left, self.top_right)
        return top_line.intersects(line)

    def __is_line_crossing_cell_bottom(self, line):
        bottom_line = self.__to_line(self.bottom_left, self.bottom_right)
        return bottom_line.intersects(line)

    def is_line_crossing_cell_right(self, position1, position2):
        line = self.__to_line(position1, position2)
        right_line = self.__to_line(self.bottom_right, self.top_right)
        return right_line.intersects(line)

    def is_line_crossing_cell_left(self, position1, position2):
        line = self.__to_line(position1, position2)
        left_line = self.__to_line(self.bottom_left, self.top_left)
        return left_line.intersects(line)

    def __to_line(self, position1, position2):
        return LineString([[position1.X, position1.Y], [position2.X, position2.Y]])

    def reset_pass_through(self):
        self.passed_through = False

    def has_passed_through(self):
        return self.passed_through

    def set_has_passed_through(self):
        self.passed_through = True
