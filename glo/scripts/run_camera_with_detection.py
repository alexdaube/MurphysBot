from pprint import pprint
from subprocess import call

import cv2
import yaml

from common.vision.camera import Camera
from robot.vision.robot_number_of_sides_island_strategy import RobotNumberOfSidesIslandStrategy

if __name__ == '__main__':
    call(["v4l2-ctl", "-d", "/dev/video0", "-c", "exposure_auto=1"])
    call(["v4l2-ctl", "-d", "/dev/video0", "-c", "exposure_auto_priority=0"])
    call(["v4l2-ctl", "-d", "/dev/video0", "-c", "exposure_absolute=1200"])
    camera = Camera(-1)
    camera.start()

    f = open('../data/charge_station_pattern.yml')
    pattern = yaml.safe_load(f)
    f.close()
    f = open('../data/pattern_colors.yml')
    colors = yaml.safe_load(f)
    f.close()

    # detection = TreasureContrastStrategy()
    # detection = RechargeStationDetectionStrategy(pattern, colors)
    detection = RobotNumberOfSidesIslandStrategy()

    while True:
        frame = camera.get_current_frame()
        data = detection.detect(frame)
        cv2.imwrite('./img.png', frame)
        pprint(data)
        cv2.imshow('video', frame)
        cv2.waitKey(1)

    cv2.destroyAllWindows()
