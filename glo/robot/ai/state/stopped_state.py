from robot.ai.state.robot_state import RobotState


class StoppedState(RobotState):
    def handle(self):
        print "stopped"

    def next_state(self):
        pass
