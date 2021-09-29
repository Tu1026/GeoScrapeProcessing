from datetime import datetime
import os
class Writer:

    @staticmethod
    def writeGEOScrapeToCsvs(resultsFrame, origFrame, sep, outPutDir):
        print(f"Outputing the file in your selected location at {outPutDir}")
        currTime = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        if sep == "\t":
            format="tsv"
        else:
            format="csv"
        ## Write main frame
        resultsFrame.to_csv(os.path.join(outPutDir,f"/{currTime}Processed_GeoSrape_mainFrame.{format}"), sep = sep, index=False)

        ## Get all the ones ready for curation
        diffColumns = resultsFrame.columns.difference(origFrame.columns)
        for column in diffColumns:
            if 


class OutputSheetsFormatting:
    @staticmethod
    def filterMainCuratableFrame(origDf, newDf):
        pass

    @staticmethod
    def hitWordsGroupingFrame(origDf, newDf):
        pass

    @staticmethod
    def groupByHitWordsFrame(origDf, newDf):
        pass

    @staticmethod
    def nonCuratedPlatFormFrame(origDf, newDf):
        pass

    @staticmethod
    def unwantedFrame(origDf, newDf):
        pass
    
     