from tkinter import filedialog
from tkinter.filedialog import askopenfilename
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

    def __init__(self, mainframe, filename=None, column_names=None, dataframe=None):
        self.mainframe = mainframe
        self.filename = filename
        self.column_names = column_names
        self.dataframe = dataframe
        self.class_labels = {}

    def get_filename(self):
        return self.filename

    def get_data(self):
        if isinstance(self.dataframe, pd.DataFrame):
            return self.dataframe

    def get_data_head(self):
        if isinstance(self.dataframe, pd.DataFrame):
            return self.dataframe.head()

    def get_column_names(self):
        return self.column_names

    def set_filename(self):
        filename = askopenfilename()
        if self.valid_file(filename):
            self.filename = filename
            self.update_data()
        else:
            self.filename = None

    def set_data(self, dataframe=None):
        if dataframe is None:
            if self.valid_file(self.get_filename()):
                self.dataframe = self.load_data()
        else:
            if isinstance(dataframe, pd.DataFrame):
                self.dataframe = dataframe

    def set_column_names(self):
        if isinstance(self.get_data(), pd.DataFrame):
            self.column_names = list(self.get_data().columns)
            self.set_class_labels(self.get_data())

    # load data into application as Pandas dataframe
    def load_data(self):
        df = None
        try:
            # if user has selected a .csv file
            if self.get_filename()[-3:] == "csv":
                df = pd.read_csv(self.get_filename())
            # if user has selected a Microsoft Excel file
            elif self.get_filename()[-3:] == "xls" or self.get_filename()[-4:] == "xlsx":
                df = pd.read_excel(str(self.get_filename()))
            return df
        except TypeError:
            print("Data import cancelled")

    def set_class_labels(self, df):
        if isinstance(self.get_data(), pd.DataFrame):
            for column in df.columns:
                if df[column].dtype == "object":
                    unique_values = df[column].unique()
                    for idx, label in enumerate(unique_values):
                        self.class_labels.update({label : idx})

    def update_data(self, dataframe=None):
        prev_class_label = self.mainframe.getSelectedClassLabel()
        if dataframe is None:
            self.set_data()
        else:
            if isinstance(dataframe, pd.DataFrame):
                self.set_data(dataframe)
        self.set_column_names()
        self.mainframe.cmbAttributes['values'] = self.get_column_names()
        if self.get_column_names() is not None and len(self.get_column_names()) > 0:
            if prev_class_label in self.get_column_names():
                self.mainframe.cmbAttributes.set(prev_class_label)
            else:
                self.mainframe.cmbAttributes.set(self.get_column_names()[0])
        self.mainframe.previewDataTable.update_table()

    def valid_file(self, filename):
        if filename is not None:
            if filename[-3:] == "csv" or \
                    filename[-3:] == "xls" or \
                    filename[-4:] == "xlsx":
                return True
        return False

    def save_data_as_csv_file(self, dataframe):
        if dataframe is not None:
            filename = filedialog.asksaveasfilename()
            if str(filename)[-4:] == ".csv":
                dataframe.to_csv(filename, index=False)
            else:
                dataframe.to_csv(filename + ".csv", index=False)
