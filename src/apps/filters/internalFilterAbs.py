### This is an abstract filter class for filers that rely on GEO output
import pandas as pd
import re
import time
import swifter
from apps.misc import formatTime
from tqdm import tqdm
from abc import ABC, abstractmethod 


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
        self.text_columns = df[df.columns & self.relevantFields]
        return df

    def cleanColumns(self, df):
        df = df[df.iloc[:,1]!= '']
        print(f"Please check if the below dataframe looks correct before filtering by {self.filterType}")
        print("\n\n ========================================These are the first 5 rows ========================================")
        print(df.head())
        print("\n\n ========================================These are the last 5 rows========================================")
        print(df.tail())
        return df


    @abstractmethod
    ### Filter by only using the outputs in Paul's listGEO -> Try out how many false negatives and we can try entrez api?
    def filterTerms(self, df, terms, failedReason, successReason):
        print(f"Filtering {self.filterType}")
        df = self.extractTextColumn(df)
        start = time.time()
        #df[self.resultColumn] = df.progress_apply(lambda row: self._filterTerms(row, terms,failedReason, successReason), axis=1)
        df[self.resultColumn] = df.swifter.allow_dask_on_strings(enable=True).apply(lambda row: self._filterTerms(row, terms,failedReason, successReason), axis=1)
        stop = time.time()
        print(f'Filtering {self.filterType} took {formatTime(start, stop)} seconds') 
        print(df.head())
        return df


    ### Private implementation of filterTerms
    def _filterTerms(self, row, terms, faileReason, successReason):
        if self.filterType == "hitWords":
            tempListOfWords = ""
            for column in self.text_columns:
                if not pd.isna(row[column]):
                    tempListOfWords = tempListOfWords + row[column]
            for term in terms:
                ## Sucess if a term is present in the text
                if re.search(term, tempListOfWords, re.IGNORECASE):
                    return (f'(Success) {successReason}')
            ## Failure if the no terms are in the text at all
            return (f'(Failure) {faileReason}')

        else:
            for column in self.text_columns:
                if not pd.isna(row[column]):
                    ## Failure if the term we don't want is in the text
                    if re.search(terms, str(row[column]), re.IGNORECASE):
                        return (f'(Failure) {faileReason}')
            ## Sucess if the term we don't want doesn't appear
            return (f'(Success) {successReason}')
    
    