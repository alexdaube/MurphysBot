from abc import ABCMeta

import cv2
import numpy as np

from common.map.point_of_interest.point_of_interest_type import PointOfInterestType


class DetectionStrategy(object):
    __metaclass__ = ABCMeta
    islands = {"Rouge": {"threshold": [[np.array([160, 60, 60]), np.array([180, 255, 255])],
                                       [np.array([0, 60, 60]), np.array([10, 255, 255])]],
                         "POIColor": PointOfInterestType.RED_COLOR},
               "Bleu": {"threshold": [[np.array([80, 60, 60]), np.array([100, 255, 255])]],
                        "POIColor": PointOfInterestType.BLUE_COLOR},
               "Vert": {"threshold": [[np.array([50, 60, 60]), np.array([80, 255, 255])]],
                        "POIColor": PointOfInterestType.GREEN_COLOR},
               "Jaune": {"threshold": [[np.array([15, 80, 80]), np.array([40, 255, 255])]],
                         "POIColor": PointOfInterestType.YELLOW_COLOR}}
    wall = [[np.array([0, 0, 0]), np.array([255, 255, 80])]]
    treasure = [[np.array([20, 150, 100]), np.array([40, 255, 255])]]

    @staticmethod
    def get_contours(picture, color):
        masks = []
        for thresh in color:
            lowthreshold, highthreshold = thresh
            masks.append(cv2.inRange(picture, lowthreshold, highthreshold))

        for i in range(1, len(masks)):
            masks[0] = cv2.bitwise_or(masks[0], masks[i])

        maskedpicture = cv2.bitwise_and(picture, picture, mask=masks[0])
        bwpicture = cv2.cvtColor(cv2.cvtColor(maskedpicture, cv2.COLOR_HSV2BGR), cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(bwpicture, 0, 255, 0)
        _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        return contours
