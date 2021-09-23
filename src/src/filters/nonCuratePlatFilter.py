## This is a special filter. It does not share common methods with other filter objects because it does not rely on data

from filters import InternalFilter

class nonCuratedPlatFilter(InternalFilter):
    ## The reason why something is filtered out at this stage
    failedReason = "Given experiment uses platforms not already curated in GEMMA"
    ## Why experiemnt passed filter
    successReason = "Supported RNA type"
    ## The regex terms for unwanted hit terms
    regex_terms = "scRNA|single.cell.RNA|locRNA|lon.non.coding.rna|mirna|microRNA"
    filterType = "RNA"
    relevantFileds = ['Title', 'Summary', 'MeSH', 'SampleTerms']
    
    def __init__(self, df) -> None:
        super().__init__(df, self.filterType, self.relevantFileds)
    
    ### Filter by only using the outputs in Paul's listGEO -> Try out how many false negatives and we can try entrez api?
    def filterTerms(self):
        super().filterTerms(self.regex_terms, self.failedReason, self.successReason)
    