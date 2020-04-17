from tkinter import filedialog
from tkinter import Tk
from fileHandling.db import addFile, getAllFiles
fileList = []


# def addFile(name, path):
#     global fileList
#     mapL = {}
#     mapL["name"] = name
#     mapL["path"] = path
#     fileList.append(mapL)


def getFiles():
    return getAllFiles()

def addFileUI():
    root = Tk()
    filname = filedialog.askopenfilename(title = "Select A File")
    print(filname)
    root.destroy()
    try:
        addFile(str(filname).split("/")[-1], filname)
    except:
        pass
