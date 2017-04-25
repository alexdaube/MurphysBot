# -*- coding: utf-8 -*-

import cv2
import numpy as np

from common.vision.detection_strategy import DetectionStrategy
from common.vision.island_handler import IslandHandler
from common.vision.shape_type import ShapeType


class WorldNumberOfSidesIslandStrategy(DetectionStrategy):
    GAUSSIAN_SIZE = (3, 3)
    APPROXIMATION_TOLERANCE_PERCENTAGE = 0.02
    minimum_wall_length = None
    minimum_shape_size = None
    maximum_shape_size = None
    picture_top = 0
    picture_bottom = None

    def detect(self, picture):
        self.picture_bottom = len(picture)
        self.minimum_shape_size = (len(picture) / 22) ** 2
        self.maximum_shape_size = (len(picture) / 15) ** 2
        self.minimum_wall_length = len(picture) * 2

        # Blur pic, turn to HSV, black out walls
        walls, picture = self.format_picture(picture)

        islands = [{"type": ShapeType.Wall, "color": "", "points": [[0, wall], [len(picture[0]), wall]]}
                   for wall in walls]

        for color in self.islands:

            contours = self.get_contours(picture, self.islands[color]["threshold"])

            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area < self.minimum_shape_size or area > self.maximum_shape_size:
                    continue
                shape = cv2.approxPolyDP(cnt, self.APPROXIMATION_TOLERANCE_PERCENTAGE* cv2.arcLength(cnt, True), True)
                height = float(shape.max(axis=0)[0][1]) - float(shape.min(axis=0)[0][1])
                width = float(shape.max(axis=0)[0][0]) - float(shape.min(axis=0)[0][0])
                if (height / width) < 0.75 or (height / width) > 1.25:
                    continue
                shape = IslandHandler.remove_intermediate_points(shape)
                shape = IslandHandler.parse_shape(shape, color, self.islands[color]["POIColor"])
                if shape is not None:
                    islands.append(shape)

        return islands

    def format_picture(self, picture):
        picture = cv2.GaussianBlur(picture, self.GAUSSIAN_SIZE, 0)
        picture = cv2.cvtColor(picture, cv2.COLOR_BGR2HSV)
        walls = self.get_walls(picture)
        picture[0:walls[0], :] = [0, 0, 0]  # black out top
        picture[walls[1]:, :] = [0, 0, 0]  # black out bottom
        return walls, picture

    def get_walls(self, picture):
        bottom_wall, top_wall = self.picture_bottom, self.picture_top
        contours = [cnt for cnt in self.get_contours(picture, self.wall) if
                    cv2.arcLength(cnt, False) > self.minimum_wall_length]
        for cnt in contours:
            cnt = self.add_intermediate_points_to_contour(cnt, picture)
            cnt = self.filter_middle_of_picture(cnt, picture)
            if len(cnt) == 0:
                continue
            if cnt.max(axis=0).min() < (self.picture_bottom - self.picture_top) / 2:
                top_wall = max(top_wall, cnt.max(axis=0).min())
            else:
                bottom_wall = min(bottom_wall, cnt.min(axis=0).max())
        return [top_wall, bottom_wall]

    @staticmethod
    def add_intermediate_points_to_contour(contour, picture):
        max_x_distance = len(picture[0]) / 10
        i = 0
        while i < len(contour) - 1:
            if contour[i][0][0] + max_x_distance < contour[i + 1][0][0]:
                contour = np.insert(contour, i + 1, [[contour[i][0][0] + max_x_distance, contour[i][0][1]]], 0)
            else:
                i += 1
        return contour

    @staticmethod
    def filter_middle_of_picture(contour, picture):
        width = len(picture[0])
        return np.array([val for val in contour if width * 4 / 10 < val[0][0] < width * 6 / 10])
