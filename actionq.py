import time
from server import Server
from tango import Tango

# ActionQueue represents the in-order list of actions that, when executed from the GUI, will be run on Tango
class ActionQueue:
    def __init__(self):
        self.tango = Tango()
        self.queue = []    # queue of actions

        self.degree = []   # degree contains amounts by which to turn in the order they were added
        self.distance = [] # distance contains distances to travel in the order they were added
        self.pause = 1     # sleep time between all queued actions

        # feed this ActionQueue to the server and kick it off in the background
        self.server = Server(self)
        self.server.start()

    # add enables an action to be added to the queue
    #   (actions will be added as either [function, direction] pairs or as [function] elements)
    def add(self, function, direction=None, port=None):
        self.queue.append(self.buildAction(function, direction, port))

    def pop(self):
        ''' pop removes the first action in the queue '''
        self.queue.pop(0)

    def push(self, function, direction=None, port=None):
        ''' push adds an action to the front of the queue.

            if adding a series of actions, push in the reverse order of desired execution
            ex. to make the robot MOVE_FORWARD->TURN_HEAD->MOVE_BACKWARD, first push MOVE_BACKWARD, then TURN_HEAD, and finally MOVE_FORWARD '''
        self.queue.insert(0, self.buildAction(function, direction, port))

    def buildAction(self, function, direction=None, port=None):
        ''' buildAction returns the action formatted as a list to be added to the queue '''
        print('    adding:', function, direction, port)
        action = [function] # form the action by first adding the function to be invoked

        # if a direction is provided, tack it on to the action (this allows us to add calls with no arguments to the queue)
        if direction != None:
            action.append(direction)
        # if a port is provided, tack it on to the action
        if port != None:
            action.append(port)
        return action

    def execute(self): # TODO: incrementally remove actions from queue directly following execution
        ''' execute goes through the queued actions and executes them in-order '''
        for i, action in enumerate(self.queue):
            func = action[0] # pull out the function name

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
                # if nothing was given, the robot must pause to listen
                if func == None:
                    self.queue = self.queue[i+1:] # remove any actions already executed
                    return                        # halt execution immediately
                func()
            time.sleep(self.pause) # pause for the specified time
        self.tango.reset() # avoid out of control bot after the execution of the user's commands
        self.queue = []    # remove all actions from queue

    # remove takes the action at the given index out of the action queue
    def remove(self, index):
        # disallow attempted removal of items outside the list
        if len(self.queue) < index + 1:
            return
        self.queue.pop(index)

    # set_distance sets the distance of turn rotation
    def set_degree(self, deg):
        self.degree.append(self.angle(deg))

    # set_distance sets the distance of drive travel
    def set_distance(self, num):
        self.distance.append(self.foot(num))

    # foot calculates the amount of sleep time for the robot to drive num feet
    def foot(self, num):
        return .025*(num**2) + .3*num - .125

    # angle calculates the amount of sleep time for the robot to turn a given angle
    def angle(self, deg):
        return -.00002304527*(deg**2) + .0144444444*deg - .3833333333
