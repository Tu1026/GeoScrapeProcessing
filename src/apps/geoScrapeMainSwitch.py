from apps.filters import (HitWordsFilter, NonCuratedPlatFilter, RNATypeFilter,
                          SuperSeriesFilter, SampleSizeFilter)
from apps.readAndWriter import Reader, Writer
from config import ConfigVariables


class GeoScrapeMainSwitch:
    listOfFilters = {
        HitWordsFilter,
        NonCuratedPlatFilter,
        RNATypeFilter,
        SuperSeriesFilter,
        SampleSizeFilter}

    def __init__(self) -> None:
        # initiaitng the frame that we will be working with
        if ConfigVariables.GOOGLESERVICE:
            self.geoScrapeFrame = ConfigVariables.GOOGLESERVICE.getWorkSheetAsFrame(
                0)
        else:
            self.geoScrapeFrame = Reader.pandas_read(
                ConfigVariables.FILELOCATION, ConfigVariables.SEP)
        self.resultsFrame = self.geoScrapeFrame

        # Remove hitwords filter if user passed in -n
        self.listOfFilters.discard(ConfigVariables.NOHITTERM)

    # Main interactable method by outside
    def filterAndOutputFile(self):
        self.__runFilters()
        Writer.writeGEOScrapeToCsvs(self.resultsFrame, self.geoScrapeFrame)

    def __initalizeFilters(self):
        print("Creating Filters... Please make sure these are the filters you want to use")
        [print(str(filter)) for filter in self.listOfFilters]
        initializedFilters = [filter() for filter in self.listOfFilters]
        print("Filters initialized")
        return initializedFilters

    def __runFilters(self):
        filters = self.__initalizeFilters()
        print("Start running the file on all filters............................")
        for filter in filters:
            self.resultsFrame = filter.filterTerms(self.resultsFrame)
