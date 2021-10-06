from apps.filters import *
from apps.readAndWriter import Reader, Writer
from apps.services import GoogleSheetsService

class GeoScrapeMainSwitch:
    listOfFilters = [HitWordsFilter, NonCuratedPlatFilter, RNATypeFilter, SuperSeriesFilter, SampleSizeFilter]
    def __init__(self, inputFileLocation, outPutFileDir, hitWordsFileLoc, sep, google, notFilterHitWords) -> None:
        if notFilterHitWords:
            self.listOfFilters.remove(HitWordsFilter)
        print(self.listOfFilters)
        self.hitWordsFileLoc = hitWordsFileLoc
        self.sep = sep
        if google:
            self.gService = GoogleSheetsService(google)
            self.geoScrapeFrame = self.gService.getWorkSheetAsFrame(0)
            self.outPutFileDir = ""
        else:
            self.geoScrapeFrame = Reader.pandas_read(inputFileLocation, self.sep)
            self.outPutFileDir = outPutFileDir
        self.resultsFrame = self.geoScrapeFrame
        self.notFilterHitWords = notFilterHitWords
    

    def filterAndOutputFile(self):
        self._runFilters()
        Writer.writeGEOScrapeToCsvs(self.resultsFrame, self.geoScrapeFrame, self.sep, self.outPutFileDir, self.gService, self.notFilterHitWords)
        

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