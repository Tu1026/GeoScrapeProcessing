class Filter:
    df = None

    ## Which column starts containing useful text, 12 for now
    text_index_start = 12
    ## Which column stops containing useful text, 15 for now
    text_index_stop = 15
    def __init__(self, df) -> None:
        pass

    def extractTextColumn(self):
        return self.df.iloc[:self.text_index_start, self.text_index_stop]

    ### Filter by only using the outputs in Paul's listGEO -> Try out how many false negatives and we can try entrez api?
    def filterTerms(self, terms):
        