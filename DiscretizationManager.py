import sklearn
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
from tkinter import *
import numpy as np


class DiscretizationManager:

    def __init__(self, mainframe, dataframe=None, feature_list=None):
        self.mainframe = mainframe
        self.window = None
        self.frame = None
        self.decisionTree = None
        self.dataframe = dataframe
        self.altered_dataframe = None
        self.feature_list = feature_list
        self.checkbox_list = []

    def create(self):
        if self.mainframe.importExportDataManager.get_data() is None:
            print("No data loaded")
            pass
        elif self.mainframe.getSelectedClassLabel() == "":
            print("Class label not selected")
            pass
        else:
            self.window = Tk()
            self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)
            self.window.title("Discretize attributes")
            self.frame = Frame(self.window)
            self.set_dataframe(self.mainframe.importExportDataManager.get_data())
            self.set_feature_list(self.mainframe.importExportDataManager.get_column_names())
            self.set_layout()
            self.window.deiconify()
            win_height = len(self.feature_list) * 30
            self.window.geometry("300x" + str(len(self.get_feature_list())*35))

    def get_feature_list(self):
        return self.feature_list

    def get_checkbox_list(self):
        return self.checkbox_list

    def get_dataframe(self):
        return self.dataframe

    def get_altered_dataframe(self):
        return self.altered_dataframe

    def set_feature_list(self, feature_list):
        self.feature_list = feature_list

    def set_layout(self):
        if self.feature_list is not None:
            rowNumber = 0
            lblUserPrompt = Label(self.window, text="Select attributes to discretize: ")
            lblUserPrompt.grid(row=rowNumber, column=1)
            rowNumber += 1
            for x in self.feature_list:
                v = IntVar(self.window)
                if str(x) == str(self.mainframe.getSelectedClassLabel()):
                    checkbox = Checkbutton(self.window, text=str(x) + "\t" + " ** Selected class label ** ", variable=v, state=DISABLED)
                else:
                    checkbox = Checkbutton(self.window, text=str(x), variable=v)
                checkbox.var = v
                self.checkbox_list.append(checkbox)
                checkbox.grid(row=rowNumber, column=1, sticky="w")
                rowNumber += 1

            runButton = Button(self.window, text="Apply", command=self.discretize_data)
            runButton.grid(row=rowNumber, column=2)
            rowNumber += 1
            separator = Label(self.window, text="")
            separator.grid(row=rowNumber, column=1)

    def set_dataframe(self, dataframe):
        self.dataframe = dataframe

    def get_selected_attributes(self):
        selected_attributes = []
        for i in range(len(self.checkbox_list)):
            if self.checkbox_list[i].var.get() == 1:
                selected_attributes.append(self.feature_list[i])
        return selected_attributes

    def discretize_data(self):
        selected_attributes = self.get_selected_attributes()
        class_label = self.mainframe.getSelectedClassLabel()
        y = self.get_dataframe()[class_label]
        for attribute in selected_attributes:
            X = np.array(self.get_dataframe()[attribute])
            X = X.reshape(-1, 1)
            min_split = round(len(X)/10)
            min_samples = round(len(X)/20)
            self.decisionTree = DecisionTreeClassifier(max_depth=2,
                                                       min_samples_split=min_split,
                                                       min_samples_leaf=min_samples)
            self.decisionTree.fit(X, y)
            plt.figure()
            sklearn.tree.plot_tree(self.decisionTree,
                                   class_names=["positive", "negative"])
            plt.title(attribute)
        plt.show()