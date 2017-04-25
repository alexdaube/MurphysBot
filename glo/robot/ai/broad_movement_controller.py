import logging
import math
import time
from math import fabs
import sys
from mock import Mock

sys.modules['robot.hardware.bluetooth_decoder'] = Mock()
from robot.hardware.hardware_controller import WheelController


class BroadMovementController(object):
    MOVE_SPEED = 0.2
    ROTATE_SPEED = 50
    MAX_ROTATE = 20
    MAXIMUM_MOVE = 50.0

    def __init__(self, wheel_controller=None):
        self.wheel_controller = wheel_controller or WheelController()
        self.remote_logger = logging.getLogger("remote")

    def move(self, destination, waypoints, robot_position):
        next_point = destination
        while len(waypoints):
            if self.is_at_position(robot_position, waypoints[0], 50):
                del waypoints[0]
            else:
                next_point = waypoints[0]
                break
        self.remote_logger.info("Next destination point @ X:{}, Y:{}".format(next_point.X, next_point.Y))
        x_distance = float(next_point.X - robot_position["x"])
        y_distance = float(next_point.Y - robot_position["y"])
        angle = 360 + math.degrees(math.atan2(y_distance, x_distance)) - robot_position["w"]
        if angle > 180:
            angle = -(360 - angle)

        distance = min(math.sqrt(x_distance ** 2 + y_distance ** 2) / 4.5, self.MAXIMUM_MOVE)
        self.remote_logger.info("Move Angle:{}, Distance:{}".format(-angle, distance / 1000))
        self.wheel_controller.move_lateral_polar(-angle, distance / 1000, self.MOVE_SPEED)

    def face_wall(self, wall, robot_position):
        if wall == 'top':
            angle = 270
        elif wall == 'bottom':
            angle = 90
        elif wall == 'back':
            angle = 180
        self.rotate(angle, robot_position)
        self.remote_logger.info("Robot is now properly facing the " + wall + " wall!")

    def face_point(self, point, robot_position):
        x_distance = float(point.X - robot_position["x"])
        y_distance = float(point.Y - robot_position["y"])
        angle = math.degrees(math.atan2(y_distance, x_distance))
        self.rotate(angle, robot_position)
        self.remote_logger.info("Robot is now properly facing the island!")

    def rotate(self, desired_angle, robot_position):
        if desired_angle < 0: desired_angle += 360
        while fabs(robot_position["w"] - desired_angle) > 1:
            pos = robot_position["w"] - desired_angle > 0
            rotate_angle = min(fabs(robot_position["w"] - desired_angle), 60) / 2
            rotate_speed = max(18, rotate_angle)
            if pos:
                self.wheel_controller.rotate(rotate_angle, rotate_speed)
                robot_position["w"] += rotate_angle
            else:
                self.wheel_controller.rotate(-rotate_angle, rotate_speed)
                robot_position["w"] -= rotate_angle
            time.sleep(1)

    def is_at_position(self, robot_position, position, threshold):
        return fabs(robot_position["x"] - position.X) <= threshold \
               and fabs(robot_position["y"] - position.Y) <= threshold

    def back_away(self):
        self.wheel_controller.move_lateral_polar(135, 0.05, 0.1)
