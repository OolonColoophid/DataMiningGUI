from tkinter import *
from tkinter.ttk import Combobox


class OptionsWindow:

    def __init__(self, mainframe):
        self.mainframe = mainframe
        self.window = None
        self.frame = None
        self.lblDecimalPlaces = None
        self.cmbDecimalPlaces = None
        self.applyButton = None
        self.settings = {"decimal places": 2}

    def create(self):
        self.window = Tk()
        self.frame = Frame(self.window)
        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)
        self.window.title("Import data options")
        self.window.geometry("300x300")
        rowNumber = 0
        # create widgets
        self.lblDecimalPlaces = Label(self.window, text="Decimal places: ")
        self.cmbDecimalPlaces = Combobox(self.window, width=5, values=['1', '2', '3', '4', '5'])
        self.cmbDecimalPlaces.set(self.settings.get("decimal places"))
        self.applyButton = Button(self.window, text="Apply changes", command=self.apply_changes)
        # widget layout
        separator1 = Label(self.window, text="")
        separator1.grid(row=rowNumber, column=1)
        rowNumber += 1
        self.lblDecimalPlaces.grid(row=rowNumber, column=1)
        self.cmbDecimalPlaces.grid(row=rowNumber, column=2)
        rowNumber += 1
        separator2 = Label(self.window, text="")
        separator2.grid(row=rowNumber, column=1)
        rowNumber += 1
        self.applyButton.grid(row=rowNumber, column=2, sticky="s")

    def apply_changes(self):
        self.settings["decimal places"] = self.cmbDecimalPlaces.get()
        self.mainframe.importExportDataManager.update_data()
        self.window.withdraw()