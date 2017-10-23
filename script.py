import tkinter
from tkinter.ttk import *

GUI = tkinter.Tk()
FrameList = []

class userGUI:
    def __init__(self,UserNum):
        if UserNum % 2 == 0:
            self.x = 2
            self.y = UserNum / 2
            self.y -= 1
        else:
            self.x = 1
            self.y = UserNum - 1
            self.y = self.y / 2

        self.userframe = tkinter.Frame(GUI)
        self.userframe.grid(column = int(self.x), row = int(self.y))
        FrameList.append(self.userframe)
        self.userLable = tkinter.Label(self.userframe, text = "user"+str(UserNum))
        self.userLable.grid()

def AddUsers(Number):
    for Frames in FrameList:
        Frames.destroy()
    for Num in range(Number):
        userGUI(Num+1)

def main():
    UserNumber = tkinter.StringVar()
    UserNum = tkinter.Entry(GUI, width=5, textvariable=UserNumber)
    UserNum.grid(column = 2, row=99)
    TestCommand = tkinter.Button(GUI, text = 'Test', width = 16,command = lambda: AddUsers(int(UserNumber.get())))
    TestCommand.grid(column=1, row=99)
    tkinter.mainloop()

main()