from .internalFilterAbs import InternalFilter


class SampleSizeFilter(InternalFilter):
    # The reason why something is filtered out at this stage
    failedReason = "Sample Size too small"
    # Why experiemnt passed filter
    successReason = "Sample Size fine"
    # The regex terms for unwanted hit terms
    regex_terms = 2
    filterType = "sampleSize"
    relevantFileds = ['NumSamples']

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
