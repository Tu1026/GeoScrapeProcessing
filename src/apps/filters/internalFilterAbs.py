# This is an abstract filter class for filers that rely on GEO output
import pandas as pd
import re
import time
from apps.misc import formatTime
from tqdm import tqdm
from abc import ABC, abstractmethod
import swifter
import dask.dataframe as dd
import multiprocessing
from dask.diagnostics import ProgressBar


class InternalFilter(ABC):
    df = None
    # The relevantFields used by the type of filter
    relevantFields = []
    filterType = ""
    text_columns = None
    resultColumn = ""

    def __init__(self, filterType, relevantFields) -> None:
        print(f'Initiaing {self.filterType} filter')
        tqdm.pandas()
        self.filterType = filterType
        self.relevantFields = relevantFields
        self.resultColumn = f'{self.filterType} Filter Results'

    def extractTextColumn(self, df):
        df = self.cleanColumns(df)
        print(
            f"Getting text from output column {self.relevantFields}."
            " Please make sure they are correct")
        self.text_columns = df[df.columns & self.relevantFields]
        return df

    def cleanColumns(self, df):
        df = df[df.iloc[:, 1] != '']
        print(
            "Please check if the below dataframe looks correct "
            f"before filtering by {self.filterType}")
        print("\n\n ========================================"
              "These are the first 5 rows =========================="
              "==============")
        print(df.head())
        print("\n\n ========================================"
              "These are the last 5 rows================"
              "========================")
        print(df.tail())
        return df


    @abstractmethod
    # Filter by only using the outputs in Paul's listGEO -> Try out how many
    # false negatives and we can try entrez api?
    def filterTerms(self, df, terms, failedReason, successReason):
        print(f"Filtering {self.filterType}")
        df = self.extractTextColumn(df)
        start = time.time()
        if self.filterType == "hitWords":
            with ProgressBar():
                df["hitList"] = dd.from_pandas(df, npartitions=2*multiprocessing.cpu_count()).map_partitions(lambda df: df.apply(
                    lambda row: self._filterTerms(
                        row,
                        terms,
                        failedReason,
                        successReason),
                    axis=1)).compute(scheduler="processes")
            df[self.resultColumn] = df["hitList"
                                       ].swifter.allow_dask_on_strings(
                enable=True).apply(
                lambda cell: (f'(Success) {successReason}'
                              if cell else f'(Failure) {failedReason}'))
        else:
            df[self.resultColumn] = df.swifter.allow_dask_on_strings(
                enable=True).apply(
                lambda row: self._filterTerms(row, terms,
                                              failedReason, successReason),
                axis=1)
        stop = time.time()
        print(
            f'Filtering {self.filterType} '
            f'took {formatTime(start, stop)} seconds')
        print(df.head())
        return df

    # Private implementation of filterTerms controls for special cases

    def _filterTerms(self, row, terms, faileReason, successReason):
        if self.filterType == "hitWords":
            hitLists = set()
            tempListOfWords = ""
            for column in self.text_columns:
                if not pd.isna(row[column]):
                    tempListOfWords = tempListOfWords + row[column]
            for term in terms:
                # Sucess if a term is present in the text
                if re.search(r'\b' + term, tempListOfWords, re.IGNORECASE):
                    hitLists.add(term)
            return list(hitLists)

        elif self.filterType == "sampleSize":
            for column in self.text_columns:
                if (not pd.isna(row[column]) and not
                        row[column] == '' and row[column] is not None):
                    if int(row[column]) <= terms:
                        return (f'(Failure) {faileReason}')
            return (f'(Success) {successReason}')

        elif self.filterType == "RNA":
            badRNAList = []
            if 'array' in row['Type']:
                return (f'(Success) {successReason}')
            elif 'Non-coding' in row['Type']:
                return (f'(Failure) {faileReason} : using non-coding')
            else:
                for column in self.text_columns:
                    if not pd.isna(row[column]):
                        for term in terms:
                            if re.search(term, str(row[column]),
                                         re.IGNORECASE):
                                badRNAList.append(term)
                return (f'(Success) {successReason}' if not badRNAList
                        else f'(Failure) {faileReason} :' +
                        ";".join(badRNAList))

        elif self.filterType == "Taxa":
            allTaxa = ""
            for column in self.text_columns:
                allTaxa += row[column]
            allTaxa = allTaxa.split(",")
            for taxon in allTaxa:
                if taxon not in terms:
                    return f'(Failure) {faileReason}'
            return f'(Success) {successReason}'

        else:
            for column in self.text_columns:
                if not pd.isna(row[column]):
                    # Failure if the term we don't want is in the text
                    if re.search(terms, str(row[column]), re.IGNORECASE):
                        return (f'(Failure) {faileReason}')
            # Sucess if the term we don't want doesn't appear
            return (f'(Success) {successReason}')
