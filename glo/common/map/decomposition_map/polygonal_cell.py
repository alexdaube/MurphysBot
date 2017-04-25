from shapely.geometry import Polygon, Point


class PolygonalCell(object):
    polygon = None

    def __init__(self, list_of_corners):
        polygon_points = []
        for corner in list_of_corners:
            polygon_points.append((corner.X, corner.Y))
        self.polygon = Polygon(polygon_points)

    def contain_position_inside_cell(self, position):
        point = Point(position.X, position.Y)
        return self.polygon.contains(point)
