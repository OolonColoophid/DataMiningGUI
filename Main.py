from tkinter import *
from Mainframe import Mainframe


def main():
    root = Tk()
    root.title("Focking")
    root.geometry("600x400")
    Mainframe(root)
    root.mainloop()


if __name__ == '__main__':
    main()