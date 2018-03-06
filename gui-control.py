import time
from tango import Tango
from tkinter import *

# ActionQueue represents the in-order list of actions that, when executed from the GUI, will be run on Tango
class ActionQueue:
    def __init__(self):
        self.tango = Tango()
        self.queue = [] # queue of actions
        self.pause = 1000

    # add enables an action to be added to the queue
    #   (actions will be added as either [function, direction] pairs or as [function] elements)
    def add(self, function, direction):
        action = [function] # form the action by first adding the function to be invoked

        # if a direction is provided, tack it on to the action (this allows us to add calls with no arguments to the queue)
        if direction != None:
            action.append(direction)
        self.queue.append(action)

    # execute goes through the queued actions and executes them in-order
    def execute(self):
        for action in self.queue:
            func = action[0]

            # if arguments must be provided to the function, do so. Otherwise, don't provide any.
            if len(action) > 1:
                self.tango.func(action[1])
            else:
                self.tango.func()
            time.wait(self.pause) # pause for the specified time

        self.tango.reset() # avoid out of control bot after the execution of the user's commands

    # remove takes the action at the given index out of the action queue
    def remove(self, index):
        self.queue.pop(index)

class NestedWindow():
    sideWidth = 5
    sideHeight = 5
    vertWidth = 5
    vertHeight = 5
    def __init__(self, part, r):
        self.window = Toplevel(r)
        self.create_buttons(part)

    def create_buttons(self, robo_part):
        if robo_part == 'head':
            self.head_buttons()
        elif robo_part == 'torso':
            self.torso_buttons()
        elif robo_part == 'drive':
            self.drive_buttons()
        elif robo_part == 'turn':
            self.turn_buttons()

    def head_buttons(self):
        leftTwo = Button(self.window, text = '< <', width = self.sideWidth, height = self.sideHeight, command = self.destroy_window)
        leftTwo.grid(row=2, column=0)

        leftOne = Button(self.window, text = ' < ', width = self.sideWidth, height = self.sideHeight, command = self.destroy_window)
        leftOne.grid(row=2, column=1)

        upTwo = Button(self.window, text = '^\n^', width = self.vertWidth, height = self.vertHeight, command = self.destroy_window)
        upTwo.grid(row=0, column=2)

        upOne = Button(self.window, text = '^\n', width = self.vertWidth, height = self.vertHeight, command = self.destroy_window)
        upOne.grid(row=1, column=2)

        downTwo = Button(self.window, text = '^\n^', width = self.vertWidth, height = self.vertHeight, command = self.destroy_window)
        downTwo.grid(row=4, column=2)

        downOne = Button(self.window, text = '^\n', width = self.vertWidth, height = self.vertHeight, command = self.destroy_window)
        downOne.grid(row=3, column=2)

        rightOne = Button(self.window, text = ' > ', width = self.sideWidth, height = self.sideHeight, command = self.destroy_window)
        rightOne.grid(row=2, column=3)

        rightTwo = Button(self.window, text = '> >', width = self.sideWidth, height = self.sideHeight, command = self.destroy_window)
        rightTwo.grid(row=2, column=4)

    def torso_buttons(self):
        leftTwo = Button(self.window, text = '< <', width = self.sideWidth, height = self.sideHeight, command = self.destroy_window)
        leftTwo.grid(row=0, column=0)

        leftOne = Button(self.window, text = ' < ', width = self.sideWidth, height = self.sideHeight, command = self.destroy_window)
        leftOne.grid(row=0, column=1)

        rightOne = Button(self.window, text = ' > ', width = self.sideWidth, height = self.sideHeight, command = self.destroy_window)
        rightOne.grid(row=0, column=3)

        rightTwo = Button(self.window, text = '> >', width = self.sideWidth, height = self.sideHeight, command = self.destroy_window)
        rightTwo.grid(row=0, column=4)

    def drive_buttons(self):
        forwardOne = Button(self.window, text = '^\n^', width = self.vertWidth, height = self.vertHeight, command = self.destroy_window)
        forwardOne.grid(row=0, column=0)

        forwardTwo = Button(self.window, text = '^\n', width = self.vertWidth, height = self.vertHeight, command = self.destroy_window)
        forwardTwo.grid(row=1, column=0)

        backwardOne = Button(self.window, text = 'v\n', width = self.vertWidth, height = self.vertHeight, command = self.destroy_window)
        backwardOne.grid(row=2, column=0)

        backwardTwo = Button(self.window, text = 'v\nv', width = self.vertWidth, height = self.vertHeight, command = self.destroy_window)
        backwardTwo.grid(row=3, column=0)

    def turn_buttons(self):
        leftTwo = Button(self.window, text = '< <', width = self.sideWidth, height = self.sideHeight, command = self.destroy_window)
        leftTwo.grid(row=0, column=0)

        leftOne = Button(self.window, text = ' < ', width = self.sideWidth, height = self.sideHeight, command = self.destroy_window)
        leftOne.grid(row=0, column=1)

        rightOne = Button(self.window, text = ' > ', width = self.sideWidth, height = self.sideHeight, command = self.destroy_window)
        rightOne.grid(row=0, column=3)

        rightTwo = Button(self.window, text = '> >', width = self.sideWidth, height = self.sideHeight, command = self.destroy_window)
        rightTwo.grid(row=0, column=4)

    def destroy_window(self):
        self.window.destroy()

class BlockWindow():
    commandButtonWidth = 10
    commandButtonHeight = 5

    queueButtonWidth = 10
    queueButtonHeight = 3
    def __init__(self, r, c=None):
        self.client = c
        self.root = r
        self.flag = True
        r.title("TangoBot")
        self.canvasW = 300
        self.canvasH = 530
        self.c = Canvas(self.root, width = self.canvasW, height = self.canvasH)
        self.create_buttons()
        self.create_command_boxes()
        self.c.pack()

        self.current_command = 0

    def add_command(self, command):
        current_box = self.boxes[self.current_command]
        current_box.set(command)
        self.boxes[self.current_command] = current_box
        self.current_command += 1

    def make_nested(self, robo_part):
        window = NestedWindow(robo_part, self.root)

    def remove_command(self, button_num):
        print(button_num)

    def create_buttons(self):
        head = Button(self.root, text = 'Head', width = self.commandButtonWidth, height = self.commandButtonHeight, command = lambda: self.make_nested('head'))
        head.place(x=(self.commandButtonWidth * 2),y=0)

        torso = Button(self.root, text = 'Torso', width = self.commandButtonWidth, height = self.commandButtonHeight,  command = lambda: self.make_nested('torso'))
        torso.place(x=(self.commandButtonWidth * 2),y=100)

        drive = Button(self.root, text = 'Drive', width = self.commandButtonWidth, height = self.commandButtonHeight, command = lambda: self.make_nested('drive'))
        drive.place(x=(self.commandButtonWidth * 2),y=200)

        turn = Button(self.root, text = 'Turn', width = self.commandButtonWidth, height = self.commandButtonHeight, command = lambda: self.make_nested('turn'))
        turn.place(x=(self.commandButtonWidth * 2),y=300)

    def create_command_boxes(self):
        self.boxes = []
        self.box_frame = Frame(self.root, width = 200, height = 480, bg='White')
        self.box_frame.place(x=(self.commandButtonWidth * 8) + 50, y=0)
        #self.box_frame.pack()

        for i in range(8):
            self.boxes.append(Button(self.box_frame, width = self.queueButtonWidth, height = self.queueButtonHeight, command = lambda i=i: self.remove_command(i)))
            self.boxes[i].place(x=(self.commandButtonWidth * 3.0) + 20, y=(i*60))
def main():
    root = Tk()
    gui = BlockWindow(root)
    root.mainloop()

main()
