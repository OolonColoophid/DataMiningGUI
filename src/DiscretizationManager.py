from tkinter import messagebox

import pandas as pd
import sklearn
from sklearn.tree import DecisionTreeClassifier, _tree
import matplotlib.pyplot as plt
from tkinter import *
import numpy as np
from collections import Counter


class DiscretizationManager:
    """
    DiscretizationManager
    Allows user to turn continuous attributes into categorical attributes
    E.g. real values 30-50, plot data, allow user to select ranges for categories
    Use decision tree to discretize invididual attributes
    """
    def __init__(self, mainframe, dataframe=None, feature_list=None):
        self.mainframe = mainframe
        self.window = None
        self.decisionTree = None
        self.dataframe = dataframe
        self.altered_dataframe = None
        self.feature_list = feature_list
        self.checkbox_list = []

    def create(self):
        if self.mainframe.importExportDataManager.get_data() is None:
            messagebox.showinfo("Information", "No data selected")
            pass
        elif self.mainframe.getSelectedClassLabel() == "":
            messagebox.showinfo("Information", "Class label not selected")
            pass
        else:
            self.window = Tk()
            self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)
            self.window.title("Discretize attributes")
            if isinstance(self.mainframe.dataPreprocessingManager.altered_dataframe, pd.DataFrame):
                self.set_dataframe(self.mainframe.dataPreprocessingManager.get_altered_dataframe())
            else:
                self.set_dataframe(self.mainframe.importExportDataManager.get_data())
            self.set_feature_list(list(self.dataframe.columns))
            self.set_layout()
            self.window.geometry("300x" + str(len(self.get_feature_list())*30+100))

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
            Label(self.window, text="Select attributes to discretize: ").grid(row=rowNumber, column=1)
            rowNumber += 1
            for x in self.feature_list:
                v = IntVar(self.window)
                if str(x) == str(self.mainframe.getSelectedClassLabel()):
                    checkbox = Checkbutton(self.window, text=str(x) + "\t" + " ** Selected class label ** ", variable=v, state=DISABLED)
                    self.count_class_number(self.dataframe, self.mainframe.getSelectedClassLabel())
                else:
                    checkbox = Checkbutton(self.window, text=str(x), variable=v)
                checkbox.var = v
                self.checkbox_list.append(checkbox)
                checkbox.grid(row=rowNumber, column=1, sticky="w")
                rowNumber += 1

            runButton = Button(self.window, text="Apply", command=self.discretize_data)
            runButton.grid(row=rowNumber, column=2)
            rowNumber += 1
            Label(self.window, text="").grid(row=rowNumber, column=1)

    def set_dataframe(self, dataframe):
        self.dataframe = dataframe

    def count_class_number(self, dataframe, class_label):
        values = dataframe[class_label].value_counts().keys().tolist()
        counts = dataframe[class_label].value_counts().tolist()
        value_dict = dict(zip(values, counts))
        return value_dict

    def get_selected_attributes(self):
        selected_attributes = []
        for i in range(len(self.checkbox_list)-1):
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
            self.tree_to_code(self.decisionTree, attribute)
            dict_labels = self.count_class_number(self.get_dataframe(), class_label)
            plt.figure()
            sklearn.tree.plot_tree(self.decisionTree,
                                   feature_names=[str(attribute)],
                                   class_names=list(self.mainframe.importExportDataManager.class_labels.keys()))
            plt.title(attribute)
            self.window.withdraw()
        # plt.show()

    def tree_to_code(self, tree, attribute):
        tree_ = self.decisionTree.tree_
        feature_names = [attribute]

        def recurse(node, depth):
            indent = "  " * depth
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_names[0]
                threshold = tree_.threshold[node]
                print("%s if %s <= %.1f:" % (indent, name, threshold))
                recurse(tree_.children_left[node], depth + 1)
                print("%s else if %s > %.1f" % (indent, name, threshold))
                recurse(tree_.children_right[node], depth + 1)
            else:
                label = str(tree.classes_[np.argmax(tree_.value[node])])
                p = tree_.value[node].max() / tree_.n_node_samples[node]
                print("%s %s (p=%.2f)" % (indent, label, p.round(decimals=2)))
        recurse(0, 1)
