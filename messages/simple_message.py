from typing import TypedDict
from enum import Enum

class NodeType(Enum):
    UAV = 0
    SENSOR = 1
    GROUND_STATION = 2

class SimpleMessage(TypedDict):
    sender_type: int
    sender_id: int
    content: str
    