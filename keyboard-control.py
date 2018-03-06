from tango import Tango
from tkinter import *
import os

class InputHandler:
    def __init__(self):
        os.system('xset r off')
        self.tango = Tango() # Tango instance to issue commands
        self.root = Tk()
        self.root.bind('<KeyPress>', self.char_pressed)
        self.root.bind('<KeyRelease>', self.char_released)
        self.root.bind('<Left>', self.left_pressed)
        self.root.bind('<Right>', self.right_pressed)
        self.root.bind('<Up>', self.up_pressed)
        self.root.bind('<Down>', self.down_pressed)

    # Determine what to move from the key pressed.
    def char_pressed(self, key):
        if key.char is 'w':
            self.tango.drive(True)
        elif key.char is 's':
            self.tango.drive(False)
        elif key.char is ' ':
            self.tango.reset()
        elif key.char is 'q':
            self.tango.twist(False)
        elif key.char is 'e':
            self.tango.twist(True)
        elif key.char is 'a':
            self.tango.turn(False)
        elif key.char is 'd':
            self.tango.turn(True)

    # Slow down the robot on key release
    def char_released(self, key):
        if key.char is 'a':
            self.tango.turn(True)
        elif key.char is 'd':
            self.tango.turn(False)

    def left_pressed(self, key):
        self.tango.head(self.tango.SIDE, True)

    def right_pressed(self, key):
        self.tango.head(self.tango.SIDE, False)

    def up_pressed(self, key):
        self.tango.head(self.tango.UPDOWN, True)

    def down_pressed(self, key):
        self.tango.head(self.tango.UPDOWN, False)
start = InputHandler()
