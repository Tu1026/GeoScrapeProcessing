from .internalFilterAbs import InternalFilter


class RNATypeFilter(InternalFilter):
    # The reason why something is filtered out at this stage
    failedReason = "Given Experiment does not use an RNA techonology supported"
    # Why experiemnt passed filter
    successReason = "Supported RNA type"
    # The regex terms for unwanted RNA types add here if you encounter more 
    regex_terms = ["scRNA", "single.cell", "locRNA",
                   "long.non.coding", "mirna", 
                   "non-coding", "srna", "snRNA", "small.nuclear",
                   "rip", "rip-seq"]
    filterType = "RNA"
    relevantFileds = ['Title', 'Summary', 'MeSH', 'SampleTerms', 'Overall Desgin']

    def __init__(self) -> None:
        super().__init__(self.filterType, self.relevantFileds)

    # Filter by only using the outputs in Paul's listGEO -> Try out how many
    # false negatives and we can try entrez api?
    def filterTerms(self, df):
        return super().filterTerms(
            df,
            self.regex_terms,
            self.failedReason,
            self.successReason)
