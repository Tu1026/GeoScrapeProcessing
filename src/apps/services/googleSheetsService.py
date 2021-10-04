import gspread
from gspread_dataframe import set_with_dataframe 
import pandas as pd

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
        try:
            newWorkSheet = self.currSpreadSheet.add_worksheet(title=name, rows=10, cols= 10)
            set_with_dataframe(newWorkSheet, df)
        except gspread.exceptions.APIError:
            set_with_dataframe(self.currSpreadSheet.worksheet(name),df) 
    
    def getWorkSheetAsFrame(self, index):
        self.getWorkSheet(index)
        return pd.DataFrame(self.currWorkSheet.get_values()[1:], columns= self.currWorkSheet.row_values(1))
        

    