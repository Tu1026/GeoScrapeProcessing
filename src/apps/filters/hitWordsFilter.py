from apps.filters import InternalFilter
from apps import Config

class HitWordFilter(InternalFilter):
    ## The reason why something is filtered out at this stage
    failedReason = "Given Experiment does not match the key word in the files"
    ## Why experiemnt passed filter
    successReason = "Experiment matches the key words given"
    ## The regex terms for unwanted hit terms
    regex_terms = ""
    filterType = "RNA"
    relevantFileds = ['Title', 'Summary', 'MeSH', 'SampleTerms']
    
    def __init__(self, df, path=Config.getHitTermsFile) -> None:
        super().__init__(df, self.filterType, self.relevantFileds)
        with open(path, "r") as f:
            print("success")
    
    ### Filter by only using the outputs in Paul's listGEO -> Try out how many false negatives and we can try entrez api?
    def filterTerms(self):
        super().filterTerms(self.regex_terms, self.failedReason, self.successReason)
