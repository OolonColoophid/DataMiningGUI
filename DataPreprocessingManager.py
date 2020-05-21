from tkinter import *
import numpy as np
import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer


class DataPreprocessingManager:
    def __init__(self, mainframe, dataframe=None, feature_list=None):
        self.mainframe = mainframe
        self.window = None
        self.frame = None
        self.dataframe = dataframe
        self.altered_dataframe = None
        self.feature_list = feature_list
        self.checkbox_list = []

    def create(self):
        if self.mainframe.importExportDataManager.get_filename() is not None:
            self.window = Tk()
            self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)
            self.window.title("Replace missing feature values")
            self.frame = Frame(self.window)
            self.set_dataframe(self.mainframe.importExportDataManager.get_data())
            self.set_feature_list(self.mainframe.importExportDataManager.get_column_names())
            self.set_checkbox_list()
            self.window.deiconify()
            win_height = len(self.feature_list) * 30
            self.window.geometry("300x" + str(win_height))
        else:
            print("No dataset loaded")

    def show_window(self):
        self.window.deiconify()

    def hide_window(self):
        self.window.iconify()

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

    def set_checkbox_list(self):
        if self.feature_list is not None:
            rowNumber = 0
            lblUserPrompt = Label(self.window, text="Select attributes with missing values: ")
            lblUserPrompt.grid(row=rowNumber, column=1)
            rowNumber += 1
            for x in self.feature_list:
                v = IntVar(self.window)
                checkbox = Checkbutton(self.window, text=str(x) + "\t" + str(self.get_dataframe()[x].dtype), variable=v)
                checkbox.var = v
                self.checkbox_list.append(checkbox)
                checkbox.grid(row=rowNumber, column=1, sticky="w")
                rowNumber += 1
            runButton = Button(self.window, text="Replace", command=self.run_button_action)
            runButton.grid(row=rowNumber, column=2)

    def run_button_action(self):
        selected_attributes = self.get_selected_attributes()
        self.remove_nan_values(selected_attributes)
        self.impute_data(selected_attributes)
        self.mainframe.importExportDataManager.save_data_as_csv_file(self.altered_dataframe)
        print("Success")

    def set_dataframe(self, dataframe):
        self.dataframe = dataframe

    def get_selected_attributes(self):
        selected_attributes = []
        for i in range(len(self.checkbox_list)):
            if self.checkbox_list[i].var.get() == 1:
                selected_attributes.append(self.feature_list[i])
        return selected_attributes

    def remove_nan_values(self, selected_attributes):
        # replace all zeros in selected columns with NaN
        self.dataframe[selected_attributes] = self.dataframe[selected_attributes].replace(['0', 0], np.nan)
        # removes all rows with NaN values in it
        self.altered_dataframe = self.dataframe.dropna()

    def impute_data(self, selected_attributes):
        # instantiates IterativeImputer
        imp = IterativeImputer(max_iter=100, random_state=0)
        # fit IterativeImputer to dataframe that does not contain missing values
        # @params X: which features to use to interpolate missing values?
        # @params y: which features to replace missing values
        X = self.altered_dataframe[self.feature_list]
        y = self.altered_dataframe[selected_attributes]
        imp.fit(X, y)
        self.altered_dataframe = pd.DataFrame(data=imp.transform(self.dataframe), columns=self.feature_list)
