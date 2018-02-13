import time

from enum import Enum
from maestro import Controller

class Tango:
    # ports with which to access servos on the robot
    WAIST = 0
    SAME = 1 # wheels spinning in the same direction
    OPP = 2 # wheels spinning in the opposite direction
    SIDE = 3 # head moving side-to-side
    UPDOWN = 4 # head moving up/down

    def __init__(self):
        self.tango = Controller() # servo controller for the Tango bot

    ### WHEEL Methods ###

    # accelerate gradually accelerates the Tango bot, ensuring it does not fall over
    def accelerate(self, port, target):
        pos = self.tango.getPosition(port) # find the current speed of the wheels
        dist = pos - target # how far we have to accelerate
        direction = lambda x: x and (1, -1)[dist < 0] # the direction of acceleration

        # incrementally set the speed of the wheels to the target speed
        for _ in range(abs(dist)):
            pos += 1 * direction
            self.tango.setTarget(port, pos)
            time.sleep(.001)

    # stop brings a moving Tango bot to a stop
    def stop(self):
        self.accelerate(SAME, 6000)
