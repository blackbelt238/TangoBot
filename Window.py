from tango import Tango
class InputHandler:
    def __init__(self):
        os.system('xset r off')
        self.tango = Tango() # Tango instance to issue commands
        self.root = tkinter.Tk()

    # Determine what to move from the key pressed.
    def input_pressed(key):
        print('Pressed', key.char)
        if key.char is 'w':
            self.tango.drive(False)
        elif key.char is 's':
            self.tango.drive(True)
        elif key.char is ' ':
            self.tango.stop()

    # Slow down the robot on key release
    def input_released(key):
        print("Released", key.char)
    self.root.bind('<KeyPress>', method_name)
    self.root.bind('<KeyRelease>', method_name)

start = InputHandler()
