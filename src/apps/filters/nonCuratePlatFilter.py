## This is a special filter. It does not share common methods with other filter objects because it does not rely on data

from .internalFilterAbs import InternalFilter

class NonCuratedPlatFilter(InternalFilter):
    ## The reason why something is filtered out at this stage
    failedReason = "Platform is not already curated and in GEMMA, please double check and make sure this platform can be added"
    ## Why experiemnt passed filter
    successReason = "Platform(s) the experiment uses is/are all in GEMMA already"
    ## The regex terms for unwanted hit terms
    regex_terms = "FALSE"
    filterType = "nonCuratedPlatofrms"
    relevantFileds = ['AllPlatformsInGemma']
    
    def __init__(self) -> None:
        super().__init__(self.filterType, self.relevantFileds)
    
    ### Filter by only using the outputs in Paul's listGEO -> Try out how many false negatives and we can try entrez api?
    def filterTerms(self, df):
        super().filterTerms(df, self.regex_terms, self.failedReason, self.successReason)
    