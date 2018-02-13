from bot import Bot

# Tango defines the behavior of a Tango bot
class Tango:
    # ports with which to access servos on the robot
    WAIST = 0
    SAME = 1 # wheels spinning in the same direction
    OPP = 2 # wheels spinning in the opposite direction
    SIDE = 3 # head moving side-to-side
    UPDOWN = 4 # head moving up/down

    def __init__(self):
        self.tango = Bot() # bot instance for Tango bot

    # stop brings a moving Tango bot to a stop
    def stop(self):
        self.accelerate(SAME, 6000)
