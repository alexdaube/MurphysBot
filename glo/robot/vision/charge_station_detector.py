from robot.vision.dummy_detection_strategy import DummyDetectionStrategy


class ChargeStationDetector(object):
    def __init__(self, strategy=None):
        self.strategy = strategy or DummyDetectionStrategy()

    def detect_charge_station(self, picture):
        return self.strategy.detect(picture)
