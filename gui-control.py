import time
from tango import Tango
from tkinter import *

# ActionQueue represents the in-order list of actions that, when executed from the GUI, will be run on Tango
class ActionQueue:
    def __init__(self):
        self.tango = Tango()
        self.queue = [] # queue of actions

        self.distance = 0 # distance is how long we want to wait to go a certain distance

    # add enables an action to be added to the queue
    #   (actions will be added as either [function, direction] pairs or as [function] elements)
    def add(self, function, direction=None, port=None):
        print('\tadding:', function, direction, port)
        action = [function] # form the action by first adding the function to be invoked

        # if a direction is provided, tack it on to the action (this allows us to add calls with no arguments to the queue)
        if direction != None:
            action.append(direction)
        # if a port is provided, tack it on to the action
        if port != None:
            action.append(port)
        self.queue.append(action)

    # execute goes through the queued actions and executes them in-order
    def execute(self):
        for action in self.queue:
            func = action[0]

            # if arguments must be provided to the function, do so. Otherwise, don't provide any.
            if len(action) > 2:
                func(action[1], action[2])
            elif len(action) > 1:
                func(action[1])
            else:
                func()
            time.sleep(self.pause) # pause for the specified time

        self.tango.reset() # avoid out of control bot after the execution of the user's commands

    # remove takes the action at the given index out of the action queue
    def remove(self, index):
        self.queue.pop(index)

    # foot calculates the amount of sleep time for the robot to drive num feet
    def foot(num):
        return .025*(num**2) + .3*num - .125

class NestedWindow():
    sideWidth = 5
    sideHeight = 5
    vertWidth = 5
    vertHeight = 5
    def __init__(self, part, r, queue):
        self.queue = queue
        self.window = Toplevel(r)
        self.window.title(part)
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
        leftTwo = Button(self.window, text = '< <', width = self.sideWidth, height = self.sideHeight, command = lambda: self.queue.add(self.queue.tango.head,True,4))
        leftTwo.grid(row=2, column=0)

        leftOne = Button(self.window, text = ' < ', width = self.sideWidth, height = self.sideHeight, command = lambda: self.queue.add(self.queue.tango.head,True,4))
        leftOne.grid(row=2, column=1)

        upTwo = Button(self.window, text = '^\n^', width = self.vertWidth, height = self.vertHeight, command = lambda: self.queue.add(self.queue.tango.head,True,5))
        upTwo.grid(row=0, column=2)

        upOne = Button(self.window, text = '^\n', width = self.vertWidth, height = self.vertHeight, command = lambda: self.queue.add(self.queue.tango.head,True,5))
        upOne.grid(row=1, column=2)

        downTwo = Button(self.window, text = '^\n^', width = self.vertWidth, height = self.vertHeight, command = lambda: self.queue.add(self.queue.tango.head,False,5))
        downTwo.grid(row=4, column=2)

        downOne = Button(self.window, text = '^\n', width = self.vertWidth, height = self.vertHeight, command = lambda: self.queue.add(self.queue.tango.head,False,5))
        downOne.grid(row=3, column=2)

        rightOne = Button(self.window, text = ' > ', width = self.sideWidth, height = self.sideHeight, command = lambda: self.queue.add(self.queue.tango.head,False,4))
        rightOne.grid(row=2, column=3)

        rightTwo = Button(self.window, text = '> >', width = self.sideWidth, height = self.sideHeight, command = lambda: self.queue.add(self.queue.tango.head,False,4))
        rightTwo.grid(row=2, column=4)

    def torso_buttons(self):
        leftTwo = Button(self.window, text = '< <', width = self.sideWidth, height = self.sideHeight, command = lambda: self.queue.add(self.queue.tango.twist,False))
        leftTwo.grid(row=0, column=0)

        leftOne = Button(self.window, text = ' < ', width = self.sideWidth, height = self.sideHeight, command = lambda: self.queue.add(self.queue.tango.twist,False))
        leftOne.grid(row=0, column=1)

        rightOne = Button(self.window, text = ' > ', width = self.sideWidth, height = self.sideHeight, command = lambda: self.queue.add(self.queue.tango.twist,True))
        rightOne.grid(row=0, column=3)

        rightTwo = Button(self.window, text = '> >', width = self.sideWidth, height = self.sideHeight, command = lambda: self.queue.add(self.queue.tango.twist,True))
        rightTwo.grid(row=0, column=4)

    def drive_buttons(self):
        forwardOne = Button(self.window, text = '^\n^', width = self.vertWidth, height = self.vertHeight, command = lambda: self.queue.add(self.queue.tango.drive,True))
        forwardOne.grid(row=0, column=0)

        forwardTwo = Button(self.window, text = '^\n', width = self.vertWidth, height = self.vertHeight, command = lambda: self.queue.add(self.queue.tango.drive,True))
        forwardTwo.grid(row=1, column=0)

        stop = Button(self.window, text = 'STOP', width = self.vertWidth, height = self.vertHeight, command = lambda: self.queue.add(self.queue.tango.stop))
        stop.grid(row=2, column=0)

        backwardOne = Button(self.window, text = 'v\n', width = self.vertWidth, height = self.vertHeight, command = lambda: self.queue.add(self.queue.tango.drive,False))
        backwardOne.grid(row=3, column=0)

        backwardTwo = Button(self.window, text = 'v\nv', width = self.vertWidth, height = self.vertHeight, command = lambda: self.queue.add(self.queue.tango.drive,False))
        backwardTwo.grid(row=4, column=0)

    def turn_buttons(self):
        leftTwo = Button(self.window, text = '< <', width = self.sideWidth, height = self.sideHeight, command = lambda: self.queue.add(self.queue.tango.turn,False))
        leftTwo.grid(row=0, column=0)

        leftOne = Button(self.window, text = ' < ', width = self.sideWidth, height = self.sideHeight, command = lambda: self.queue.add(self.queue.tango.turn,False))
        leftOne.grid(row=0, column=1)

        rightOne = Button(self.window, text = ' > ', width = self.sideWidth, height = self.sideHeight, command = lambda: self.queue.add(self.queue.tango.turn,True))
        rightOne.grid(row=0, column=2)

        rightTwo = Button(self.window, text = '> >', width = self.sideWidth, height = self.sideHeight, command = lambda: self.queue.add(self.queue.tango.turn,True))
        rightTwo.grid(row=0, column=3)

    def destroy_window(self):
        self.window.destroy()

class BlockWindow():
    commandButtonWidth = 10
    commandButtonHeight = 5

    queueButtonWidth = 10
    queueButtonHeight = 3
    def __init__(self, r, c=None):
        self.queue = ActionQueue()
        self.queue.tango.reset() # reset everything before continuing

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
        window = NestedWindow(robo_part, self.root, self.queue)

    def remove_command(self, button_num):
        self.queue.remove(button_num)

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

        for i in range(8):
            self.boxes.append(Button(self.box_frame, width = self.queueButtonWidth, height = self.queueButtonHeight // 2, command = lambda i=i: self.remove_command(i)))
            self.boxes[i].place(x=(self.commandButtonWidth * 3.0) + 20, y=(i*30))
        ex = Button(self.box_frame, text = 'Execute', width = self.queueButtonWidth, height = self.queueButtonHeight // 2, command = lambda: self.queue.execute())
        self.boxes.append(ex)
        ex.place(x=(self.commandButtonWidth * 3.0) + 20, y=240)

def main():
    root = Tk()
    gui = BlockWindow(root)
    root.mainloop()

main()