import math

import numpy as np

from common.map.point_of_interest.point_of_interest_type import PointOfInterestType
from common.vision.shape_type import ShapeType


class IslandHandler(object):
    @staticmethod
    def parse_shape(shape, color, POIColor):
        if len(shape) == 3:
            return {"color": color, "type": ShapeType.Triangle, "points": shape.squeeze(axis=1).tolist(),
                    "POIType": PointOfInterestType.TRIANGLE_ISLAND, "POIColor": POIColor}
        elif len(shape) == 4:
            return {"color": color, "type": ShapeType.Square, "points": shape.squeeze(axis=1).tolist(),
                    "POIType": PointOfInterestType.SQUARE_ISLAND, "POIColor": POIColor}
        elif len(shape) == 5:
            return {"color": color, "type": ShapeType.Pentagon, "points": shape.squeeze(axis=1).tolist(),
                    "POIType": PointOfInterestType.PENTAGON_ISLAND, "POIColor": POIColor}
        elif len(shape) > 5:
            averagey = (shape.max(axis=0)[0][1] + shape.min(axis=0)[0][1]) / 2
            minx = shape.min(axis=0)[0][0]
            maxx = shape.max(axis=0)[0][0]
            return {"color": color,
                    "type": ShapeType.Circle,
                    "points": [[minx, averagey], [maxx, averagey]],
                    "POIType": PointOfInterestType.CIRCLE_ISLAND,
                    "POIColor": POIColor}

    @staticmethod
    def remove_intermediate_points(shape):
        def is_between(a, b, c):
            def distance(a, b):
                return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

            return math.fabs(distance(a, b) + distance(b, c) - distance(a, c)) < math.fabs(distance(a, c) * 0.05)

        if len(shape) > 10:
            return shape
        i = -1
        while i < len(shape) - 1:
            first = shape[i - 1][0]
            second = shape[i][0]
            third = shape[i + 1][0]
            if is_between(first, second, third):
                shape = np.delete(shape, i, axis=0)
            i += 1
        return shape
