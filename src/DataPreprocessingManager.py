from tkinter import *

import numpy as np
import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer


class DataPreprocessingManager:
    """
    DataPreprocessingManager
    Allows user to preprocess the data using multivariate feature imputation
    User selects attributes with missing values to replace
    IterativeImputer fills missing values based on other attributes in instance
    """

    def __init__(self, mainframe, dataframe=None, feature_list=None):
        self.mainframe = mainframe
        self.window = None
        self.dataframe = dataframe
        self.altered_dataframe = None
        self.feature_list = feature_list
        self.checkbox_list = []

    def create(self):
        if self.mainframe.importExportDataManager.get_filename() is not None:
            self.window = Toplevel(self.mainframe.root)
            self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)
            self.window.title("Replace missing feature values")
            self.set_dataframe(self.mainframe.importExportDataManager.get_data())
            self.set_feature_list(self.mainframe.importExportDataManager.get_column_names())
            self.set_layout()
            self.window.geometry("300x" + str((len(self.get_feature_list()) * 30) + 100))
        else:
            print("No dataset loaded")

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
            Label(self.window, text="").grid(row=rowNumber, column=0)
            rowNumber += 1
            Label(self.window, text="Select attributes with missing values: ").grid(row=rowNumber, column=0)
            rowNumber += 1
            for x in self.feature_list:
                v = IntVar(self.window)
                checkbox = Checkbutton(self.window, text=str(x) + "\t" + str(self.get_dataframe()[x].dtype), variable=v)
                checkbox.grid(row=rowNumber, column=0, sticky="w")
                checkbox.var = v
                self.checkbox_list.append(checkbox)
                rowNumber += 1

            Label(self.window, text="").grid(row=rowNumber, column=0)
            rowNumber += 1
            Button(self.window, text="Replace", command=self.run_button_action).grid(row=rowNumber, column=0)
            rowNumber += 1
            Label(self.window, text="").grid(row=rowNumber, column=0)

    def run_button_action(self):
        selected_attributes = self.get_selected_attributes()
        self.remove_nan_values(selected_attributes)
        self.impute_data(selected_attributes)
        self.altered_dataframe = self.format_data(self.altered_dataframe)
        self.mainframe.importExportDataManager.save_data_as_csv_file(self.altered_dataframe)

    def set_dataframe(self, dataframe):
        self.dataframe = dataframe

    def get_selected_attributes(self):
        selected_attributes = []
        for i in range(len(self.checkbox_list)):
            if self.checkbox_list[i].var.get() == 1:
                selected_attributes.append(self.feature_list[i])
        return selected_attributes

    def remove_nan_values(self, selected_attributes):
        self.dataframe[selected_attributes] = self.dataframe[selected_attributes].replace(['0', 0], np.nan)
        self.altered_dataframe = self.dataframe.dropna()

    def impute_data(self, selected_attributes):
        """
        X: which features to use to interpolate missing values
        y: which features to replace missing values
        """
        imp = IterativeImputer(max_iter=100, random_state=0)
        X = self.altered_dataframe[self.feature_list]
        y = self.altered_dataframe[selected_attributes]
        imp.fit(X, y)
        self.altered_dataframe = pd.DataFrame(data=imp.transform(self.dataframe), columns=self.feature_list)

    def format_data(self, df):
        for column in df.columns:
            if df[column].dtype == "float64":
                df = df.round({column: int(self.mainframe.optionsWindow.settings.get("decimal places"))})
        return df
