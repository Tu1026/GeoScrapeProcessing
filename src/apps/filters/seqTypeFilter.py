# No longer used replaced by other simpler methods


# from .internalFilterAbs import InternalFilter

# class SeqTypeFilter(InternalFilter):
#     ## The reasouperSerien why something is filtered out at this stage
#     failedReason = "These experiments are array experiements that don't to be on RNA-seq pipeline"
#     successReason = "These are RNA-seq experiments that need to be in the pipeline"
#     ## The regex terms for unwanted hit terms
#     regex_terms = "array"
#     filterType = "Sequencing Type"
#     relevantFields = ["Type"]

#     def __init__(self) -> None:
#         super().__init__(self.filterType, self.relevantFields)

#     ### Filter by only using the outputs in Paul's listGEO -> Try out how many false negatives and we can try entrez api
#     def filterTerms(self, df):
# return super().filterTerms(df, self.regex_terms, self.failedReason,
# self.successReason)
