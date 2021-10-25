from apps.filters import (HitWordsFilter, NonCuratedPlatFilter, RNATypeFilter,
                          SuperSeriesFilter, SampleSizeFilter, TaxaFilter)
from apps.readAndWriter import Reader, Writer
from config import ConfigVariables
from apps.services import GeoService
import dask.dataframe as dd
import multiprocessing
from dask.diagnostics import ProgressBar


class GeoScrapeMainSwitch:
    listOfFilters = {
        HitWordsFilter,
        NonCuratedPlatFilter,
        RNATypeFilter,
        SuperSeriesFilter,
        SampleSizeFilter,
        TaxaFilter}
    columnsToGetFromExternal = ["Overall Design"]

    def __init__(self) -> None:
        # initiaitng the frame that we will be working with
        if ConfigVariables.GOOGLESERVICE:
            self.geoScrapeFrame = ConfigVariables.GOOGLESERVICE.getWorkSheetAsFrame(
                0)
        else:
            self.geoScrapeFrame = Reader.pandas_read(
                ConfigVariables.FILELOCATION, ConfigVariables.SEP)
        self.__populateColumnsWithExternalData()
        self.resultsFrame = self.geoScrapeFrame

        # Remove hitwords filter if user passed in -n
        self.listOfFilters.discard(ConfigVariables.NOHITTERM)

    # Main interactable method by outside
    def filterAndOutputFile(self):
        self.__runFilters()
        Writer.writeGEOScrapeToCsvs(self.resultsFrame, self.geoScrapeFrame)

    def __initalizeFilters(self):
        print("Creating Filters... Please make sure these are"
              " the filters you want to use")
        [print(str(filter)) for filter in self.listOfFilters]
        initializedFilters = [filter() for filter in self.listOfFilters]
        print("Filters initialized")
        return initializedFilters

    def __runFilters(self):
        filters = self.__initalizeFilters()
        print("Start running the file on all "
              "filters............................")
        for filter in filters:
            self.resultsFrame = filter.filterTerms(self.resultsFrame)

    def __populateColumnsWithExternalData(self):
        for field in self.columnsToGetFromExternal:
            self.geoScrapeFrame[field] \
                = dd.from_pandas(self.geoScrapeFrame, npartitions=2*multiprocessing.cpu_count()
                                 ).map_partitions(lambda df:
                                                  df.apply(lambda row:
                                                            self.__getDataFromGEOService(row, field), axis=1))\
                                                                .compute(scheduler="threads")

    def __getDataFromGEOService(self, row, field):
        geoSer = GeoService(row['Acc'])
        if field == "Overall Design":
            return geoSer.getOverAllDesign()
