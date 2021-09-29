import gspread
from gspread_dataframe import set_with_dataframe, get_as_dataframe

class GoogleSheetsService:
    gc = None
    currWorkSheet = None
    currSpreadSheet = None

    def __init__(self, sheetUrl) -> None:
        self.gc = gspread.service_account()
        self.getSpreadSheet(sheetUrl)

    def getSpreadSheet(self, sheetUrl):
        self.currSpreadSheet = self.gc.open_by_url(sheetUrl)

    def getWorkSheet(self, index):
        self.currWorkSheet = self.currSpreadSheet.get_worksheet(index)

    def createNewWorkSheetFromDf(self, name, df):
        newWorkSheet = self.currSpreadSheet.add_worksheet(title=name, rows=10, cols= 10)
        set_with_dataframe(newWorkSheet, df)
    
    def getWorkSheetAsFrame(self, index):
        self.getWorkSheet(index)
        return get_as_dataframe(self.currWorkSheet)
    