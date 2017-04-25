import cv2
import numpy as np

from common.constants import TABLE_WIDTH
from common.vision.detection_strategy import DetectionStrategy


class DotPatternDetectionStrategy(DetectionStrategy):
    def __init__(self, dot_pattern, dot_colors):
        self.radius_threshold = 5
        self.angle_offset = 270
        self.dot_pattern = dot_pattern
        self.dot_colors = dot_colors
        self.hue_threshold = 10
        self.distance_threshold = 25
        self.MIN_RADIUS = 20

    def detect(self, picture):
        picture_width = len(picture[0])
        picture_ratio = float(TABLE_WIDTH) / float(picture_width)

        kernel = np.ones((5, 5), np.uint8)

        img = cv2.GaussianBlur(picture, (5, 5), 0)
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        dots = self._extract_dots(img_hsv, kernel, picture_ratio)
        dots = self._filter_false_positive(dots, picture_ratio)

        if ('center' in dots):
            angle = self._find_orientation(self.dot_pattern, dots)
            robot = {'x': dots['center']['x'], 'y': dots['center']['y'], 'w': angle}
        else:
            robot = {}

        return robot

    def _extract_dots(self, img_hsv, kernel, picture_ratio):
        dots = []
        for dot in self.dot_pattern:
            color = self.dot_pattern[dot]['color']
            radius = self.dot_pattern[dot]['r']
            hue = self.dot_colors[color]['h'] / 2
            lower_range = np.array(
                [max(0, hue - self.hue_threshold), self.dot_colors[color]['s'], self.dot_colors[color]['v']])
            upper_range = np.array([min(180, hue + self.hue_threshold), 255, 255])

            colormask = cv2.inRange(img_hsv, lower_range, upper_range)

            maskedpicture = cv2.bitwise_and(img_hsv, img_hsv, mask=colormask)

            maskedpicture = cv2.erode(maskedpicture, kernel, iterations=1)
            maskedpicture = cv2.erode(maskedpicture, np.ones((3, 3), np.uint8), iterations=1)
            maskedpicture = cv2.dilate(maskedpicture, kernel, iterations=1)

            bwpicture = cv2.cvtColor(cv2.cvtColor(maskedpicture, cv2.COLOR_HSV2BGR), cv2.COLOR_BGR2GRAY)

            bwpicture = cv2.GaussianBlur(bwpicture, (5, 5), 0)

            ret, thresh = cv2.threshold(bwpicture, 0, 255, 0)
            im, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.001 * cnt_len, True)
                (x, y), r = cv2.minEnclosingCircle(cnt)
                r *= picture_ratio
                if self.MIN_RADIUS < r < radius + self.radius_threshold:
                    dots.append({'name': dot, 'x': x, 'y': y, 'r': r})
        return dots

    def _find_orientation(self, initial_dots, dots):
        angles = []

        for dot in initial_dots:
            if dot != 'center' and dot in dots:
                p1 = np.array([initial_dots[dot]['x'] - initial_dots['center']['x'],
                               initial_dots[dot]['y'] - initial_dots['center']['y']])
                p2 = np.array([dots[dot]['x'] - dots['center']['x'],
                               dots[dot]['y'] - dots['center']['y']])

                angles.append(self._angle_between(p1, p2))

        x, y = 0, 0
        for angle in angles:
            x += np.cos(np.radians(angle))
            y += np.sin(np.radians(angle))
        angle = np.arctan2(y, x)

        angle *= 360 / (2 * np.pi)
        if angle < 0:
            angle += 360

        return angle

    def _angle_between(self, p1, p2):
        angle = np.arctan2(p1[0], p1[1]) - np.arctan2(p2[0], p2[1])
        angle *= 360 / (2 * np.pi)
        if angle < 0:
            angle += 360

        angle = (angle + self.angle_offset) % 360

        return np.floor(angle)

    def _filter_false_positive(self, dots, picture_ratio):
        filtered_dots = {}

        if len(dots) == 1 and dots[0]['name'] == 'center':
            filtered_dots['center'] = dots[0]
            return filtered_dots

        for dot in dots:
            for other in dots:
                if dot['name'] != other['name']:
                    a1 = np.array([self.dot_pattern[dot['name']]['x'], self.dot_pattern[dot['name']]['y']])
                    b1 = np.array([self.dot_pattern[other['name']]['x'], self.dot_pattern[other['name']]['y']])
                    dot_dist = np.linalg.norm(a1 - b1)

                    a = np.array([dot['x'], dot['y']])
                    b = np.array([other['x'], other['y']])
                    dist = np.linalg.norm(a - b)
                    dist *= picture_ratio

                    if dist > dot_dist - self.distance_threshold and dist < dot_dist + self.distance_threshold:
                        filtered_dots[dot['name']] = dot

        return filtered_dots
