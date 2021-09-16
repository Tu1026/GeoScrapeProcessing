from re import I
from .filter import Filter

class RNATypeFilter(Filter):
    ## The reason why something is filtered out at this stage
    failed_reason = "Given Experiment does not use an RNA techonology supported"
    ## The regex terms for unwanted hit terms
    regex_terms = "scRNA|single.cell.RNA|locRNA|lon.non.coding.rna|mirna|microRNA"
    filterType = "RNA"
    
    def __init__(self, df) -> None:
        super().__init__(df, self.filterType)
    
    ### Filter by only using the outputs in Paul's listGEO -> Try out how many false negatives and we can try entrez api?
    def filterTerms(self):
        super().filterTerms(self.regex_terms, self.failed_reason)
    
