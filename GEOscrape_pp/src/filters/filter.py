import pandas as pd
import re
import time
from misc.misc import formatTime
from tqdm import tqdm

class Filter:
    df = None
    ## Which column starts containing useful text, 11 for now
    text_index_start = 11
    ## Which column stops containing useful text, 15 for now
    text_index_stop = 15

    filterType = ""
    text_columns = None
    resultColumn = ""

    def __init__(self, df, filterType) -> None:
        print(f'Initiaing {self.filterType} filter')
        tqdm.pandas()
        self.df = df
        self.filterType = filterType
        self.resultColumn = f'{self.filterType} Filter Results'

    def extractTextColumn(self):
        self.cleanColumns()
        print(f"Getting text from output column {self.text_index_start} - {self.text_index_stop}. Please make sure they are correct")
        self.text_columns = self.df.iloc[:,self.text_index_start:self.text_index_stop]
    
    def cleanColumns(self):
        self.df = self.df[self.df.iloc[:,1]!= '']

    ### Filter by only using the outputs in Paul's listGEO -> Try out how many false negatives and we can try entrez api?
    def filterTerms(self, terms, failed_info):
        print(f"Filtering {self.filterType}")
        self.extractTextColumn()
        start = time.time()
        self.df[self.resultColumn] = self.df.progress_apply(lambda row: self._filterTerms(row, terms,failed_info), axis=1)
        stop = time.time()
        print(f'Filtering {self.filterType} took {formatTime(start, stop)} seconds')

    def returnFrame(self):
        return self.df

    def _filterTerms(self, row, terms, failed_info):
        for column in self.text_columns:
            if not pd.isna(row[column]):
                if re.search(terms, row[column], re.IGNORECASE):
                    return (f'Something is wrong with {failed_info}. Double check the experiment again may not be supported.')
        return ("Passed filter")
    
    
