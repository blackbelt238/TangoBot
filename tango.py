from bot import Bot
from Tkinter import *
import os

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

    # center brings the given joint back to center
    def center(self, port):
        self.tango.bendTurn(port, CENTER)

    # drive allows the tango bot to drive forwards or backwards at 3 different speeds
    def drive(self, direction):
        pos = self.tango.position(SAME) # determine the wheels' current position
        inc = TO_EXT / 3 # accelerate with 3 speeds

        # backward direction
        if direction == False:
            # negatively accelerate the tango bot as long as it is not moving at its' maximum backward speed
            if pos < CENTER + TO_EXT:
                self.tango.accelerate(SAME, pos + inc)
        # forward direction
        elif direction == True:
            # positively accelerate the tango bot as long as it is not moving at its' maximum forward speed
            if pos > CENTER - TO_EXT:
                self.tango.accelerate(SAME, pos - inc)

    # head allows the Tango bot's head to turn or tilt with 5 degrees of resolution
    def head(self, port, direction):
        pos = self.tango.position(port) # determine the head's current position on the desired axis
        inc = TO_EXT / 5 # turn on 5 degrees/steps of resolution

        # tilt the head down / turn it left TODO: CONFIRM THIS
        if direction == False:
            if pos > CENTER - TO_EXT:
                self.tango.bendTurn(port, pos - inc)
        # tilt the head down / turn it right TODO: CONFIRM THIS
        elif direction == True:
            if pos < CENTER + TO_EXT:
                self.tango.bendTurn(port, pos + inc)

    # reset sets all joints and wheel speeds to their central setting
    def reset(self):
        self.stop()
        self.center(WAIST)
        self.center(SIDE)
        self.center(UPDOWN)

    # stop brings a moving Tango bot to a stop
    def stop(self):
        self.tango.accelerate(SAME, CENTER)

    # turn allows the Tango bot to turn left or right
    def turn(self, direction):
        pos = self.tango.position(DIFF) # determine the wheels' current position
        inc = TO_EXT / 3 # accelerate with 3 speeds
        length = .005 # length of time to turn

        # left turn TODO: check if this is correct
        if direction == False:
            # accelerate the wheels (L:-, R:+), leading to a left turn
            if pos < CENTER + TO_EXT:
                self.tango.accelerate(DIFF, pos + inc)
                Bot.wait(length)
                self.tango.accelerate(DIFF, pos)
        # right direction: TODO: check if this is correct
        elif direction == True:
            # accelerate the wheels (L:+, R:-), leading to a right turn
            if pos > CENTER - TO_EXT:
                self.tango.accelerate(DIFF, pos - inc)
                Bot.wait(length)
                self.tango.accelerate(DIFF, pos)

    # twist allows the Tango bot to twist at the waist along 3 degrees of resolution
    def twist(self, direction):
        pos = self.tango.position(WAIST) # determine the waist's current position
        inc = TO_EXT / 3 # twist on 3 degrees of resolution

        # twist left
        if direction == False:
            if pos > CENTER - TO_EXT:
                self.tango.bendTurn(port, pos - inc)
        # twist right
        elif direction == True:
            if pos < CENTER + TO_EXT:
                self.tango.bendTurn(port, pos + inc)
                
class InputHandler:
    def __init__(self):
        os.system('xset r off')
        self.tango = Tango() # Tango instance to issue commands
        self.root = tkinter.Tk()

    # Determine what to move from the key pressed.
    def input_pressed(key):
        print("Pressed {}".format(key))
        self.tango.drive(-1)

    # Slow down the robot on key release
    def input_released(key):
        print("Released {}".format(key))
    root.bind('<KeyPress>', method_name)
    root.bind('<KeyRelease>', method_name)

start = InputHandler()
