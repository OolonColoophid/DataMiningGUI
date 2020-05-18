from tkinter.filedialog import askopenfilename


class ImportDataManager:
    def __init__(self, fileName=None):
        self.fileName = fileName

    def setFileName(self):
        fileName = askopenfilename()
        self.fileName = fileName
        print(str(fileName))

    def getFileName(self):
        return self.fileName
