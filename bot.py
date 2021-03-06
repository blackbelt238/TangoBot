import time
from maestro import Controller

# Bot contains the functionality underlying all Tango bot behaviors
class Bot:
    def __init__(self):
        self.bot = Controller() # servo controller for the Tango bot

    # accelerate allows the gradual acceleration of the Tango bot, ensuring it does not fall over
    def accelerate(self, port, target, t):
        pos = self.position(port) # find the current speed of the wheels
        dist = target - pos # how far we have to accelerate
        direction = -1 if dist < 0 else 1 # the direction of acceleration

        # incrementally set the speed of the wheels to the target speed
        for _ in range(abs(dist)):
            pos += 1 * direction
            self.bot.setTarget(port, pos)
            time.sleep(t)

    # bendTurn allows the Tango bot to turn or bend at one of its' joints
    def bendTurn(self, port, target):
        self.bot.setTarget(port, target)

    def position(self, port):
        return self.bot.getPosition(port)

    def wait(time):
        time.sleep(time)
