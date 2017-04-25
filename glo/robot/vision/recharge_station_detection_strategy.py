import cv2
import numpy as np

from common.constants import TABLE_WIDTH
from common.vision.dot_pattern_detection_strategy import DotPatternDetectionStrategy


class RechargeStationDetectionStrategy(DotPatternDetectionStrategy):
    def __init__(self, dot_pattern, dot_colors):
        super(RechargeStationDetectionStrategy, self).__init__(dot_pattern, dot_colors)
        self.hue_threshold = 15
        self.sat_threshold = 55
        self.val_threshold = 55
        self.MIN_RADIUS = 100

    def detect(self, picture):
        picture_width = len(picture[0])
        picture_ratio = float(TABLE_WIDTH) / float(picture_width)

        kernel = np.ones((5, 5), np.uint8)

        img = cv2.GaussianBlur(picture, (5, 5), 0)
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        dots = self._extract_dots(img_hsv, kernel, picture, picture_ratio)
        dots = self._filter_false_positive(dots, picture_ratio)

        if ('center' in dots):
            angle = self._find_orientation(self.dot_pattern, dots)
            robot = {'x': dots['center']['x'], 'y': dots['center']['y'], 'w': angle}
        else:
            robot = {}

        return robot

    def _extract_dots(self, img_hsv, kernel, picture, picture_ratio):
        dots = []
        for dot in self.dot_pattern:

            color = self.dot_pattern[dot]['color']
            radius = self.dot_pattern[dot]['r']
            hue = self.dot_colors[color]['h'] / 2
            sat = self.dot_colors[color]['s'] * 2.55
            val = self.dot_colors[color]['v'] * 2.55
            lower_range = np.array(
                [max(0, hue - self.hue_threshold), max(0, sat - self.sat_threshold), max(0, val - self.val_threshold)])
            upper_range = np.array([min(180, hue + self.hue_threshold), min(255, sat + self.sat_threshold),
                                    min(255, val + self.val_threshold)])

            colormask = cv2.inRange(img_hsv, lower_range, upper_range)

            maskedpicture = cv2.bitwise_and(img_hsv, img_hsv, mask=colormask)
            maskedpicture = cv2.erode(maskedpicture, kernel, iterations=1)
            maskedpicture = cv2.dilate(maskedpicture, kernel, iterations=1)

            bwpicture = cv2.cvtColor(cv2.cvtColor(maskedpicture, cv2.COLOR_HSV2BGR), cv2.COLOR_BGR2GRAY)

            bwpicture = cv2.GaussianBlur(bwpicture, (5, 5), 0)

            ret, thresh = cv2.threshold(bwpicture, 0, 255, 0)
            im, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02 * cnt_len, True)
                (x, y), r = cv2.minEnclosingCircle(cnt)
                r *= picture_ratio
                if self.MIN_RADIUS < r < radius + self.radius_threshold:
                    cv2.drawContours(picture, cnt, -1, (255, 0, 0), 2)
                    dots.append({'name': dot, 'x': x, 'y': y, 'r': r})
        return dots
