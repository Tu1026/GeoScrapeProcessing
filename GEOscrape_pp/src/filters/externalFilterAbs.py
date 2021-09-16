### This is an abstract filter class for filers that relies on some parsing from other services
import pandas as pd
import re
import time
from misc.misc import formatTime
from tqdm import tqdm

class Filter:
    df = None
    ## The relevantFields used by the type of filter
    relevantFields = []
    filterType = ""
    text_columns = None
    resultColumn = ""


    def __init__(self, df, filterType, relevantFields) -> None:
        print(f'Initiaing {self.filterType} filter')
        tqdm.pandas()
        self.df = df
        self.filterType = filterType
        self.relevantFields = relevantFields
        self.resultColumn = f'{self.filterType} Filter Results'


    def extractTextColumn(self):
        self.cleanColumns()
        print(f"Getting text from output column {self.relevantFields}. Please make sure they are correct")
        self.text_columns = self.df.iloc[self.df.columns & self.relevantFields]
    

    def cleanColumns(self):
        self.df = self.df[self.df.iloc[:,1]!= '']


    ### Filter by only using the outputs in Paul's listGEO -> Try out how many false negatives and we can try entrez api?
    def filterTerms(self, terms, failedReason, successReason):
        print(f"Filtering {self.filterType}")
        self.extractTextColumn()
        start = time.time()
        self.df[self.resultColumn] = self.df.progress_apply(lambda row: self._filterTerms(row, terms,failedReason, successReason), axis=1)
        stop = time.time()
        print(f'Filtering {self.filterType} took {formatTime(start, stop)} seconds')


    def returnFrame(self):
        return self.df

    ### Private implementation of filterTerms
    def _filterTerms(self, row, terms, faileReason, successReason):
        for column in self.text_columns:
            if not pd.isna(row[column]):
                if re.search(terms, str(row[column]), re.IGNORECASE):
                    return (f'(Failure) {faileReason}')
        return (f'(Success) {successReason}')
    
    