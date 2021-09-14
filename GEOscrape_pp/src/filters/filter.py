import pandas as pd
import re
import time
class Filter:
    df = None
    ## Which column starts containing useful text, 12 for now
    text_index_start = 12
    ## Which column stops containing useful text, 15 for now
    text_index_stop = 15
    filterType = ""

    def __init__(self, df, filterType) -> None:
        print(f'Initiaing {self.filterType} filter')
        self.df = df
        self.filterType = filterType

    def extractTextColumn(self):
        return self.df.iloc[:self.text_index_start, self.text_index_stop]

    ### Filter by only using the outputs in Paul's listGEO -> Try out how many false negatives and we can try entrez api?
    def filterTerms(self, terms, failed_info):
        print(f"Filtering {self.filterType}")
        self.df[self.filterType] = self.df
    
    ### Private implementation of filterTerms method
    def _filterTerms(self, terms, failed_info):
        text_columns = self.extractTextColumn()
        for _, row in text_columns.iterrows():
            for column in text_columns:
                if re.search(terms, row[column], re.IGNORECASE):
                    return (f'{failed_info}. Double check the experiment again may not be supported.')
    
