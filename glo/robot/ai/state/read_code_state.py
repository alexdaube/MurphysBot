from common.map.point_of_interest.point_of_interest_type import PointOfInterestType
from robot.ai.broad_movement_controller import BroadMovementController
from robot.ai.state.move_to_treasure_state import MoveToTreasureState
from robot.ai.state.robot_state import RobotState
from robot.communication.robot_client import RobotClient
from robot.hardware.hardware_controller import ManchesterCodeReceiver


class ReadCodeState(RobotState):
    def __init__(self, controller, manchester_decoder=None, movement=None, client=None):
        super(ReadCodeState, self).__init__(controller)
        self.manchester_decoder = manchester_decoder or ManchesterCodeReceiver()
        self.movement = movement or BroadMovementController()
        self.client = client or RobotClient()

    def handle(self):
        letter = self.manchester_decoder.get_code()
        while letter is None:
            letter = self.manchester_decoder.get_code()
        destination = self.send_letter(letter)
        self.controller.set_destination(PointOfInterestType.from_string(destination))
        self.movement.back_away()
        self.next_state()

    def send_letter(self, letter):
        destination = self.client.get_destination(letter)
        data_destination = {'letter': letter, 'description': destination}
        self.client.send_destination(data_destination)
        return destination

    def next_state(self):
        if not self.run:
            return
        self.controller.set_state(MoveToTreasureState)
        self.controller.activate()
