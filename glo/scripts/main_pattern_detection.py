from glob import glob

import cv2
import yaml

from common.vision.dot_pattern_detection_strategy import DotPatternDetectionStrategy

if __name__ == '__main__':
    # camera = Camera(-1)
    # camera.start()


    f = open('../data/charge_station_pattern.yml')
    pattern = yaml.safe_load(f)
    f.close()
    f = open('../data/pattern_colors.yml')
    colors = yaml.safe_load(f)
    f.close()

    detection_strategy = DotPatternDetectionStrategy(pattern, colors)

    # while True:
    #     frame = camera.get_current_frame()
    #     cv2.imshow("preview", frame)
    #
    #     print detection_strategy.detect(frame)
    #
    #     key = cv2.waitKey(1)
    #     if key == 27: # exit on ESC
    #         break

    files = glob('../recharge_station.png')

    for file in files:
        frame = cv2.imread(file)

        detection_strategy = DotPatternDetectionStrategy(pattern, colors)

        print file + str(detection_strategy.detect(frame))

    key = cv2.waitKey(0)

    cv2.destroyAllWindows()
