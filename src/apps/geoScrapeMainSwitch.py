from apps.filters import *
from apps.readAndWriter import Reader, Writer
from apps.services import GoogleSheetsService

class GeoScrapeMainSwitch:
    hitWordsFileLoc = ""
    geoScrapeFrame = None
    resultsFrame =None
    outPutFileDir = ""
    sep = ""
    listOfFilters = [HitWordsFilter, NonCuratedPlatFilter, RNATypeFilter, SuperSeriesFilter, SampleSizeFilter]
    google = ""
    gService = None

    def __init__(self, inputFileLocation, outPutFileDir, hitWordsFileLoc, sep, google) -> None:
        self.google = google
        self.hitWordsFileLoc = hitWordsFileLoc
        self.sep = sep
        if self.google:
            self.gService = GoogleSheetsService(self.google)
            self.geoScrapeFrame = self.gService.getWorkSheetAsFrame(0)
        else:
            self.geoScrapeFrame = Reader.pandas_read(inputFileLocation, self.sep)
            self.outPutFileDir = outPutFileDir
        self.resultsFrame = self.geoScrapeFrame
    

    def filterAndOutputFile(self):
        self._runFilters()
        Writer.writeGEOScrapeToCsvs(self.resultsFrame, self.geoScrapeFrame, self.sep, self.outPutFileDir, self.gService)
        

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