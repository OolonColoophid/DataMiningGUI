from tkinter.ttk import Combobox, Treeview
from tkinter import *

from ImportDataManager import ImportDataManager
from PreviewDataTable import PreviewDataTable


class Mainframe(Frame):
    """
    Multiple Docuement Interface
    Everything in the application stems from the mainframe
    """

    def __init__(self, root):
        self.root = root
        self.importDataManager = ImportDataManager(self)

        # create menu bar
        self.menubar = Menu(root)
        root.config(menu=self.menubar)
        self.fileMenu = Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="File", menu=self.fileMenu)
        self.fileMenu.add_command(label="Import data...", command=self.importDataManager.set_filename)

        # create labels
        self.lblReduceFeatures = Label(root, text="Reduce Features?")
        self.lblInterpolateMissingValues = Label(root, text="Interpolate missing values?")
        self.lblAttributes = Label(root, text="Select class label: ")
        self.lblAlgorithm = Label(root, text="Select algorithm: ")

        # create comboboxes
        self.cmbReduceFeatures = Combobox(root, state="readonly", values=["Yes", "No"], width=5)
        self.cmbInterpolateMissingValues = Combobox(root, state="readonly", values=["Yes", "No"], width=5)
        self.cmbAttributes = Combobox(root, state="readonly")
        self.cmbAlgorithm = Combobox(root, state="readonly", values=["Logistic Regression",
                                                                     "Decision Tree",
                                                                     "Support Vector Machine",
                                                                     "Naive Bayes",
                                                                     "Random Forest"])

        # set default combobox values
        self.cmbReduceFeatures.set("No")
        self.cmbInterpolateMissingValues.set("No")
        self.cmbAlgorithm.set("Logistic Regression")

        # create preview data table
        self.previewDataTable = PreviewDataTable(self)

        # create buttons
        self.runButton = Button(text="Run", width=10)
        self.runButton.bind("<Button-1>", self.getSelectedUserParams)

        # set grid layout
        rowNumber = 0
        self.lblReduceFeatures.grid(row=rowNumber, column=1, sticky=W)
        self.cmbReduceFeatures.grid(row=rowNumber, column=2, sticky=W)
        rowNumber += 1
        self.lblInterpolateMissingValues.grid(row=rowNumber, column=1, sticky=W)
        self.cmbInterpolateMissingValues.grid(row=rowNumber, column=2, sticky=W)
        rowNumber += 1
        self.lblAttributes.grid(row=rowNumber, column=1, sticky=W)
        self.cmbAttributes.grid(row=rowNumber, column=2, sticky=W)
        rowNumber += 1
        self.lblAlgorithm.grid(row=rowNumber, column=1, sticky=W)
        self.cmbAlgorithm.grid(row=rowNumber, column=2, sticky=W)
        rowNumber += 1

        self.previewDataTable.treeview.grid(row=rowNumber, column=1,
                                            rowspan=self.previewDataTable.treeview.winfo_width(),
                                            columnspan=2, sticky=W)
        rowNumber += 1

        self.runButton.grid(row=rowNumber, column=1)
        rowNumber += 1

    def getReduceFeatureOption(self):
        return self.cmbReduceFeatures.get()

    def getInterpolateMissingValuesOption(self):
        return self.cmbInterpolateMissingValues.get()

    def getSelectedClassLabel(self):
        return self.cmbAttributes.get()

    def getSelectedAlgorithm(self):
        return self.cmbAlgorithm.get()

    def getSelectedUserParams(self, event):
        print("Reduce features: " + self.getReduceFeatureOption())
        print("Interpolate missing values: " + self.getInterpolateMissingValuesOption())
        print("Class label: " + self.getSelectedClassLabel())
        print("Selected algorithm: " + self.getSelectedAlgorithm())
        print(self.importDataManager.summary())
