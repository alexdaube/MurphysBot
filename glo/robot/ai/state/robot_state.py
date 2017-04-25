import logging
from abc import ABCMeta, abstractmethod


class RobotState(object):
    __metaclass__ = ABCMeta
    run = True

    def __init__(self, controller=None):
        self.controller = controller
        self.logger = logging.getLogger("RobotState")
        self.remote_logger = logging.getLogger("remote")

    def stop(self):
        self.run = False

    @abstractmethod
    def handle(self):
        pass

    def inject_command(self, command):
        pass

    def next_state(self):
        pass
