#!/usr/bin/python2

from subprocess import call

import yaml
from flask import Flask

from common.logger.logging_setup import configure_http_logger
from common.logger.logging_setup import configure_root_logger
from common.vision.camera import Camera
from robot.ai.robot_controller import RobotController
from robot.ai.state.move_to_charge_station_state import MoveToChargeStationState
from robot.communication.robot_api import RobotAPI
from robot.communication.robot_client import RobotClient
from robot.hardware.hardware_controller import PrehensorController, CameraController
from robot.vision.charge_station_detector import ChargeStationDetector
from robot.vision.island_detector import IslandDetector
from robot.vision.recharge_station_detection_strategy import RechargeStationDetectionStrategy
from robot.vision.robot_number_of_sides_island_strategy import RobotNumberOfSidesIslandStrategy
from robot.vision.robot_vision import RobotVision
from robot.vision.treasure_detection_by_wall_contrast_strategy import TreasureDetectionByWallContrastStrategy
from robot.vision.treasure_detector import TreasureDetector


def _configure_camera():
    call(["v4l2-ctl", "-d", "/dev/video0", "-c", "exposure_auto=1"])
    call(["v4l2-ctl", "-d", "/dev/video0", "-c", "exposure_auto_priority=0"])
    call(["v4l2-ctl", "-d", "/dev/video0", "-c", "exposure_absolute=1200"])


def main():
    _configure_camera()
    f = open('./data/charge_station_pattern.yml')
    dot_pattern = yaml.safe_load(f)
    f.close()
    f = open('./data/pattern_colors.yml')
    dot_colors = yaml.safe_load(f)
    f.close()

    configure_root_logger("robot")
    client = RobotClient()
    configure_http_logger("remote", client)
    vision = RobotVision(IslandDetector(RobotNumberOfSidesIslandStrategy()),
                         TreasureDetector(TreasureDetectionByWallContrastStrategy()),
                         ChargeStationDetector(RechargeStationDetectionStrategy(dot_pattern, dot_colors)),
                         Camera(0))

    controller = RobotController(client, vision, MoveToChargeStationState)
    pre = PrehensorController()
    pre.set_up_down('down')
    pre.set_up_down('up')
    cam = CameraController()
    cam.set_orientation(0, 0)
    controller.send_voltage(pre)
    api = RobotAPI(Flask("RobotAPI"), controller)
    api.run()


if __name__ == "__main__":
    main()
