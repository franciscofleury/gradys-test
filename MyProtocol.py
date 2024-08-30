import logging

from gradysim.protocol.interface import IProtocol
from gradysim.protocol.messages.telemetry import Telemetry

class MyProtocol(IProtocol):
  
  def initialize(self):
    self.counter = 0;
    self.provider.schedule_timer("my_timer", self.provider.current_time() + 5)

  def handle_timer(self, timer: str):
    logging.info(f"{timer} expired!")
    self.counter += 1
    self.provider.schedule_timer(timer, self.provider.current_time() + 5)

  def handle_packet(self, message: str):
    logging.info(f"Message received: {message}")

  def handle_telemetry(self, Telemetry):
    Pass

  def finish(self):
    logging.info(f"my_timer executed {self.counter} times!")
