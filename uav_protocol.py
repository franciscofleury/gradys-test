import json
import logging
from random import random

from gradysim.protocol.interface import IProtocol
from gradysim.protocol.messages.communication import CommunicationCommand, CommunicationCommandType
from gradysim.protocol.messages.mobility import GotoCoordsMobilityCommand
from gradysim.protocol.messages.telemetry import Telemetry
from gradysim.simulator.handler.visualization import VisualizationController
from messages.simple_message import SimpleMessage
from messages.simple_message import NodeType

class UavProtocol(IProtocol):

    def _next_point(self):
        point = self.gs_pos
        if len(self.waypoints) != 0:
            point = self.waypoints.pop()

        movement = GotoCoordsMobilityCommand(point[0], point[1], 20)
        self.provider.send_mobility_command(movement)
        logging.info(f"Going to  ({point[0]}, {point[1]}, {point[2]})")
    def initialize(self):
        self.waypoints = [(300, -20, 0), (152, -30, 0), (-53, 32, 0)]
        self.gs_pos = (0,0,0)
        self.beat_on = True
        self.beat_interval = 1
        self.packets = []
        self.visited_sensors = []
        self._controller = VisualizationController()
        self.provider.schedule_timer("paint node", self.provider.current_time() + 5)

        logging.info(f"Node ID: {self.provider.get_id()}")
        self.provider.schedule_timer("heartbeat", self.provider.current_time() + self.beat_interval)
        self._next_point()
    def _heartbeat(self):
        hb_message: SimpleMessage = {
            "sender_id": self.provider.get_id(),
            "sender_type": NodeType.UAV.value,
            "content": "GET DATA"
        }

        command = CommunicationCommand(
            CommunicationCommandType.BROADCAST,
            message=json.dumps(hb_message)
        )
        self.provider.send_communication_command(command)
        logging.info("sending heartbeat")

    def handle_timer(self, timer: str):
        if timer == "heartbeat" and self.beat_on:
            self._heartbeat()
            self.provider.schedule_timer("heartbeat", self.provider.current_time() + self.beat_interval)
        if timer == "unvisit":
            self.visited_sensors.pop(0)
        if timer == "paint node":
            self._controller.paint_node(self.provider.get_id(), (0,255,0));
            self._controller.show_node_id(self.provider.get_id(), True);

    def handle_packet(self, message: str):
        parsed_message: SimpleMessage = json.loads(message)
        if parsed_message['sender_type'] == NodeType.SENSOR.value and parsed_message['sender_id'] not in self.visited_sensors:
            if not parsed_message['content'].startswith("NO DATA"):
                packets = parsed_message['content'].split(" ")
                logging.info(f"Received {len(packets)} packets!")
                self.packets.extend(packets)
            else:
                logging.info("Received empty message")
            self.visited_sensors.append(parsed_message['sender_id'])
            self.provider.schedule_timer("unvisit", self.provider.current_time() + 4)
            self._next_point()
    
    def handle_telemetry(self, telemetry: Telemetry):
        pass

    def finish(self):
        logging.info(f"Collected {len(self.packets)} packets!")

