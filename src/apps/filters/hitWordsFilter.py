from .internalFilterAbs import InternalFilter
from config import Config
from apps.readAndWriter import Reader

class HitWordsFilter(InternalFilter):
    ## The reason why something is filtered out at this stage
    failedReason = "Given Experiment does not match the key word in the files"
    ## Why experiemnt passed filter
    successReason = "Experiment matches the key words given"
    ## The regex terms for unwanted hit terms
    regexTerms = Reader.read_terms(Config.getHitTermsFile())
    filterType = "hitWords"
    relevantFileds = ['Title', 'Summary', 'MeSH', 'SampleTerms']
    
    def __init__(self, path=Config.getHitTermsFile()) -> None:
        super().__init__(self.filterType, self.relevantFileds)
    
    ### Filter by only using the outputs in Paul's listGEO -> Try out how many false negatives and we can try entrez api?
    def filterTerms(self, df):
        super().filterTerms(self.regexTerms, self.failedReason, self.successReason)