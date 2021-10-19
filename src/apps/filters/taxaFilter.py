from .internalFilterAbs import InternalFilter


class TaxaFilter(InternalFilter):
    # The reason why something is filtered out at this stage
    failedReason = "Given Taxon is not currently supported in GEMMA"
    # Why experiemnt passed filter
    successReason = "One of the three supported taxa"
    # The regex terms for unwanted RNA types add here if you encounter more 
    regex_terms = ["Mus musculus", "Homo sapiens", "Rattus norvegicus"]
    filterType = "Taxa"
    relevantFileds = ['Taxa']

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
