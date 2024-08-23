import json
import logging
from random import random

from gradysim.protocol.interface import IProtocol
from gradysim.protocol.messages.communication import SendMessageCommand, CommunicationCommandType
from gradysim.protocol.messages.telemetry import Telemetry
from messages.simple_message import SimpleMessage
from messages.simple_message import NodeType

class SensorProtocol(IProtocol):
    def initialize(self):
        self.produced_packets = []
        self.produce_time = 10
        self.produced_count = 0
        self.sent_count = 0

        self.provider.schedule_timer("produce", self.provider.current_time() + self.produce_time)

    def _produce(self):
        data = random()
        self.produced_packets.append(data)
        self.produced_count += 1
        
    def handle_timer(self, timer: str):
        if timer == "produce":
            self.produce()
            self.provider.schedule_timer("produce", self.provider.current_time() + self.produce_time)
    
    def _assemble_packets(self) -> str:
        produced_message = " ".join(self.produced_packets)
        final_message = str(len(self.produced_packets)) + " " + produced_message
        self.sent_count += len(self.produced_packets)
        self.produced_packets = []
        return final_message
        
    def handler_packet(self, message: str):
        message: SimpleMessage = json.loads(message)
        if message.sender_type == NodeType.UAV:

            response: SimpleMessage = {
                'sender_type': NodeType.SENSOR,
                'sender_id': self.provider.get_id(),
                'content': self._assemble_packets()
            }

            message_command = SendMessageCommand(
                message=json.dumps(response),
                destination=message.sender_id
            )
            self.provider.send_communication_command(message_command)

        
    
    def handler_telemetry(self, Telemetry):
        pass
    
    def finish(self):
        logging.info(f"Produced: {self.produced_count}")
        logging.info(f"Sent: {self.sent_count}")