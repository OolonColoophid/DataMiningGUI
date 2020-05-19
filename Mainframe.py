from tkinter.ttk import Combobox
from tkinter import *

from ImportDataManager import ImportDataManager

global rowNumber


def getReduceFeatureOption():
    return cmbReduceFeatures.get()


def getInterpolateMissingValuesOption():
    return cmbInterpolateMissingValues.get()


def getSelectedClassLabel():
    return cmbAttributes.get()


def getSelectedAlgorithm():
    return cmbAlgorithm.get()


# when data is loaded into ImportDataManager, updates comboox with column names
def update_attribute_list(event):
    column_names = importDataManager.get_column_names()
    cmbAttributes['values'] = column_names
    if importDataManager.get_column_names() is not None and len(importDataManager.get_column_names()) > 0:
        cmbAttributes.set(column_names[0])


def getSelectedUserParams(event):
    print("Reduce features: " + getReduceFeatureOption())
    print("Interpolate missing values: " + getInterpolateMissingValuesOption())
    print("Class label: " + getSelectedClassLabel())
    print("Selected algorithm: " + getSelectedAlgorithm())
    print(importDataManager.summary())


root = Tk()
root.title("Focking")

# create import data manager
importDataManager = ImportDataManager()

# create menu bar
menu = Menu(root)
root.config(menu=menu)
fileMenu = Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Import data...", command=importDataManager.set_filename)

# create labels
lblReduceFeatures = Label(root, text="Reduce Features?")
lblInterpolateMissingValues = Label(root, text="Interpolate missing values?")
lblAttributes = Label(root, text="Select class label: ")
lblAlgorithm = Label(root, text="Select algorithm: ")

# create comboboxes
cmbReduceFeatures = Combobox(root, state="readonly", values=["Yes", "No"], width=5)
cmbInterpolateMissingValues = Combobox(root, state="readonly", values=["Yes", "No"], width=5)
cmbAttributes = Combobox(root, state="readonly")
cmbAttributes.bind("<Button-1>", update_attribute_list)
cmbAlgorithm = Combobox(root, state="readonly", values=["Logistic Regression",
                                                        "Decision Tree",
                                                        "Support Vector Machine",
                                                        "Naive Bayes",
                                                        "Random Forest"])

# set default combobox values
cmbReduceFeatures.set("No")
cmbInterpolateMissingValues.set("No")
cmbAlgorithm.set("Logistic Regression")

# create buttons
runButton = Button(text="Run", width=10)
runButton.bind("<Button-1>", getSelectedUserParams)

# set grid layout
rowNumber = 0
lblReduceFeatures.grid(row=rowNumber, column=1)
cmbReduceFeatures.grid(row=rowNumber, column=2)
rowNumber += 1
lblInterpolateMissingValues.grid(row=rowNumber, column=1)
cmbInterpolateMissingValues.grid(row=rowNumber, column=2)
rowNumber += 1
lblAttributes.grid(row=rowNumber, column=1)
cmbAttributes.grid(row=rowNumber, column=2)
rowNumber += 1
lblAlgorithm.grid(row=rowNumber, column=1)
cmbAlgorithm.grid(row=rowNumber, column=2)
rowNumber += 1
runButton.grid(row=rowNumber, column=1)
rowNumber += 1

root.mainloop()
