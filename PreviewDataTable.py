from tkinter.ttk import Treeview
from tkinter import *


class PreviewDataTable:

    """
    PreviewDataTable
    show the user the head of the data that they have imported
    @methods:
    ----------
    update_table: remove column names and rows, get column names from ImportDataManager, append data to each row
    Problem: treeview is resizing to the width of the screen size, when it's told explcitly not to (stretch=False)
    """

    def __init__(self, mainframe):
        self.mainframe = mainframe
        self.canvas = Canvas(self.mainframe.root)
        self.treeview = Treeview(mainframe.root)
        self.treeview['columns'] = ("column 1", "column 2", "column 3", "column 4", "column 5")
        self.treeview['show'] = 'headings'  # removes empty identifier column
        for column in self.treeview['columns']:
            self.treeview.heading(column, text=str(column), anchor="w")
            self.treeview.column(column, anchor="center", width=80, stretch=False)
        for i in range(5):
            self.treeview.insert('', 'end')
        self.treeview.bind('<Button-1>', self.handle_click)

    def update_table(self):
        # delete everything from treeview
        for child in self.treeview.get_children():
            self.treeview.delete(child)

        # insert new column names
        self.treeview['columns'] = self.mainframe.importDataManager.get_column_names()

        # insert data from head of pandas dataframe
        for i, j in self.mainframe.importDataManager.get_data_head().iterrows():
            append_data = []
            for k in j:
                append_data.append(k)
            self.treeview.insert('', 'end', value=append_data)

        for column in self.treeview['columns']:
            self.treeview.heading(column, text=str(column), anchor="w")
            self.treeview.column(column, anchor="center", width=80, stretch=False)

    # makes columns unresizeable
    def handle_click(self, event):
        if self.treeview.identify_region(event.x, event.y) == "separator":
            return "break"
