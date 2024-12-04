from enum import Enum

class LiveUpdateCommand(str, Enum):
    START = "start"
    STOP = "stop"