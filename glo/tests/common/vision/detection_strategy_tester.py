import json
from abc import abstractmethod, ABCMeta
from os import listdir
from os.path import isfile, join

import cv2


class DetectionStrategyTester(object):
    __metaclass__ = ABCMeta
    strategy = None
    testData = []

    def __init__(self, strategy):
        files = [f for f in listdir(self.PATH) if isfile(join(self.PATH, f))]
        files = [f.strip(".json") for f in files if f.endswith(".json")]
        self.testData = [{"name": f,
                          "json": join(self.PATH, f) + ".json",
                          "png": join(self.PATH, f) + ".png"} for f in files]
        self.strategy = strategy

    def test(self, testclass):
        errors = {}
        for test in self.testData:
            file = open(test["json"], "r")
            data = json.loads(file.read())
            testerrors = self.test_method(data, self.strategy.detect(cv2.imread(test["png"])))
            if len(testerrors) > 0:
                errors[test["name"]] = testerrors
        testclass.assertTrue(len(errors) == 0, errors)

    @abstractmethod
    def test_method(self, testdata, calculateddata):
        pass
