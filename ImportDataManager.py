from tkinter.filedialog import askopenfilename

# need xlrd library to handle .xls and .xlsx data import
import xlrd

# convert data in all filetypes into pandas DataFrame
import pandas as pd


class ImportDataManager:
    """
    ImportDataManager used to import data into the application
    @params
    --------
    filename: operating system path to the file containing data to be imported
    data: converted into a pandas DataFrame
    column_names: the columns of the data that is imported
    """

    def __init__(self, filename=None, column_names=None, data=None):
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

    # used to show the first five rows of data to the user
    # when the data has been imported, update table to contain first five rows of data
    def get_data_head(self):
        if isinstance(self.data, pd.DataFrame):
            return self.data.head()

    # returns the column names of the imported data
    # user selects the class label for the algorithms
    def get_column_names(self):
        return self.column_names

    def summary(self):
        print(self.get_filename())
        print(self.get_column_names())
        print(self.get_data_head())

    def set_filename(self):
        filename = askopenfilename()
        if filename != '':
            self.filename = filename
        else:
            self.filename = None
        self.set_data()
        self.set_column_names()

    def set_data(self):
        if self.get_filename() != '':
            self.data = self.load_data()

    def set_column_names(self):
        if isinstance(self.get_data(), pd.DataFrame):
            self.column_names = list(self.get_data().columns)

    def load_data(self):
        # if user has selected a .csv file, use pd.read_csv
        try:
            if self.get_filename()[-3:] == "csv" and self.get_filename() is not None:
                df = pd.read_csv(self.get_filename())
            # if user has selected a Microsoft Excel file, use pd.read_excel
            elif self.get_filename()[-3:] == "xls" or self.get_filename()[-4:] == "xlsx":
                df = pd.read_excel(str(self.get_filename()))
            else:
                pass
            return df
        except TypeError:
            print("Data import cancelled")
