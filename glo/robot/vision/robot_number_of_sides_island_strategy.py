# -*- coding: utf-8 -*-

import cv2

from common.vision.detection_strategy import DetectionStrategy
from common.vision.island_handler import IslandHandler


class RobotNumberOfSidesIslandStrategy(DetectionStrategy):
    GAUSSIAN_SIZE = (5, 5)

    def detect(self, picture):
        picture = self.format_picture(picture)
        islands = []
        for color in self.islands:
            contours = self.get_contours(picture, self.islands[color]["threshold"])
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area < 3000 or area > 34000:
                    continue
                # approximate the polygon with 2% tolerance
                shape = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
                height = float(shape.max(axis=0)[0][1]) - float(shape.min(axis=0)[0][1])
                width = float(shape.max(axis=0)[0][0]) - float(shape.min(axis=0)[0][0])
                if (height / width) < 0.5 or (height / width) > 2:
                    continue
                shape = IslandHandler.remove_intermediate_points(shape)
                shape = IslandHandler.parse_shape(shape, color, self.islands[color]["POIColor"])
                if shape is not None:
                    islands.append(shape)

        return islands

    def format_picture(self, picture):
        picture = cv2.GaussianBlur(picture, self.GAUSSIAN_SIZE, 0)
        picture = cv2.cvtColor(picture, cv2.COLOR_BGR2HSV)
        return picture
