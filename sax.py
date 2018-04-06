from Tkinter import *
from time import sleep
from threading import Thread


root = Tk()
photo_path = "Epic_sax_guy.gif"
max_frames = 12
frames = [PhotoImage(file = photo_path, format = 'gif -index %i' % (i)) for i in range (max_frames)]

def update2(ind):
    frame = frames[ind]
    ind += 1
    if ind == max_frames:
        ind = 0
    label.configure(image=frame)
    root.after(1, update2, ind)

def tkinterCreate():
    root2 = Tk()
    label2 = Label(root2)
    label2.pack()
    root2.after(0, update2, 0)

thread = Thread(target = tkinterCreate, args = (10, ))

def update1(ind):
    frame = frames[ind]
    ind += 1
    if ind == max_frames:
        ind = 0
    label.configure(image=frame)
    root.after(100, update1, ind)

label = Label(root)
label.pack()

root.after(0, update1, 0)
#root2.after(0, update2, 0)

root.mainloop()
