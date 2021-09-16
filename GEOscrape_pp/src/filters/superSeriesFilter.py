from typing import overload
from .filter import Filter

class SuperSeriesFilter(Filter):
    ## The reason why something is filtered out at this stage
    failed_reason = "Given Experiment is a superseries"
    ## The regex terms for unwanted hit terms
    regex_terms = "s"
    filterType = "Superseries"
    
    def __init__(self, df) -> None:
        super().__init__(df, self.filterType)
    
    ### Filter by only using the outputs in Paul's listGEO -> Try out how many false negatives and we can try entrez api
    def filterTerms(self):
        df = super().returnFrame()
        super().df = df.loc[df["SuperSeries"] == False]


