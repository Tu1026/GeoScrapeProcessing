from apps.filters import *
from apps.readAndWriter import Reader, Writer
from config import ConfigVariables

class GeoScrapeMainSwitch:
    listOfFilters = {HitWordsFilter, NonCuratedPlatFilter, RNATypeFilter, SuperSeriesFilter, SampleSizeFilter}.discard(ConfigVariables.HITTERMSFILE)

    def __init__(self) -> None:
        if ConfigVariables.GOOGLESERVICE:
            self.geoScrapeFrame = ConfigVariables.GOOGLESERVICE.getWorkSheetAsFrame(0)
        else:
            self.geoScrapeFrame = Reader.pandas_read(ConfigVariables.FILELOCATION, self.sep)
        self.resultsFrame = self.geoScrapeFrame
        

    def filterAndOutputFile(self):
        self._runFilters()
        Writer.writeGEOScrapeToCsvs(self.resultsFrame, self.geoScrapeFrame)
        

    def _initalizeFilters(self):
        print("Creating Filters... Please make sure these are the filters you want to use")    
        [print(str(filter)) for filter in self.listOfFilters]
        initializedFilters = [filter() for filter in self.listOfFilters]
        print("Filters initialized")
        return initializedFilters

    def _runFilters(self):
        filters = self._initalizeFilters()
        print("Start running the file on all filters............................")
        for filter in filters:
            self.resultsFrame = filter.filterTerms(self.resultsFrame)