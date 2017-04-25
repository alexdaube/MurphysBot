import math
import random
import time
from subprocess import call

from robot.hardware.hardware_controller import CameraController
from robot.hardware.hardware_controller import WheelController


class FineMovementController:
    magnet_position = [347, 315]
    threshold = 30
    camera_threshold = 15
    camera_v_angle = 0
    camera_h_angle = 0
    max_angle = 45
    min_angle = -30

    def __init__(self, robot_vision, camera_controller=CameraController(),
                 wheel_controller=WheelController()):
        self.camera_controller = camera_controller
        self.wheel_controller = wheel_controller
        self.robot_vision = robot_vision

    def back_away(self):
        self._reset_camera_orientation()
        self.wheel_controller.move_forward(0.075, 0.1)

    def back_away_slowly(self):
        self._reset_camera_orientation()
        self.wheel_controller.move_forward(0.03, 0.1)

    def spaz_out(self):
        start = time.time()
        while time.time() - start < 5:
            self.camera_controller.set_orientation(random.randint(-90, 90), random.randint(-90, 90))

    def back_away_from_recharge_station(self):
        self._reset_camera_orientation()
        self.wheel_controller.move_lateral_polar(90, 0.05, 0.1)

    def ram_it(self):
        self._reset_camera_orientation()
        self.wheel_controller.move_forward(-0.06, 0.1)

    def fall_into_line_with_island(self, island_description, island_color):
        orientation = -90
        self.camera_controller.set_orientation(orientation, 0)
        side_move_left, side_move_right, side_moved = False, False, False
        side_move = 0.03
        move = -0.025
        while True:
            island, picture = self.robot_vision.detect_island(island_description, island_color, average_point=True)

            if island is not None:
                offset_x = island['points'][0] - (self.magnet_position[0])

                if math.fabs(offset_x) < self.threshold * 2:
                    break

                if side_move_left and side_move_right:
                    side_move /= 2.5
                    side_move_left, side_move_right = False, False
                if offset_x > 0:
                    side_moved = True
                    side_move_left = True
                    self.wheel_controller.move_lateral_cart(side_move, 0, 0.1)
                else:
                    side_moved = True
                    side_move_right = True
                    self.wheel_controller.move_lateral_cart(-side_move, 0, 0.1)
            else:
                move = -0.05
                orientation = (orientation + 5) % -90
                if orientation > -50:
                    orientation = -90
                self.camera_controller.set_orientation(orientation, 0)

        if not side_moved:
            self.wheel_controller.move_forward(move, 0.15)

    def is_aligned_with_island(self, island_color):
        self.camera_controller.set_orientation(-90, 0)
        islands, picture = self.robot_vision.detect_island(None, None, average_point=True,
                                                           black_out=self.magnet_position[1])

        for island in islands:
            if island["POIColor"] != island_color:
                continue
            if math.fabs(island["points"][0] - self.magnet_position[0]) <= self.threshold * 2 and \
                            math.fabs(island["points"][1] - self.magnet_position[1]) <= 75:
                return True
        return False

    def move_towards_charge_station(self):
        self._reset_camera_orientation()
        self.camera_v_angle = -10
        self.camera_controller.set_vertical(self.camera_v_angle)

        self._find_recharge_station()
        self._align_with_recharge_station()

    def fine_move_right(self):
        self.wheel_controller.move_lateral_polar(-90, 0.015, 0.1)
        self.wheel_controller.move_lateral_polar(0, 0.015, 0.1)

    def fine_move_left(self):
        self.wheel_controller.move_lateral_polar(90, 0.015, 0.1)
        self.wheel_controller.move_lateral_polar(0, 0.015, 0.1)

    def _find_recharge_station(self):
        max_angle_step = 5

        while True:
            recharge_station, picture = self.robot_vision.detect_recharge_station()
            picture_width = len(picture[0])

            if "x" in recharge_station:
                offset_x = recharge_station['x'] - (self.magnet_position[0])

                if math.fabs(offset_x) < self.camera_threshold:
                    break

                if offset_x > 0:
                    if math.fabs(offset_x) > picture_width / 3:
                        self.camera_h_angle += 5
                    else:
                        self.camera_h_angle += 1
                else:
                    if math.fabs(offset_x) > picture_width / 3:
                        self.camera_h_angle -= 5
                    else:
                        self.camera_h_angle -= 1
            else:
                if self.camera_h_angle > self.max_angle:
                    self.camera_h_angle = self.min_angle

                    if self.camera_v_angle - max_angle_step < self.min_angle:
                        self._reconfigure_camera()

                    self.camera_v_angle = (self.camera_v_angle - max_angle_step) % self.min_angle
                else:
                    self.camera_h_angle += max_angle_step

            self.camera_controller.set_orientation(self.camera_v_angle, self.camera_h_angle)

    @staticmethod
    def _reconfigure_camera():
        call(["v4l2-ctl", "-d", "/dev/video0", "-c", "exposure_auto=1"])
        call(["v4l2-ctl", "-d", "/dev/video0", "-c", "exposure_auto_priority=0"])
        call(["v4l2-ctl", "-d", "/dev/video0", "-c", "exposure_absolute=800"])

    def _align_with_recharge_station(self):
        max_side_move = 0.06

        while True:
            self.camera_controller.set_orientation(self.camera_v_angle, self.camera_h_angle)
            recharge_station, picture = self.robot_vision.detect_recharge_station()

            if "x" in recharge_station:
                offset_x = int(round(recharge_station['x'] - (self.magnet_position[0])))

                if -2 < self.camera_h_angle < 2 and math.fabs(offset_x) < self.threshold:
                    break

                if self.camera_h_angle > 0:
                    side_move = min(max_side_move, float(self.camera_h_angle) / 300)
                else:
                    side_move = max(-max_side_move, float(self.camera_h_angle) / 300)

                if 0.0 < side_move < 0.01:
                    side_move = 0.015
                elif -0.01 < side_move < 0.0:
                    side_move = -0.015

                self.wheel_controller.move_lateral_cart(side_move, 0, 0.1)

                if math.fabs(self.camera_h_angle) > 7:
                    self._reset_camera_orientation()

            self._find_recharge_station()

    def _reset_camera_orientation(self):
        self.camera_h_angle = 0
        self.camera_v_angle = 0
        self.camera_controller.reset_orientation()

    def verify_treasure_grab(self):
        self.back_away()
        self.camera_controller.set_orientation(-90, 0)
        time.sleep(0.3)
        treasures, picture = self.robot_vision.detect_treasures(black_out=self.magnet_position[1],
                                                                average_point=True, in_wall=False)
        for treasure in treasures:
            if math.fabs(treasure[1] - (self.magnet_position[1] - 10)) <= 25 and \
                                    (self.magnet_position[0] - 100) <= treasure[0] <= (self.magnet_position[0] + 100):
                return True
        return False

    def is_near_treasure(self):
        self.camera_controller.set_orientation(-90, 0)
        treasures, picture = self.robot_vision.detect_treasures(average_point=True,
                                                                black_out=self.magnet_position[1], in_wall=False)
        if len(treasures) and treasures[0][1] > self.magnet_position[1] - 150 and \
                        math.fabs(treasures[0][0] - self.magnet_position[0]) < 10:
            return True
        else:
            return False

    def move_towards_treasure(self):
        orientation = -60
        self.camera_controller.set_orientation(orientation, 0)
        side_move_left, side_move_right, side_moved = False, False, False
        move = -0.02
        side_move = 0.010

        while True:
            treasures, picture = self.robot_vision.detect_treasures(average_point=True, in_wall=False)
            picture_width = len(picture[0])

            if len(treasures):
                offset_x = picture_width
                for i in range(len(treasures)):
                    treasure_offset = treasures[i][0] - (self.magnet_position[0])
                    if treasure_offset < offset_x:
                        offset_x = treasure_offset

                if math.fabs(offset_x) < 10:
                    break

                if side_move_right and side_move_left:
                    side_move /= 1.5
                    side_move_left, side_move_right = False, False

                if offset_x > 0:
                    side_moved = True
                    side_move_right = True
                    self.wheel_controller.move_lateral_cart(side_move, 0, 0.15)
                else:
                    side_moved = True
                    side_move_left = True
                    self.wheel_controller.move_lateral_cart(-side_move, 0, 0.15)
            else:
                orientation = (orientation - 5) % -90
                if orientation > -60:
                    orientation = -90
                self.camera_controller.set_orientation(orientation, 0)
        if not side_moved:
            self.wheel_controller.move_forward(move, 0.15)
