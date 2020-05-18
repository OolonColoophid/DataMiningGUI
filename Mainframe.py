from tkinter.ttk import Combobox
from tkinter import *

from ImportDataManager import ImportDataManager

root = Tk()
root.title("Focking")

# create import data manager
importDataManager = ImportDataManager()

# create menu bar
menu = Menu(root)
root.config(menu=menu)
fileMenu = Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Import data...", command=importDataManager.setFileName)

# create labels
lblReduceFeatures = Label(root, text="Reduce Features?")
lblInterpolateMissingValues = Label(root, text="Interpolate missing values?")
lblAlgorithm = Label(root, text="Algorithm: ")

# create comboboxes
cmbReduceFeatures = Combobox(root, state="readonly", values=["Yes", "No"], width=5)
cmbInterpolateMissingValues = Combobox(root, state="readonly", values=["Yes", "No"], width=5)
cmbAlgorithm = Combobox(root, state="readonly", values=["Logistic Regression",
                                                        "Decision Tree",
                                                        "Support Vector Machine",
                                                        "Naive Bayes",
                                                        "Random Forest"])

# set default combobox value
cmbReduceFeatures.set("No")
cmbInterpolateMissingValues.set("No")
cmbAlgorithm.set("Logistic Regression")


def getReduceFeatureOption():
    return cmbReduceFeatures.get()


def getInterpolateMissingValuesOption():
    return cmbInterpolateMissingValues.get()


def getSelectedAlgorithm():
    return cmbAlgorithm.get()


def getSelectedUserParams(event):
    print("Reduce features: " + getReduceFeatureOption())
    print("Interpolate missing values: " + getInterpolateMissingValuesOption())


# create buttons
runButton = Button(text="Run")
runButton.bind("<Button-1>", getSelectedUserParams)

# set grid layout

lblReduceFeatures.grid(row=1, column=1)
cmbReduceFeatures.grid(row=1, column=2)

lblInterpolateMissingValues.grid(row=2, column=1)
cmbInterpolateMissingValues.grid(row=2, column=2)

lblAlgorithm.grid(row=3, column=1)
cmbAlgorithm.grid(row=3, column=2)

runButton.grid(row=4, column=1)

root.mainloop()
