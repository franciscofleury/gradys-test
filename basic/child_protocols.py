import logging

from gradysim.protocol.interface import IProtocol
from gradysim.protocol.messages.communication import CommunicationCommand, CommunicationCommandType
from gradysim.protocol.messages.mobility import SetSpeedMobilityCommand, GotoCoordsMobilityCommand
from gradysim.protocol.messages.telemetry import Telemetry

class BasicProtocol(IProtocol):
    def _move(self):
        point = self.away_point if self.direction == "away" else -self.away_point
        movement_command = GotoCoordsMobilityCommand(point, 0, 0)
        self.provider.send_mobility_command(movement_command)
        self.changed_counter += 1

    def initialize(self):
        self.away_point = 100 if self.provider.get_id() == 0 else -100
        self.speed = 2
        self.time_until_turn = 5
        
        self.changed_counter = 0
        self.direction = "away"

        speed_command = SetSpeedMobilityCommand(self.speed)
        self.provider.send_mobility_command(speed_command)
        self._move()
        self.provider.schedule_timer("change_directions", self.provider.current_time() + self.time_until_turn)
        self.provider.schedule_timer("go_back", self.provider.current_time() + 1)
        
    def handle_timer(self, timer: str):
        if timer == "change_directions" and self.direction == "away":
            self.direction = "towards"
            self._move()
        if timer == "go_back":
            message_command = CommunicationCommand(
                CommunicationCommandType.BROADCAST,
                message="GO BACK"
            )
            self.provider.send_communication_command(message_command)
            self.provider.schedule_timer("go_back", self.provider.current_time() + 1)

    def handle_packet(self, message: str):
        if message == "GO BACK":
            self.direction = "away"
            self._move()
            self.provider.schedule_timer("change_directions", self.provider.current_time() + self.time_until_turn)

    def handle_telemetry(self, Telemetry):
        pass

    def finish(self):
        logging.info(f"Changed direction {self.changed_counter} times!")
