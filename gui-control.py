import threading
import time
from server import Server
from tango import Tango
from tkinter import *

# ActionQueue represents the in-order list of actions that, when executed from the GUI, will be run on Tango
class ActionQueue:
    def __init__(self):
        self.tango = Tango()
        self.queue = []    # queue of actions

        self.degree = []   # keep track of how long to wait to turn the desired number of degrees
        self.distance = [] # keep track of how long to wait to go a certain distance
        self.pause = 1     # sleep time between all queued actions

        # feed this ActionQueue to the server and kick it off in the background
        Server.actionqueue = self
        threading.Thread(target=Server.start).start()

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

            # if arguments must be provided to call the function, do so. Otherwise, don't provide any.
            if len(action) > 2:
                func(action[1], action[2])
            elif len(action) > 1:
                func(action[1])

                # if executing a wheel-related action, sleep for the necessary amount of time
                if func == self.tango.drive:
                    time.sleep(self.distance.pop(0))
                elif func == self.tango.turn:
                    time.sleep(self.degree.pop(0))
                self.tango.stop() # stop after driving or turning (no effect if not moving)
            else:
                func()
            time.sleep(self.pause) # pause for the specified time
        self.tango.reset() # avoid out of control bot after the execution of the user's commands

    # remove takes the action at the given index out of the action queue
    def remove(self, index):
        # disallow attempted removal of items outside the list
        if len(self.queue) < index + 1:
            return
        self.queue.pop(index)

    # set_distance sets the distance of turn rotation
    def set_degree(self, deg):
        self.degree.append(ActionQueue.angle(deg))

    # set_distance sets the distance of drive travel
    def set_distance(self, num):
        self.distance.append(ActionQueue.foot(num))

    # foot calculates the amount of sleep time for the robot to drive num feet
    def foot(num):
        return .025*(num**2) + .3*num - .125

    # angle calculates the amount of sleep time for the robot to turn a given angle
    def angle(deg):
        return -.00002304527*(deg**2) + .0144444444*deg - .3833333333

# NestedWindow represents a window that is opened up by a BlockWindow
class NestedWindow():
    sideWidth = 5
    sideHeight = 5
    vertWidth = 5
    vertHeight = 5
    def __init__(self, part, r, queue):
        self.queue = queue
        self.window = Toplevel(r)
        self.window.title(part) # name the window according to what it's controlling
        self.create_buttons(part)

    # create_buttons
    def create_buttons(self, robo_part):
        if robo_part == 'head':
            self.head_buttons()
        elif robo_part == 'torso':
            self.torso_buttons()
        elif robo_part == 'drive':
            self.drive_buttons()
        elif robo_part == 'speak':
            self.speak_buttons()
        elif robo_part == 'turn':
            self.turn_buttons()

    # head_buttons populates the window with all buttons relating to operating the head
    def head_buttons(self):
        left = Button(self.window, text = 'LEFT', width = self.sideWidth, height = self.sideHeight, command = lambda: self.queue.add(self.queue.tango.head,True,3))
        left.grid(row=1, column=0)

        up = Button(self.window, text = 'UP', width = self.vertWidth, height = self.vertHeight, command = lambda: self.queue.add(self.queue.tango.head,True,4))
        up.grid(row=0, column=1)

        down = Button(self.window, text = 'DOWN', width = self.vertWidth, height = self.vertHeight, command = lambda: self.queue.add(self.queue.tango.head,False,4))
        down.grid(row=2, column=1)

        right = Button(self.window, text = 'RIGHT', width = self.sideWidth, height = self.sideHeight, command = lambda: self.queue.add(self.queue.tango.head,False,3))
        right.grid(row=1, column=2)

    # torso_buttons populates the window with all buttons relating to turning at the waist
    def torso_buttons(self):
        left = Button(self.window, text = 'LEFT', width = self.sideWidth, height = self.sideHeight, command = lambda: self.queue.add(self.queue.tango.twist,False))
        left.grid(row=0, column=0)

        right = Button(self.window, text = 'RIGHT', width = self.sideWidth, height = self.sideHeight, command = lambda: self.queue.add(self.queue.tango.twist,True))
        right.grid(row=0, column=1)

    # drive_buttons populates the window with all buttons relating to getting the robot to drive
    def drive_buttons(self):
        # buttons for causing a drive
        forward = Button(self.window, text = 'FWD', width = self.vertWidth, height = self.vertHeight, command = lambda: self.queue.add(self.queue.tango.drive,True))
        forward.grid(row=0, column=0)

        backward = Button(self.window, text = 'BWD', width = self.vertWidth, height = self.vertHeight, command = lambda: self.queue.add(self.queue.tango.drive,False))
        backward.grid(row=1, column=0)

        # distances for the drive_buttons
        one = Button(self.window, text = '1', width = self.vertWidth, height = self.vertHeight // 2, command = lambda: self.queue.set_distance(1))
        one.grid(row=0, column=1)

        two = Button(self.window, text = '2', width = self.vertWidth, height = self.vertHeight // 2, command = lambda: self.queue.set_distance(2))
        two.grid(row=1, column=1)

        three = Button(self.window, text = '3', width = self.vertWidth, height = self.vertHeight // 2, command = lambda: self.queue.set_distance(3))
        three.grid(row=2, column=1)

        four = Button(self.window, text = '4', width = self.vertWidth, height = self.vertHeight // 2, command = lambda: self.queue.set_distance(4))
        four.grid(row=3, column=1)

        five = Button(self.window, text = '5', width = self.vertWidth, height = self.vertHeight // 2, command = lambda: self.queue.set_distance(5))
        five.grid(row=4, column=1)

    def speak_buttons(self):
        p1 = Button(self.window, text='\"Ironic\"', width = self.sideWidth, height = self.sideHeight, command = lambda: self.queue.add(self.queue.tango.speak,'ironic'))
        p1.grid(row=0, column=0)

        p2 = Button(self.window, text='\"In Response\"', width = self.sideWidth, height = self.sideHeight, command = lambda: self.queue.add(self.queue.tango.speak,'in response'))
        p2.grid(row=0, column=1)

    # turn_buttons populates the window with all buttons relating to getting the robot to turn
    def turn_buttons(self):
        # buttons for causing a turn
        left = Button(self.window, text = 'LEFT', width = self.vertWidth, height = self.vertHeight, command = lambda: self.queue.add(self.queue.tango.turn,False))
        left.grid(row=0, column=0)

        right = Button(self.window, text = 'RIGHT', width = self.vertWidth, height = self.vertHeight, command = lambda: self.queue.add(self.queue.tango.turn,True))
        right.grid(row=1, column=0)

        # distances for the drive_buttons
        fortyfive = Button(self.window, text = '45 deg', width = self.vertWidth, height = self.vertHeight // 2, command = lambda: self.queue.set_degree(45))
        fortyfive.grid(row=0, column=1)

        ninety = Button(self.window, text = '90 deg', width = self.vertWidth, height = self.vertHeight // 2, command = lambda: self.queue.set_degree(90))
        ninety.grid(row=1, column=1)

        oneeighty = Button(self.window, text = '180 deg', width = self.vertWidth, height = self.vertHeight // 2, command = lambda: self.queue.set_degree(180))
        oneeighty.grid(row=2, column=1)

    # destroy_window kills the nested window
    def destroy_window(self):
        self.window.destroy()

# BlockWindow is the home window for controlling Tango
class BlockWindow():
    commandButtonWidth = 10
    commandButtonHeight = 5

    queueButtonWidth = 10
    queueButtonHeight = 3
    def __init__(self, r, c=None):
        self.queue = ActionQueue() # keep track of actions
        self.queue.tango.reset()   # reset everything before continuing

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
        ''' make_nested creates a nested window representing the control of the given part '''
        window = NestedWindow(robo_part, self.root, self.queue)

    def remove_command(self, button_num):
        self.queue.remove(button_num)
        self.update_command_boxes()

    def create_buttons(self):
        ''' create_buttons places the main command buttons on the screen '''
        head = Button(self.root, text = 'Head', width = self.commandButtonWidth, height = self.commandButtonHeight, command = lambda: self.make_nested('head'))
        head.place(x=(self.commandButtonWidth * 2),y=0)

        torso = Button(self.root, text = 'Torso', width = self.commandButtonWidth, height = self.commandButtonHeight,  command = lambda: self.make_nested('torso'))
        torso.place(x=(self.commandButtonWidth * 2),y=100)

        drive = Button(self.root, text = 'Drive', width = self.commandButtonWidth, height = self.commandButtonHeight, command = lambda: self.make_nested('drive'))
        drive.place(x=(self.commandButtonWidth * 2),y=200)

        turn = Button(self.root, text = 'Turn', width = self.commandButtonWidth, height = self.commandButtonHeight, command = lambda: self.make_nested('turn'))
        turn.place(x=(self.commandButtonWidth * 2),y=300)

        speak = Button(self.root, text = 'Speak', width = self.commandButtonWidth, height = self.commandButtonHeight, command = lambda: self.make_nested('speak'))
        speak.place(x=(self.commandButtonWidth * 2),y=400)

    def create_command_boxes(self):
        self.boxes = []
        self.box_frame = Frame(self.root, width = 200, height = 480, bg='White')
        self.box_frame.place(x=(self.commandButtonWidth * 8) + 50, y=0)

        for i in range(8):
            self.boxes.append(Button(self.box_frame, width = self.queueButtonWidth, height = self.queueButtonHeight // 2, command = lambda i=i: self.remove_command(i)))
            self.boxes[i].place(x=(self.commandButtonWidth * 3.0) + 20, y=(i*30))

        # create the execute button below the queue of actions
        ex = Button(self.box_frame, text = 'Execute', width = self.queueButtonWidth, height = self.queueButtonHeight, command = lambda: self.queue.execute())
        self.boxes.append(ex)
        ex.place(x=(self.commandButtonWidth * 3.0) + 20, y=240)

    # update_command_boxes ensures the command box names are consistent with the actions in them
    def update_command_boxes(self, event = None):
        index = 0
        # update all boxes referring to actions
        for action in self.queue.queue:
            box = self.boxes[index]
            fname = action[0].__name__[action[0].__name__.rfind('.')+1:]
            box.config(text=fname)
            index += 1
        # clear all boxes no longer referring to actions
        for i in range(index, 8):
            self.boxes[i].config(text='')

def main():
    root = Tk()
    gui = BlockWindow(root) # create the GUI
    root.bind('<FocusIn>', gui.update_command_boxes) # ensures the command boxes update every time focus returns to the window
    root.mainloop()

main()
