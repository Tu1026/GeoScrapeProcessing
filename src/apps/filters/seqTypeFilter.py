
from .internalFilterAbs import InternalFilter

class seqTypeFilter(InternalFilter):
    ## The reasouperSerien why something is filtered out at this stage
    failedReason = "These experiments are array experiements that don't to be on RNA-seq pipeline"
    successReason = "These are RNA-seq experiments that need to be in the pipeline"
    ## The regex terms for unwanted hit terms
    regex_terms = "array"
    filterType = "Superseries"
    relevantFields = ["Type"]
    
    def __init__(self, df) -> None:
        super().__init__(df, self.filterType, self.relevantFields)
    
    ### Filter by only using the outputs in Paul's listGEO -> Try out how many false negatives and we can try entrez api
    def filterTerms(self):
        super().filterTerms(self.regex_terms, self.failedReason, self.successReason)

    