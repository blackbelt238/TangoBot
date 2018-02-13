from bot import Bot

# Tango defines the behavior of a Tango bot
class Tango:
    # ports with which to access servos on the robot
    WAIST = 0
    SAME = 1 # wheels spinning in the same direction
    OPP = 2 # wheels spinning in the opposite direction
    SIDE = 3 # head moving side-to-side
    UPDOWN = 4 # head moving up/down

    CENTER = 6000 # where the Tango bot's joints are centered and speed is at 0
    TO_EXT = 3000 # the farthest from CENTER the joints and speed can go

    def __init__(self):
        self.tango = Bot() # bot instance for Tango bot

    # drive allows the tango bot to drive forwards or backwards at 3 different speeds
    def drive(self, direction):
        pos = self.tango.position(SAME) # determine the wheels' current position
        inc = TO_EXT / 3 # define the increments by which to accelerate

        # backward direction
        if direction < 0:
            # negatively accelerate the tango bot as long as it is not moving at its' maximum backward speed
            if pos < CENTER + TO_EXT:
                self.tango.accelerate(SAME, pos + inc)
        # forward direction
        elif direction > 0:
            # positively accelerate the tango bot as long as it is not moving at its' maximum forward speed
            if pos > CENTER - TO_EXT:
                self.tango.accelerate(SAME, pos - inc)

    # stop brings a moving Tango bot to a stop
    def stop(self):
        self.tango.accelerate(SAME, CENTER)
