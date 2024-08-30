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
        self.produce_time = 5
        self.produced_count = 0
        self.sent_count = 0
        self.sending = True

        self.provider.schedule_timer("produce", self.provider.current_time() + self.produce_time)

    def _produce(self):
        data = str(random())
        self.produced_packets.append(data)
        self.produced_count += 1
        
    def handle_timer(self, timer: str):
        if timer == "produce":
            self._produce()
            self.provider.schedule_timer("produce", self.provider.current_time() + self.produce_time)
        if timer == "start sending":
            self.sending = True
    def _assemble_packets(self) -> str:
        produced_message = " ".join(self.produced_packets)
        self.sent_count += len(self.produced_packets)
        self.produced_packets = []
        return produced_message
        
    def handle_packet(self, message: str):
        parsed_message: SimpleMessage = json.loads(message)
        if parsed_message['sender_type'] == NodeType.UAV.value and self.sending:
            if len(self.produced_packets) == 0:
                empty_response: SimpleMessage = {
                    'sender_id': self.provider.get_id(),
                    'sender_type': NodeType.SENSOR.value,
                    'content': "NO DATA"
                }
                command = SendMessageCommand(
                    message=json.dumps(empty_response),
                    destination=parsed_message['sender_id']
                )
                self.provider.send_communication_command(command)
                logging.info("Sending NO DATA")
            packet_size = len(self.produced_packets)
            packet_str = self._assemble_packets()
            response: SimpleMessage = {
                'sender_type': NodeType.SENSOR.value,
                'sender_id': self.provider.get_id(),
                'content': packet_str
            }
            logging.info(f"sender_type: {response['sender_type']}")
            message_command = SendMessageCommand(
                message=json.dumps(response),
                destination=parsed_message['sender_id']
            )
            self.provider.send_communication_command(message_command)
            self.sending = False
            self.provider.schedule_timer("start sending", self.provider.current_time() + 5)
            logging.info(f"Sent {packet_size} packets!")
    
    def handle_telemetry(self, telemetry: Telemetry):
        pass
    
    def finish(self):
        logging.info(f"Produced: {self.produced_count}")
        logging.info(f"Sent: {self.sent_count}")