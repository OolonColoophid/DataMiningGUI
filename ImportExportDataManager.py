from tkinter import filedialog
from tkinter.filedialog import askopenfilename

# convert data in all filetypes into pandas DataFrame
from tkinter.messagebox import Message

import pandas as pd


class ImportExportDataManager:
    """
    ImportDataManager used to import data into the application
    @params
    --------
    filename: operating system path to the file containing data to be imported
    data: converted into a pandas DataFrame
    column_names: the columns of the data that is imported
    """

    def __init__(self, mainframe, filename=None, column_names=None, data=None):
        self.mainframe = mainframe
        self.filename = filename
        self.column_names = column_names
        self.data = data

    # returns the operating system filepath of the file imported
    def get_filename(self):
        return self.filename

    # return data only if it has been successfully converted into a pandas DataFrame
    def get_data(self):
        if isinstance(self.data, pd.DataFrame):
            return self.data

    # returns the column names and first five rows of the pandas dataframe
    def get_data_head(self):
        if isinstance(self.data, pd.DataFrame):
            return self.data.head()

    # returns the column names of the imported data
    def get_column_names(self):
        return self.column_names

    def summary(self):
        print("Filepath: " + str(self.get_filename()))
        print("Column names: " + str(self.get_column_names()))
        print(self.get_data_head())

    def set_filename(self):
        filename = askopenfilename()
        if filename != '':
            self.filename = filename
        else:
            self.filename = None
        self.update_data()

    def set_data(self):
        if self.valid_file():
            self.data = self.load_data()

    def set_column_names(self):
        if isinstance(self.get_data(), pd.DataFrame):
            self.column_names = list(self.get_data().columns)

    def load_data(self):
        # if user has selected a .csv file, use pd.read_csv
        try:
            if self.get_filename()[-3:] == "csv":
                df = pd.read_csv(self.get_filename())
                self.format_data(df)
                self.map_data(df)
            # if user has selected a Microsoft Excel file, use pd.read_excel
            elif self.get_filename()[-3:] == "xls" or self.get_filename()[-4:] == "xlsx":
                df = pd.read_excel(str(self.get_filename()))
                self.format_data(df)
                self.map_data(df)
            else:
                pass
            return df
        except TypeError:
            print("Data import cancelled")

    def format_data(self, df):
        for column in df.columns:
            if df[column].dtype == "float64":
                df.loc[:, column] = df.round({column: int(self.mainframe.optionsWindow.settings.get("decimal places"))})

    def map_data(self, df):
        for column in df.columns:
            if df[column].dtype == "object":
                unique_values = df[column].unique()
                mapping = {label: idx for idx, label in enumerate(unique_values)}
                df[column] = df[column].map(mapping)

    def update_data(self):
        self.set_data()
        self.set_column_names()
        self.mainframe.cmbAttributes['values'] = self.get_column_names()
        if self.get_column_names() is not None and len(self.get_column_names()) > 0:
            self.mainframe.cmbAttributes.set(self.column_names[0])
        self.mainframe.previewDataTable.update_table()

    def valid_file(self):
        if self.get_filename() is not None:
            if self.get_filename()[-3:] == "csv" or \
                    self.get_filename()[-3:] == "xls" or \
                    self.get_filename()[-4:] == "xlsx":
                return True
        return False

    def save_data_as_csv_file(self, dataframe):
        if dataframe is not None:
            filename = filedialog.asksaveasfilename()
            dataframe.to_csv(filename+".csv", index=False)