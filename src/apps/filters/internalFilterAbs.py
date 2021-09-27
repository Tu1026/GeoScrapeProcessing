### This is an abstract filter class for filers that rely on GEO output
import pandas as pd
import re
import time
import swifter
from apps.misc import formatTime
from tqdm import tqdm
from abc import ABC, abstractclassmethod    


class InternalFilter(ABC):
    df = None
    ## The relevantFields used by the type of filter
    relevantFields = []
    filterType = ""
    text_columns = None
    resultColumn = ""


    def __init__(self, filterType, relevantFields) -> None:
        print(f'Initiaing {self.filterType} filter')
        tqdm.pandas()
        self.filterType = filterType
        self.relevantFields = relevantFields
        self.resultColumn = f'{self.filterType} Filter Results'


    def extractTextColumn(self, df):
        df = self.cleanColumns(df)
        print(f"Getting text from output column {self.relevantFields}. Please make sure they are correct")
        self.text_columns = df.iloc[df.columns & self.relevantFields]
    

    def cleanColumns(self, df):
        df = df[df.iloc[:,1]!= '']
        return df

    @abstractclassmethod
    ### Filter by only using the outputs in Paul's listGEO -> Try out how many false negatives and we can try entrez api?
    def filterTerms(self, df, terms, failedReason, successReason):
        print(f"Filtering {self.filterType}")
        self.extractTextColumn(df)
        start = time.time()
        #df[self.resultColumn] = df.progress_apply(lambda row: self._filterTerms(row, terms,failedReason, successReason), axis=1)
        df[self.resultColumn] = df.swifter.allow_dask_on_strings(enable=True).apply(lambda row: self._filterTerms(row, terms,failedReason, successReason), axis=1)
        stop = time.time()
        print(f'Filtering {self.filterType} took {formatTime(start, stop)} seconds')
        return df


    ### Private implementation of filterTerms
    def _filterTerms(self, row, terms, faileReason, successReason):
        if self.filterType == "hitWords":
            tempListOfWords = ""
            for column in self.text_columns:
                tempListOfWords = tempListOfWords + row[column].astype(str)
            for term in terms:
                if re.search(term, tempListOfWords, re.IGNORECASE):
                    return (f'(Failure) {faileReason}')
            return (f'(Success) {successReason}')

        else:
            for column in self.text_columns:
                if not pd.isna(row[column]):
                    if re.search(terms, str(row[column]), re.IGNORECASE):
                        return (f'(Failure) {faileReason}')
            return (f'(Success) {successReason}')
    
    