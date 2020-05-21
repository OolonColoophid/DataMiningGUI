from tkinter.ttk import Combobox, Treeview
from tkinter import *

from DiscretizationManager import DiscretizationManager
from ImportExportDataManager import ImportExportDataManager
from DataPreprocessingManager import DataPreprocessingManager
from OptionsWindow import OptionsWindow
from PreviewDataTable import PreviewDataTable


class Mainframe(Frame):
    """
    Multiple Docuement Interface
    Everything in the application stems from the mainframe
    """

    def __init__(self, root):
        self.root = root

        self.importExportDataManager = ImportExportDataManager(self)
        self.dataPreprocessingManager = DataPreprocessingManager(self)
        self.discretizationManager = DiscretizationManager(self)
        self.optionsWindow = OptionsWindow(self)
        self.frame = Frame(root)

        # create menu bar
        self.menubar = Menu(root)
        root.config(menu=self.menubar)
        self.fileMenu = Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="File", menu=self.fileMenu)
        self.fileMenu.add_command(label="Import data...", command=self.importExportDataManager.set_filename)
        self.fileMenu.add_command(label="Options...", command=self.optionsWindow.create)
        self.dataMenu = Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="Data", menu=self.dataMenu)
        self.dataMenu.add_command(label="Replace missing values...", command=self.dataPreprocessingManager.create)
        self.dataMenu.add_command(label="Discretize data...", command=self.discretizationManager.create)

        # create labels
        self.lblReduceFeatures = Label(self.frame, text="Reduce Features?")
        self.lblInterpolateMissingValues = Label(self.frame, text="Interpolate missing values?")
        self.lblAttributes = Label(self.frame, text="Select class label: ")
        self.lblAlgorithm = Label(self.frame, text="Select algorithm: ")

        # create comboboxes
        self.cmbReduceFeatures = Combobox(self.frame, state="readonly", values=["Yes", "No"], width=5)
        self.cmbInterpolateMissingValues = Combobox(self.frame, state="readonly", values=["Yes", "No"], width=5)
        self.cmbAttributes = Combobox(self.frame, state="readonly")
        self.cmbAlgorithm = Combobox(self.frame, state="readonly", values=["Logistic Regression",
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
        self.frame.grid(row=rowNumber, column=1, sticky=W)
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

        separator1 = Label(root, text="")
        separator1.grid(row=rowNumber, column=1)
        rowNumber += 1

        self.previewDataTable.treeview.grid(row=rowNumber, column=1,
                                            rowspan=self.previewDataTable.treeview.winfo_width(),
                                            columnspan=2, sticky=W)
        rowNumber += 1
        separator2 = Label(root, text="")
        separator2.grid(row=rowNumber, column=1)
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
        print(self.importExportDataManager.summary())
