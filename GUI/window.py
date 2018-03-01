from Tkinter import *

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
        self.c.pack()

    def pressed(self):
        print 'test'

    def create_window(self):
        window = Toplevel(self.root)

    def create_buttons(self):
        button1 = Button(self.root, text = 'press', command = self.create_window)
        button1.pack(side="top", expand=True, padx=4, pady=4)

        button2 = Button(self.root, text = 'press2', command = self.pressed)
        button2.pack(side="top", expand=True, padx=4, pady=4)
def main():
    root = Tk()
    gui = BlockWindow(root)
    root.mainloop()

main()
