from .internalFilterAbs import InternalFilter
from apps.readAndWriter import Reader
from config import ConfigVariables

class HitWordsFilter(InternalFilter):
    ## The reason why something is filtered out at this stage
    failedReason = "Given Experiment does not match the key word in the files"
    ## Why experiemnt passed filter
    successReason = "Experiment matches the key words given"
    ## The regex terms for unwanted hit terms
    filterType = "hitWords"
    relevantFields = ['Title', 'Summary', 'MeSH', 'SampleTerms']
    
    def __init__(self) -> None:
        self.regexTerms = Reader.read_terms(ConfigVariables.HITTERMSFILE)
        super().__init__(self.filterType, self.relevantFields)
    
    ### Filter by only using the outputs in Paul's listGEO -> Try out how many false negatives and we can try entrez api?
    def filterTerms(self, df):
        return super().filterTerms(df, self.regexTerms, self.failedReason, self.successReason)

    def __eq__(self, o: object) -> bool:
        if (isinstance(o, HitWordsFilter)):
            return self.filterType == o.filterType and self.successReason == o.successReason and self.relevantFields == o.relevantFields and self.failedReason == o.failedReason

    
    def __hash__(self) -> int:
        return hash(self.failedReason, self.successReason, self.filterType, self.relevantFields)