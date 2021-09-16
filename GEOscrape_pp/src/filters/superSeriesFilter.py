from .filter import Filter

class SuperSeriesFilter(Filter):
    ## The reason why something is filtered out at this stage
    failed_reason = "Given Experiment is a superseries"
    ## The regex terms for unwanted hit terms
    regex_terms = "s"
    filterType = "Superseries"
    
    def __init__(self, df) -> None:
        super().__init__(df, self.filterType)
    
    ### Filter by only using the outputs in Paul's listGEO -> Try out how many false negatives and we can try entrez api?
    def filterTerms(self):
        return super().filterTerms(self.regex_terms, self.failed_reason)
    
    def test(self):
        print("test")

    def __init__(self, df, filterType) -> None:
        super().__init__(df, filterType)