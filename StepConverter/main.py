#! /usr/bin/env python


from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from OCC.Display.SimpleGui import init_display

from parser import Parser


def getFile():
    Tk().withdraw()
    return askopenfilename()

def getFiles():
    Tk().withdraw()
    dirName = askdirectory()
    return [path.join(dirName, f) for f in listdir(dirName) if path.isfile(path.join(dirName, f))]

def main():
    display,start_display, add_menu,add_functionto_menu = init_display()
    parser = Parser(display)
    parser.importStep()
    start_display()



if __name__ == '__main__':
    main()
