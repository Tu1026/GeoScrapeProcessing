from apps.filters import *
from apps.readAndWriter import Reader, Writer
class GeoScrapeMainSwitch:
    hitWordsFileLoc = ""
    geoScrapeFrame = None
    filters = ["SuperSeriesFilter", "RNATypeFilter", "SeqTypeFilter", "HitWordsFilter", "NonCuratedPlatFilter"]
    resultsFrame =None
    outPutFileDir = ""
    sep = ""
    listOfFilters = [HitWordsFilter, NonCuratedPlatFilter, RNATypeFilter,
    SeqTypeFilter, SuperSeriesFilter]

    def __init__(self, inputFileLocation, outPutFileDir, hitWordsFileLoc, sep) -> None:
        self.hitWordsFileLoc = hitWordsFileLoc
        self.sep = sep
        self.geoScrapeFrame = Reader.pandas_read(inputFileLocation, self.sep)
        self.resultsFrame = self.geoScrapeFrame
        self.outPutFileDir = outPutFileDir
    

    def filterAndOutputFile(self):
        self._runFilters()
        Writer.writeToCsv(self.resultsFrame, self.sep, self.outPutFileDir)
        

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