## This is a hidden filter, output is not important because we simply just don't want superseries

from .filter import Filter

class SuperSeriesFilter(Filter):
    ## The reason why something is filtered out at this stage
    failed_reason = "Given Experiment is a superseries"
    ## The regex terms not applicable here 
    regex_terms = "TRUE"
    filterType = "Superseries"
    relevantFields = ["SuperSeries"]
    
    def __init__(self, df) -> None:
        super().__init__(df, self.filterType, self.relevantFields)
    
    ### Filter by only using the outputs in Paul's listGEO -> Try out how many false negatives and we can try entrez api
    def filterTerms(self):
        super().filterTerms(self.regex_terms, self.failed_reason)


