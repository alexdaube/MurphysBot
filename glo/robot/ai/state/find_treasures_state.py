# coding=utf-8
import math

from common.constants import TABLE_HEIGHT, DISTANCE_OF_CAMERA_FROM_CENTER
from robot.ai.broad_movement_controller import BroadMovementController
from robot.ai.state.move_to_charge_station_state import MoveToChargeStationState
from robot.ai.state.robot_state import RobotState
from robot.hardware.hardware_controller import CameraController


class FindTreasuresState(RobotState):
    def __init__(self, controller, robot_vision=None, camera_controller=None,
                 movement_controller=None):
        super(FindTreasuresState, self).__init__(controller)
        self.robot_vision = robot_vision or controller.vision
        self.camera_controller = camera_controller or CameraController()
        self.movement_controller = movement_controller or BroadMovementController()

    def handle(self):
        found_treasures = []
        for val in ['top', 'bottom']:
            self.movement_controller.face_wall(val, self.controller.position)
            for angle in range(-90, 90, 3):
                real_angle = self.camera_controller.set_horizontal(angle)
                treasures, picture = self.robot_vision.detect_treasures(average_point=True)
                picture_width = len(picture[0])
                for treasure in treasures:
                    if math.fabs(treasure[0] - picture_width / 2) < 20:  # centered
                        found_position = self.get_treasure_position(real_angle)
                        if found_position is not None:
                            found_treasures.append(found_position)
        self.controller.add_treasures(self.average_found_treasure_positions(found_treasures))
        self.next_state()

    def average_found_treasure_positions(self, treasures):
        averaged_treasures = []
        while len(treasures) > 0:
            indices = [0]
            for i in range(1, len(treasures)):
                if math.fabs(treasures[i][0] - treasures[0][0]) < 100 and \
                                math.fabs(treasures[i][1] - treasures[0][1]) < 100:
                    indices.append(i)
            sum_x, sum_y = 0, 0
            for i in reversed(indices):
                sum_x += treasures[i][0]
                sum_y += treasures[i][1]
                del treasures[i]
            averaged_treasures.append([sum_x / len(indices), sum_y / len(indices)])
        return averaged_treasures

    def get_treasure_position(self, camera_angle):
        robot_angle = self.controller.position["w"]
        angle = (robot_angle + camera_angle) % 360

        robot_position = [self.controller.position["x"], self.controller.position["y"]]
        cam_position = [robot_position[0] + DISTANCE_OF_CAMERA_FROM_CENTER * math.cos(math.radians(robot_angle)),
                        robot_position[1] + DISTANCE_OF_CAMERA_FROM_CENTER * math.sin(math.radians(
                            robot_angle))]

        x_position, y_position = self.get_positions(angle, cam_position)

        if x_position > 1800:
            return None

        if x_position < 0:
            distance = cam_position[0] - x_position
            dy = float(y_position - cam_position[1]) / float(distance)
            x_position = 0
            y_position = cam_position[1] + cam_position[0] * dy
        return [round(x_position), round(y_position)]

    @staticmethod
    def get_positions(angle, cam_position):
        y_position = 0
        if angle < 90:
            triangle_angle = 90 - angle
            distance = TABLE_HEIGHT - cam_position[1]
            y_position = TABLE_HEIGHT
        elif angle < 180:
            triangle_angle = angle % 90
            distance = -(TABLE_HEIGHT - cam_position[1])
            y_position = TABLE_HEIGHT
        elif angle < 270:
            distance = -cam_position[1]
            triangle_angle = 270 - angle
        else:
            distance = cam_position[1]
            triangle_angle = angle % 90

        x_position = math.tan(math.radians(triangle_angle)) * distance + cam_position[0]
        return x_position, y_position

    def next_state(self):
        if not self.run:
            return
        self.controller.set_state(MoveToChargeStationState)
        self.controller.activate()
