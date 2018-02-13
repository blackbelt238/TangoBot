from enum import Enum
from maestro import Controller

class Tango:
    def __init__(self):
        self.tango = Controller() # servo controller for the Tango bot

# ports with which to access servos on the robot
class Port(Enum):
    WAIST = 0
    SAME = 1
    OPP = 2
    SIDE = 3
    UPDOWN = 4
