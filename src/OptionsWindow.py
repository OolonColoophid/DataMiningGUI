from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox


class OptionsWindow:

    def __init__(self, mainframe):
        self.mainframe = mainframe
        self.window = None
        self.frame = None
        self.cmbDecimalPlaces = None
        self.cmbKFoldCrossVal = None
        self.applyButton = None
        self.settings = {"decimal places": 2,
                         "k-fold cross validation": 10}

    def create(self):
        self.window = Tk()
        self.frame = Frame(self.window)
        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)
        self.window.title("Import data options")
        self.window.geometry("300x300")

        rowNumber = 0
        Label(self.window, text="").grid(row=rowNumber, column=1)
        rowNumber += 1
        Label(self.window, text="Decimal places: ").grid(row=rowNumber, column=1)
        self.cmbDecimalPlaces = Combobox(self.window, width=5, values=['1', '2', '3', '4', '5'])
        self.cmbDecimalPlaces.grid(row=rowNumber, column=2)
        self.cmbDecimalPlaces.set(self.settings.get("decimal places"))
        rowNumber += 1
        Label(self.window, text="").grid(row=rowNumber, column=1)
        rowNumber += 1
        lblKFoldCrossVal = Label(self.window, text="K_cross_validate: ").grid(row=rowNumber, column=1)
        self.cmbKFoldCrossVal = Combobox(self.window, width=5, values=['5', '10', '20'])
        self.cmbKFoldCrossVal.grid(row=rowNumber, column=2)
        self.cmbKFoldCrossVal.set(self.settings.get("k-fold cross validation"))
        rowNumber += 1
        Label(self.window, text="").grid(row=rowNumber, column=1)
        rowNumber += 1
        self.applyButton = Button(self.window, text="Apply changes", command=self.apply_changes)
        self.applyButton.grid(row=rowNumber, column=2, sticky="s")

    def apply_changes(self):
        self.window.attributes("-topmost", 1)
        messageBox = messagebox.askquestion(self.window, "Apply changes?")
        self.window.deiconify()
        if messageBox == 'yes':
            self.settings["decimal places"] = self.cmbDecimalPlaces.get()
            self.settings["k-fold cross validation"] = self.cmbKFoldCrossVal.get()
            self.mainframe.previewDataTable.update_table(self.mainframe.importExportDataManager.get_data())
            self.window.attributes("-topmost", 0)
            self.window.withdraw()
        else:
            pass
