# -*- coding: utf-8 -*-

from math import fabs

import cv2
import numpy as np

from common.vision.detection_strategy import DetectionStrategy


class TreasureDetectionByWallContrastStrategy(DetectionStrategy):
    APPROX_PERCENT = 0.05
    TREASURE_MIN_SIZE = 10
    GAUSSIAN_SIZE = (3, 3)

    def detect(self, picture, in_wall=True):
        treasures = []
        picture = self.format_picture(picture)
        wall_shapes = self.detect_wall(picture)

        treasure_contours = self.get_contours(picture, self.treasure)
        for cnt in treasure_contours:
            if cv2.contourArea(cnt) < self.TREASURE_MIN_SIZE:
                continue
            treasure_shape = cv2.approxPolyDP(cnt, self.APPROX_PERCENT * cv2.arcLength(cnt, True), True)
            if not in_wall or self.shape_is_within_wall(wall_shapes, treasure_shape) and len(treasure_shape) >= 2:
                treasure_shape = self.eliminate_identical_points(treasure_shape.squeeze(axis=1).tolist())
                treasures.append(treasure_shape)
        return treasures

    def detect_wall(self, picture):
        opened = cv2.morphologyEx(picture, cv2.MORPH_OPEN, np.ones((25, 25), np.uint8))
        wall_contours = self.get_contours(opened, self.wall)
        wall_contours = [cnt for cnt in wall_contours if cv2.arcLength(cnt, True) > 500]
        return [cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True) for cnt in wall_contours]

    # https://www.ecse.rpi.edu/Homepages/wrf/Research/Short_Notes/pnpoly.html
    @staticmethod
    def shape_is_within_wall(walls, shape):
        c = False
        for wall in walls:
            c = False
            test_point_x, test_point_y = [float(val) - 5 for val in shape.min(axis=0)[0]]
            number_of_sides = len(wall)
            points_x = [float(val) for val in wall[:, 0][:, 0]]
            points_y = [float(val) for val in wall[:, 0][:, 1]]
            i, j = 0, number_of_sides - 1
            while i < number_of_sides:
                if (((points_y[i] > test_point_y) != (points_y[j] > test_point_y)) and
                        (test_point_x < (points_x[j] - points_x[i]) * (test_point_y - points_y[i]) / (
                                    points_y[j] - points_y[i]) + points_x[i])):
                    c = not c
                j = i
                i += 1
            if c:
                return True
        return c

    @staticmethod
    def eliminate_identical_points(shape):
        i, j = 0, 0
        while i < len(shape):
            while j < len(shape):
                if j != i and fabs(shape[i][0] - shape[j][0]) < 3 and fabs(shape[i][1] - shape[j][1]) < 3:
                    del shape[j]
                    j = len(shape)
                j += 1
            i += 1
            j = 0
        return shape

    def format_picture(self, picture):
        picture = cv2.GaussianBlur(picture, self.GAUSSIAN_SIZE, 0)
        picture = cv2.cvtColor(picture, cv2.COLOR_BGR2HSV)
        return picture
