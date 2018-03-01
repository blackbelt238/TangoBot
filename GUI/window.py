from Tkinter import *

class NestedWindow():
    def __init__(self, part, r):
        self.window = Toplevel(r)
        self.create_buttons(part)

    def create_buttons(self, robo_part):
        if robo_part == 'head':
            self.head_buttons()

    def head_buttons(self):
        leftTwo = Button(self.window, text = '< <', command = self.destroy_window)
        leftTwo.grid(row=2, column=0)

        leftOne = Button(self.window, text = ' < ', command = self.destroy_window)
        leftOne.grid(row=2, column=1)

        upTwo = Button(self.window, text = '^\n^', command = self.destroy_window)
        upTwo.grid(row=0, column=2)
        
        upOne = Button(self.window, text = '^\n', command = self.destroy_window)
        upOne.grid(row=1, column=2)

        downTwo = Button(self.window, text = '^\n^', command = self.destroy_window)
        downTwo.grid(row=4, column=2)
        
        downOne = Button(self.window, text = '^\n', command = self.destroy_window)
        downOne.grid(row=3, column=2)

        rightOne = Button(self.window, text = ' > ', command = self.destroy_window)
        rightOne.grid(row=2, column=3)
        
        rightTwo = Button(self.window, text = '> >', command = self.destroy_window)
        rightTwo.grid(row=2, column=4)

    def destroy_window(self):
        self.window.destroy()

class BlockWindow():
    def __init__(self, r, c=None):
        self.client = c
        self.root = r
        self.flag = True
        r.title("TangoBot")
        self.canvasW = 1000
        self.canvasH = 530
        self.c = Canvas(self.root, width = self.canvasW, height = self.canvasH)
        self.create_buttons()

    def pressed(self):
        print 'test'

    def make_nested(self, robo_part):
        window = NestedWindow(robo_part, self.root)

    def create_buttons(self):
        head = Button(self.root, text = 'Head', command = lambda: self.make_nested('head'))
        head.place(x=0,y=0)

        torso = Button(self.root, text = 'Torso', command = self.pressed)
        torso.place(x=0,y=100)
def main():
    root = Tk()
    gui = BlockWindow(root)
    root.mainloop()

main()
