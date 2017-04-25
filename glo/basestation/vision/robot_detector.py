class RobotDetector:
    def __init__(self, detection_strategy):
        self.detection_strategy = detection_strategy

    def detect_robot(self, picture):
        return self.detection_strategy.detect(picture)
