from tkinter import *
from Mainframe import Mainframe


def main():
    root = Tk()
    root.title("Focking")
    root.geometry("600x400")
    Mainframe(root)
    root.protocol("WM_DELETE_WINDOW", sys.exit)
    root.mainloop()


if __name__ == '__main__':
    main()