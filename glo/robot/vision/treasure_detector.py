from robot.vision.treasure_detection_by_wall_contrast_strategy import TreasureDetectionByWallContrastStrategy


class TreasureDetector:
    def __init__(self, strategy=None):
        self.strategy = strategy or TreasureDetectionByWallContrastStrategy()

    def detect_treasures(self, picture, in_wall):
        return self.strategy.detect(picture, in_wall)
